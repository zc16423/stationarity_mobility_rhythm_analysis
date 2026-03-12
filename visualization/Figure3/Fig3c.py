"""
Figure 3c
Stratification of RSI_phi by data density.

CBGs are grouped into quartiles based on their device counts:
    Q1: 0–25% (lowest device count)
    Q2: 25–50%
    Q3: 50–75%
    Q4: 75–100% (highest device count)

This stratification controls for potential sparsity effects.
The persistence of racial disparities across quartiles
demonstrates the robustness of the RSI_phi signal.

Error bars represent 95% confidence intervals.

Input:
    figure_data/Figure3/Fig3c/Fig3c.csv

Required columns:
    Device_Count_Group
    Race
    mean
    CI_upper

Output:
    visualization/Figure3/Fig3c//Fig3c.svg
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
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

df = pd.read_csv(DATA_DIR / "Fig3c.csv")


# ---------------------------
# Color scheme
# ---------------------------

colors = {
    "White": "#33bfeb",
    "Hispanic": "#ff7f0e",
    "Black": "#d62728"
}


# ---------------------------
# Prepare groups
# ---------------------------

groups = df["Device_Count_Group"].unique()

x = np.arange(len(groups))
width = 0.3


# ---------------------------
# Create figure
# ---------------------------

fig, ax = plt.subplots(figsize=(8, 6))


# ---------------------------
# Bar plots with 95% CI
# ---------------------------

for i, race in enumerate(["White", "Hispanic", "Black"]):

    race_data = df[df["Race"] == race]

    means = race_data["mean"].values

    errors = (race_data["CI_upper"] - race_data["mean"]).values

    offset = width * (i - 0.5)

    ax.bar(
        x + offset,
        means,
        width,
        label=race,
        color=colors[race],
        yerr=errors,
        capsize=5,
        alpha=0.8,
        error_kw={
            "elinewidth": 1.5,
            "markeredgewidth": 1.5
        }
    )


# ---------------------------
# Axis labels
# ---------------------------

ax.set_ylabel(r"$RSI_\phi$", fontsize=26)
ax.set_xlabel("Device Count Quartile", fontsize=26)

ax.set_xticks(x)
ax.set_xticklabels(groups, fontsize=24)


# Y-axis range
ax.set_ylim(-0.05, 0.5)


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
    loc="upper right",
    fontsize=24,
    frameon=False
)


# ---------------------------
# Layout
# ---------------------------

plt.tight_layout()

plt.subplots_adjust(
    left=0.14,
    right=0.97,
    top=0.98,
    bottom=0.14
)


# ---------------------------
# Save figure
# ---------------------------

output_path = FIGURE_DIR / "Fig3c.svg"

plt.savefig(output_path, format="svg")

plt.show()

print(f"Figure saved to {output_path}")