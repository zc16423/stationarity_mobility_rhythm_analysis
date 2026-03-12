"""
Figure 1f: Model fitting quality.

This script visualizes the relationship between the coefficient of 
determination (R²) and the residual sum of squares (RSS) for fitted 
rhythmic models.

Input data
----------
figure_data/Figure1/Fig1f.csv

Required columns
----------------
R2
Residuals Sum

Output
------
visualization/Figure1/Fig1f.svg
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from pathlib import Path

# -----------------------------------
# Matplotlib configuration
# -----------------------------------

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.weight"] = "normal"
plt.rcParams["svg.fonttype"] = "none"

sns.set_theme(style="white")

# -----------------------------------
# Path configuration
# -----------------------------------

data_path = Path("../../figure_data/Figure1/Fig1f.csv")
output_path = Path("Fig1f.svg")

# -----------------------------------
# Load data
# -----------------------------------

data = pd.read_csv(data_path)

# -----------------------------------
# Create joint regression plot
# -----------------------------------

g = sns.jointplot(
    x="R2",
    y="Residuals Sum",
    data=data,
    kind="reg",
    truncate=False,
    color="#5470c6",
    height=9,
    scatter_kws={"s": 150},
)

# Remove marginal distributions
g.ax_marg_x.remove()
g.ax_marg_y.remove()

# Main axes
ax = g.ax_joint

# -----------------------------------
# Axis configuration
# -----------------------------------

ax.set_xlim(0.87, 1)
ax.xaxis.set_major_locator(MultipleLocator(0.02))

ax.set_ylim(0, None)
ax.yaxis.set_major_locator(MultipleLocator(0.01))

ax.set_xlabel(r"R$^2$", fontsize=28)
ax.set_ylabel(r"RSS", fontsize=28)

ax.grid(False)

# -----------------------------------
# Spine formatting
# -----------------------------------

for location, spine in ax.spines.items():

    if location in ["left", "bottom"]:
        spine.set_visible(True)
        spine.set_color("black")
        spine.set_linewidth(2)
    else:
        spine.set_visible(False)

# -----------------------------------
# Tick formatting
# -----------------------------------

ax.tick_params(
    axis="both",
    which="both",
    direction="out",
    length=10,
    width=2,
    color="black",
    labelsize=28,
)

ax.yaxis.set_ticks_position("left")
ax.xaxis.set_ticks_position("bottom")

# -----------------------------------
# Layout
# -----------------------------------

plt.subplots_adjust(
    left=0.10,
    right=0.99,
    top=0.99,
    bottom=0.09,
)

g.fig.set_size_inches(12, 9)

# -----------------------------------
# Save figure
# -----------------------------------

plt.savefig(output_path, format="svg")

print("Figure saved to:", output_path)