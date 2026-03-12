"""
Figure 1e: Distribution of rhythmic curves and mean rhythm.

This script visualizes sinusoidal curves fitted for individual units
(e.g., census block groups) and overlays the mean rhythm.

Input data
----------
figure_data/Figure1/Fig1e.csv

Columns required:
    Amplitude
    Phase Angle
    Baseline

Output
------
visualization/Figure1/Fig1e.svg
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------------
# Matplotlib configuration
# -----------------------------------

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.weight"] = "normal"
plt.rcParams["svg.fonttype"] = "none"

# -----------------------------------
# Path configuration
# -----------------------------------

data_path = Path("../../figure_data/Figure1/Fig1e.csv")
output_path = Path("Fig1e.svg")

# -----------------------------------
# Read data
# -----------------------------------

data = pd.read_csv(data_path)

amplitudes = data["Amplitude"]
phase_angles = data["Phase Angle"]
baselines = data["Baseline"]

# -----------------------------------
# Mean parameters (estimated from sample)
# -----------------------------------

mean_amp = 0.13869380375550777
mean_phase = 1.1389609754337795
mean_base = 0.4585188690359699

# -----------------------------------
# Generate x values
# -----------------------------------

x = np.linspace(0, 2 * np.pi, 1000)

# -----------------------------------
# Plot
# -----------------------------------

fig, ax = plt.subplots(figsize=(12, 7.5))

gray_color = "#D3D3D3"

# Individual rhythm curves
for a, b, c in zip(amplitudes, phase_angles, baselines):

    y = a * np.sin(x + b) + c

    ax.plot(
        x,
        y,
        color=gray_color,
        linewidth=0.5
    )

# Mean rhythm curve
y_mean = mean_amp * np.sin(x + mean_phase) + mean_base

ax.plot(
    x,
    y_mean,
    color="#ee6666",
    linewidth=3,
    label="Mean"
)

# -----------------------------------
# Figure styling
# -----------------------------------

ax.legend(
    loc="lower left",
    fontsize=28,
    frameon=False
)

ax.set_xlabel(r"$x_t$", fontsize=28)
ax.set_ylabel(r"$R(t)$", fontsize=28)

ax.grid(False)

# Spine formatting
for location, spine in ax.spines.items():

    if location in ["left", "bottom"]:
        spine.set_visible(True)
        spine.set_color("black")
        spine.set_linewidth(2)
    else:
        spine.set_visible(False)

# Tick formatting
ax.tick_params(
    axis="both",
    direction="out",
    length=10,
    width=2,
    color="black",
    labelsize=28
)

ax.yaxis.set_ticks_position("left")
ax.xaxis.set_ticks_position("bottom")

plt.subplots_adjust(
    left=0.10,
    right=0.99,
    top=0.90,
    bottom=0.11
)

# -----------------------------------
# Save figure
# -----------------------------------

plt.savefig(output_path, format="svg")
plt.close()

print("Figure saved to:", output_path)