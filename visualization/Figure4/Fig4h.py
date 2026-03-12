
"""
Fig4h
Violin plots comparing weekday changes in baseline parameter B
between Mar.13–Dec.31 in 2019 and 2020.

Blue : 2019
Red  : 2020

Input data
----------
figure_data/Figure4/Fig4h/

Output
------
visualization/Figure4/Fig4h/
"""

import pandas as pd
import seaborn as sns
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

DATA_DIR = ROOT / "figure_data" / "Figure4" / "Fig4h"
OUTPUT_DIR = ROOT / "visualization"/ "Figure4" / "Fig4h"

OUTPUT_DIR.mkdir(exist_ok=True)

output_path = OUTPUT_DIR / "Fig4h.svg"


# -------------------------
# Group definitions
# -------------------------

groups = {
    "White": ["White_2019.csv", "White_2020.csv"],
    "Hispanic": ["Hispanic_2019.csv", "Hispanic_2020.csv"],
    "Black": ["Black_2019.csv", "Black_2020.csv"]
}


# -------------------------
# Load data
# -------------------------

def load_data():

    frames = []

    for group, files in groups.items():

        for file in files:

            df = pd.read_csv(DATA_DIR / file, usecols=["Baseline"])

            df = df.rename(columns={"Baseline": "Value"})

            df["Group"] = group

            if "2019" in file:
                df["Date"] = "2019-03-13 to 2019-12-31"
            else:
                df["Date"] = "2020-03-13 to 2020-12-31"

            frames.append(df)

    data = pd.concat(frames, ignore_index=True)

    data["Group"] = pd.Categorical(
        data["Group"],
        categories=["White", "Hispanic", "Black"],
        ordered=True
    )

    return data


data = load_data()


# -------------------------
# Plot
# -------------------------

sns.set_style("white")

fig, ax = plt.subplots(figsize=(9.5, 6))

sns.violinplot(
    data=data,
    x="Group",
    y="Value",
    hue="Date",
    split=True,
    inner="quart",
    linewidth=1.2,
    palette={
        "2019-03-13 to 2019-12-31": "skyblue",
        "2020-03-13 to 2020-12-31": "salmon"
    },
    ax=ax
)


# -------------------------
# Labels
# -------------------------

ax.set_xlabel("Race", fontsize=20)
ax.set_ylabel(r"$B$", fontsize=20)

ax.set_title("Baseline", fontsize=22)


# -------------------------
# Legend
# -------------------------

ax.legend(
    title="Date",
    loc="upper right",
    fontsize=18,
    title_fontsize=18,
    frameon=False
)


# -------------------------
# Axis formatting
# -------------------------

ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, _: f"{x:.2f}")
)

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
    left=0.12,
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

print("Fig4h saved to:", output_path)