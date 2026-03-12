
"""
Fig4a
Fitted curves for devices at home per hour on weekdays.

Blue line  : mean before U.S. national emergency
Red line   : mean after U.S. national emergency
Gray lines : individual fitted curves

Input data
----------
figure_data/Figure4/Fig4a/

Output
------
visualization/Figure4/Fig4a/

"""

import pandas as pd
import numpy as np
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

DATA_DIR = ROOT / "data" / "fig4"
OUTPUT_DIR = ROOT / "figures"

OUTPUT_DIR.mkdir(exist_ok=True)

before_file = DATA_DIR / "before.csv"
during_file = DATA_DIR / "during.csv"

output_path = OUTPUT_DIR / "Fig4a.svg"


# -------------------------
# Load data
# -------------------------

data_before = pd.read_csv(before_file)
data_during = pd.read_csv(during_file)

amp_before = data_before["Amplitude"]
phase_before = data_before["Phase Angle"]
base_before = data_before["Baseline"]

amp_during = data_during["Amplitude"]
phase_during = data_during["Phase Angle"]
base_during = data_during["Baseline"]


# -------------------------
# Time axis
# -------------------------

x = np.linspace(0, 2*np.pi, 1000)


# -------------------------
# Plot
# -------------------------

fig, ax = plt.subplots(figsize=(9, 5.5))

gray_before = "#D3D3D3"
gray_during = "#B0B0B0"


# ---- individual curves ----

for a, b, c in zip(amp_before, phase_before, base_before):
    y = a * np.sin(x + b) + c
    ax.plot(x, y, color=gray_before, linewidth=0.5)

for a, b, c in zip(amp_during, phase_during, base_during):
    y = a * np.sin(x + b) + c
    ax.plot(x, y, color=gray_during, linewidth=0.5)


# -------------------------
# Mean fitted curves
# -------------------------

amp_before_mean = 0.163685010586481
phase_before_mean = 1.2381308797992419
base_before_mean = 0.44274728780936423

y_before_mean = amp_before_mean * np.sin(x + phase_before_mean) + base_before_mean

ax.plot(
    x,
    y_before_mean,
    color="#1f77b4",
    linewidth=3,
    label="Before National Emergency (Mean)"
)


amp_after_mean = 0.08975118156211995
phase_after_mean = 1.0711461759483718
base_after_mean = 0.49231654180670525

y_after_mean = amp_after_mean * np.sin(x + phase_after_mean) + base_after_mean

ax.plot(
    x,
    y_after_mean,
    color="#ee6666",
    linewidth=3,
    label="After National Emergency (Mean)"
)


# -------------------------
# Legend
# -------------------------

ax.legend(
    loc="lower left",
    fontsize=18,
    frameon=False,
    ncol=2
)


# -------------------------
# Axis labels
# -------------------------

ax.set_xlabel(r"$x_t$", fontsize=20)
ax.set_ylabel(r"$R(t)$", fontsize=20)


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
    left=0.10,
    right=0.98,
    top=0.98,
    bottom=0.12
)


# -------------------------
# Save
# -------------------------

plt.savefig(
    output_path,
    format="svg",
    bbox_inches="tight"
)

plt.close()

print("Fig4a saved to:", output_path)