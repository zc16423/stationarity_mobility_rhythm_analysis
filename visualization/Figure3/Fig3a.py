"""
Figure 3a
Distribution of RSI_phi across racial groups.

This script plots kernel density estimation (KDE) curves of the
RSI_phi distribution for three racial groups:
White, Hispanic, and Black.

Input:
    figure_data/Figure3/Fig3a

Each file must contain the column:
    phase_angle_variance

Output:
    visualization/Figure3/Fig3a.svg
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'
plt.rcParams['svg.fonttype'] = 'none'

sns.set_theme(style="white")


# ---------------------------
# Input files
# ---------------------------

file_paths = {
    "White": DATA_DIR / "fig3a_white.csv",
    "Hispanic": DATA_DIR / "fig3a_hispanic.csv",
    "Black": DATA_DIR / "fig3a_black.csv"
}


# ---------------------------
# Color scheme
# ---------------------------

colors = {
    "White": "#33bfeb",
    "Hispanic": "#ff7f0e",
    "Black": "#d62728"
}


# ---------------------------
# Load and merge data
# ---------------------------

data = pd.DataFrame()

for group, path in file_paths.items():

    df = pd.read_csv(path)
    df["Group"] = group

    data = pd.concat([data, df], ignore_index=True)


# ---------------------------
# Create figure
# ---------------------------

fig, ax = plt.subplots(figsize=(8, 6))


# KDE curves
for group, color in colors.items():

    sns.kdeplot(
        data=data[data["Group"] == group],
        x="phase_angle_variance",
        ax=ax,
        color=color,
        label=group,
        fill=True,
        alpha=0.6,
        linewidth=2
    )


# ---------------------------
# Axis configuration
# ---------------------------

ax.set_xlabel(r"$RSI_\phi$", fontsize=26)
ax.set_ylabel("Density", fontsize=26)

ax.set_xlim(0, 1)

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
# Layout
# ---------------------------

plt.subplots_adjust(
    left=0.12,
    right=0.95,
    top=0.98,
    bottom=0.15
)


# ---------------------------
# Legend
# ---------------------------

ax.legend(
    title=None,
    loc="upper right",
    fontsize=24,
    frameon=False
)


# ---------------------------
# Save figure
# ---------------------------

output_path = FIGURE_DIR / "Fig3a.svg"

plt.savefig(output_path, format="svg")

plt.show()

print(f"Figure saved to {output_path}")