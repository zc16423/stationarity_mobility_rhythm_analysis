
"""
Fig4g
Weekly values of baseline parameter B in 2020 weekdays.

Blue    : majority-White CBGs
Orange  : majority-Hispanic CBGs
Red     : majority-Black CBGs

Vertical dashed line indicates the U.S. national emergency declaration (2020-03-13).

Input data
----------
figure_data/Figure4/Fig4g/

Output
------
visualization/Figure4/Fig4g/
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

DATA_DIR = ROOT / "figure_data" / "Figure4" / "Fig4g"
OUTPUT_DIR = ROOT / "visualization"/ "Figure4" / "Fig4g"

OUTPUT_DIR.mkdir(exist_ok=True)

output_path = OUTPUT_DIR / "Fig4g.svg"


# -------------------------
# Groups and colors
# -------------------------

groups = ["White", "Hispanic", "Black"]

colors = {
    "White": "#33bfeb",
    "Hispanic": "#ff7f0e",
    "Black": "#d62728"
}


# -------------------------
# Create figure
# -------------------------

fig, ax = plt.subplots(figsize=(13.5, 6))


# -------------------------
# Plot time series
# -------------------------

for group in groups:

    df = pd.read_csv(DATA_DIR / f"{group}.csv")

    ax.plot(
        df["Week"],
        df["Baseline"],
        linewidth=3,
        color=colors[group],
        label=group
    )


# -------------------------
# National emergency marker
# -------------------------

week_emergency = 11

ax.axvline(
    week_emergency,
    linestyle="--",
    linewidth=0.8,
    color="#333333"
)

ax.text(
    week_emergency,
    ax.get_ylim()[1] * 0.98,
    "National Emergency (2020-03-13)",
    ha="left",
    va="top",
    fontsize=18
)


# -------------------------
# Axis labels
# -------------------------

ax.set_xlabel("Week (2020)", fontsize=20)
ax.set_ylabel(r"$B$", fontsize=20)

ax.set_xticks(np.arange(1, 54, 3))


# -------------------------
# Legend
# -------------------------

ax.legend(
    loc="upper right",
    fontsize=18,
    frameon=False
)


# -------------------------
# Style
# -------------------------

ax.grid(False)

for spine_loc, spine in ax.spines.items():

    if spine_loc in ["left", "bottom"]:

        spine.set_visible(True)
        spine.set_color("black")
        spine.set_linewidth(1.5)

    else:

        spine.set_visible(False)


ax.tick_params(
    axis="both",
    which="both",
    direction="out",
    length=7,
    width=1.5,
    color="black",
    labelsize=18
)

ax.yaxis.set_ticks_position("left")
ax.xaxis.set_ticks_position("bottom")


# -------------------------
# Layout
# -------------------------

plt.subplots_adjust(
    left=0.08,
    right=0.98,
    top=0.95,
    bottom=0.12
)


# -------------------------
# Save figure
# -------------------------

plt.savefig(
    output_path,
    format="svg",
    bbox_inches="tight"
)

plt.close()

print("Fig4g saved to:", output_path)