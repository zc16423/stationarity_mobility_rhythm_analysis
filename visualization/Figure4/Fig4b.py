
"""
Fig4b
Calendar heatmaps showing mean value of R(t) over 24 hours
for weekdays in the U.S., 2020.

Months shown: March, April, September, October.

Input data
----------
figure_data/Figure4/Fig4b/

Output
------
visualization/Figure4/Fig4b/

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import numpy as np
from pathlib import Path


# -------------------------
# Global plotting style
# -------------------------

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'
plt.rcParams['svg.fonttype'] = 'none'


# -------------------------
# Paths (repo structure)
# -------------------------

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "figure_data" / "Figure4" / "Fig4b"
OUTPUT_DIR = ROOT / "visualization"/ "Figure4" / "Fig4b"

OUTPUT_DIR.mkdir(exist_ok=True)

input_file = DATA_DIR / "Fig4b.csv"
output_path = OUTPUT_DIR / "Fig4b.svg"


# -------------------------
# Load data
# -------------------------

data = pd.read_csv(input_file)

data["Date"] = pd.to_datetime(data["Date"])

data["Year"] = data["Date"].dt.year
data["Month"] = data["Date"].dt.month


# -------------------------
# Filter: weekdays in 2020
# -------------------------

data_2020 = data[
    (data["Year"] == 2020) &
    (data["Date"].dt.dayofweek < 5)
]


# Selected months
months = [3, 4, 9, 10]

data_2020 = data_2020[data_2020["Month"].isin(months)]


# -------------------------
# Plot
# -------------------------

sns.set_style("white")

fig, axes = plt.subplots(1, 4, figsize=(14, 4))


# colorbar axis
cbar_ax = fig.add_axes([0.35, -0.05, 0.3, 0.04])


for i, month in enumerate(months):

    ax = axes[i]

    month_data = data_2020[data_2020["Month"] == month].copy()

    month_data.set_index("Date", inplace=True)

    month_days = calendar.monthrange(2020, month)[1]

    cal_data = pd.DataFrame(
        index=pd.date_range(
            start=f"2020-{month:02d}-01",
            end=f"2020-{month:02d}-{month_days}"
        )
    )

    cal_data["24-hour rate"] = np.nan

    cal_data.update(month_data["24-hour rate"])

    cal_data["Week"] = ((cal_data.index.day - 1) // 7) + 1
    cal_data["Day"] = cal_data.index.weekday

    cal_pivot = cal_data.pivot(
        index="Week",
        columns="Day",
        values="24-hour rate"
    )

    cal_pivot = cal_pivot.reindex(columns=range(5))


    sns.heatmap(
        cal_pivot,
        ax=ax,
        cmap="PiYG_r",
        vmin=0.4,
        vmax=0.58,
        linewidths=1,
        linecolor="white",
        cbar=True if i == 0 else False,
        cbar_ax=cbar_ax if i == 0 else None,
        cbar_kws={"orientation": "horizontal"} if i == 0 else None
    )


    ax.set_title(
        calendar.month_abbr[month],
        fontsize=22
    )

    ax.xaxis.tick_top()

    ax.set_xticklabels(
        ["M", "T", "W", "T", "F"],
        fontsize=18
    )

    ax.set_yticklabels(
        [f"Week {int(w)}" for w in cal_pivot.index],
        rotation=0,
        fontsize=18
    )

    ax.tick_params(length=0)

    for spine in ax.spines.values():
        spine.set_visible(False)


# colorbar formatting
cbar_ax.tick_params(labelsize=18)


# labels
fig.text(
    0.5,
    -0.15,
    r"24-hours Mean $R(t)$",
    ha="center",
    fontsize=20
)

fig.text(
    0.5,
    1.02,
    "National Emergency (2020-03-13)",
    ha="center",
    fontsize=18
)


# layout
plt.subplots_adjust(
    left=0.06,
    right=0.98,
    top=0.85,
    bottom=0.15,
    wspace=0.25
)


# save
plt.savefig(
    output_path,
    format="svg",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Fig4b saved to:", output_path)