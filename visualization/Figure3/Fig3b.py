"""
Figure 3b
Relationship between racial composition proportion and RSI_phi.

This script estimates robust linear regressions between the
proportion of a racial group within census block groups and
the corresponding RSI_phi value.

Three groups are considered:
    White
    Hispanic
    Black

Input:
    figure_data/Figure3/Fig3b/

Each file must contain:
    Proportion
    Mean_Variance

Output:
    visualization/Figure2/Fig3b.svg
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from pathlib import Path


# ---------------------------
# Path configuration
# ---------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
FIGURE_DIR = BASE_DIR / "figures"

FIGURE_DIR.mkdir(exist_ok=True)


# ---------------------------
# Plot style
# ---------------------------

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.weight"] = "normal"
plt.rcParams["svg.fonttype"] = "none"

sns.set_theme(style="white")


# ---------------------------
# Load data
# ---------------------------

white_data = pd.read_csv(DATA_DIR / "fig3b_white.csv")
hispanic_data = pd.read_csv(DATA_DIR / "fig3b_hispanic.csv")
black_data = pd.read_csv(DATA_DIR / "fig3b_black.csv")


# Add group labels
white_data["Group"] = "White"
hispanic_data["Group"] = "Hispanic"
black_data["Group"] = "Black"


# Merge datasets
combined_data = pd.concat(
    [white_data, hispanic_data, black_data],
    ignore_index=True
)


# ---------------------------
# Visualization settings
# ---------------------------

color_map = {
    "White": "#33bfeb",
    "Hispanic": "#ff7f0e",
    "Black": "#d62728"
}

marker_map = {
    "White": "o",
    "Hispanic": "s",
    "Black": "D"
}


# ---------------------------
# Create figure
# ---------------------------

fig, ax = plt.subplots(figsize=(8, 6))


# Regression plots
for group in ["White", "Hispanic", "Black"]:

    group_data = combined_data[combined_data["Group"] == group]

    prev_collections = len(ax.collections)

    sns.regplot(
        data=group_data,
        x="Proportion",
        y="Mean_Variance",
        ax=ax,
        label=group,
        color=color_map[group],
        marker=marker_map[group],
        scatter_kws={"s": 40},
        ci=95,
        robust=True
    )

    # Adjust CI transparency
    new_collections = ax.collections[prev_collections:]

    for coll in new_collections:
        if isinstance(coll, PolyCollection):
            coll.set_alpha(0.4)


# ---------------------------
# Axis labels
# ---------------------------

ax.set_xlabel("Proportion (%)", fontsize=26)
ax.set_ylabel(r"$RSI_\phi$", fontsize=26)


# Format y-axis
ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, _: f"{x:.2f}")
)


# Remove grid
ax.grid(False)


# ---------------------------
# Spine styling
# ---------------------------

for spine_location, spine in ax.spines.items():

    if spine_location in ["left", "bottom"]:
        spine.set_visible(True)
        spine.set_color("black")
        spine.set_linewidth(1.5)

    else:
        spine.set_visible(False)


# ---------------------------
# Tick styling
# ---------------------------

ax.tick_params(
    axis="both",
    which="both",
    direction="out",
    length=7,
    width=1.5,
    color="black",
    labelsize=24
)

ax.yaxis.set_ticks_position("left")
ax.xaxis.set_ticks_position("bottom")


# ---------------------------
# Legend
# ---------------------------

ax.legend(
    title=None,
    loc="upper left",
    fontsize=24,
    frameon=False,
    scatterpoints=1,
    markerscale=2
)


# ---------------------------
# Layout
# ---------------------------

plt.subplots_adjust(
    left=0.15,
    right=0.98,
    top=0.98,
    bottom=0.14
)


# ---------------------------
# Save figure
# ---------------------------

output_path = FIGURE_DIR / "Fig3b_RSI_phi_proportion.svg"

plt.savefig(output_path, format="svg")

plt.show()

print(f"Figure saved to {output_path}")