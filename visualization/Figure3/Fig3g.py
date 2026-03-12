

"""
Figure 3g
OLS regression results on determinants of temporal dispersion
in population mobility.

Each column represents a regression model and each row a
predictor variable. Cell color indicates coefficient value.

Input:
    figure_data/Figure3/Fig3g/*.csv

Required columns in each file:
    Variable
    Coefficient

Output:
    visualization/Figure3/Fig3g.svg
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib.colors import TwoSlopeNorm


# ---------------------------
# Path configuration
# ---------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "figure_data" / "Figure3"/ "Fig3g"
FIGURE_DIR = BASE_DIR / "visualization"/ "Figure3"

FIGURE_DIR.mkdir(exist_ok=True)

output_path = FIGURE_DIR / "Fig3g.svg"


# ---------------------------
# Plot style
# ---------------------------

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.weight"] = "normal"
plt.rcParams["svg.fonttype"] = "path"


# ---------------------------
# Load model files
# ---------------------------

model_files = sorted(DATA_DIR.glob("*.csv"))

models = {}
vars_by_model = []


for f in model_files:

    df = pd.read_csv(f)

    df = df[["Variable", "Coefficient"]]

    models[f.name] = df

    vars_by_model.append(df["Variable"].tolist())


# Variables determined by the last model
all_vars = vars_by_model[-1]

n_var = len(all_vars)
n_model = len(model_files)


# ---------------------------
# Build coefficient matrix
# ---------------------------

M = np.full((n_var, n_model), np.nan)


for j, f in enumerate(model_files):

    df = models[f.name]

    mapping = dict(zip(df["Variable"], df["Coefficient"]))

    for i, var in enumerate(all_vars):

        if var in mapping:
            M[i, j] = mapping[var]


# ---------------------------
# Plot heatmap
# ---------------------------

fig, ax = plt.subplots(figsize=(7, 10))

ax.set_facecolor("white")
fig.patch.set_facecolor("white")


norm = TwoSlopeNorm(vmin=-0.1, vcenter=0, vmax=0.2)

cmap = plt.get_cmap("PiYG_r")


mesh = ax.pcolormesh(
    M,
    cmap=cmap,
    norm=norm,
    edgecolors="white",
    linewidth=1.2,
    rasterized=False
)


# ---------------------------
# Annotate coefficients
# ---------------------------

for i in range(n_var):

    for j in range(n_model):

        val = M[i, j]

        if not np.isnan(val):

            ax.text(
                j + 0.5,
                i + 0.5,
                f"{val:.2f}",
                ha="center",
                va="center",
                fontsize=16,
                color="black"
            )


# ---------------------------
# Axis configuration
# ---------------------------

ax.xaxis.tick_top()

ax.set_xticks(np.arange(n_model) + 0.5)

ax.set_xticklabels(
    [f.stem for f in model_files],
    fontsize=20
)

ax.set_yticks(np.arange(n_var) + 0.5)

ax.set_yticklabels(
    all_vars,
    fontsize=20
)

ax.invert_yaxis()

ax.set_xlim(0, n_model)

ax.set_ylim(n_var, 0)


# ---------------------------
# Colorbar
# ---------------------------

cbar_ax = fig.add_axes([0.05, 0.02, 0.75, 0.035])

cbar = fig.colorbar(
    mesh,
    cax=cbar_ax,
    orientation="horizontal"
)

cbar.set_ticks([-0.6, -0.4, -0.2, 0, 0.5, 1, 1.5])

cbar.ax.tick_params(labelsize=20)

cbar.solids.set_edgecolor("face")

cbar.solids.set_rasterized(False)

cbar.solids.set_antialiased(True)


# ---------------------------
# Layout
# ---------------------------

plt.subplots_adjust(
    left=0.15,
    right=0.92,
    top=0.97,
    bottom=0.08
)


# ---------------------------
# Save figure
# ---------------------------

plt.savefig(
    output_path,
    format="svg",
    dpi=300,
    bbox_inches="tight",
    transparent=False,
    facecolor="white"
)

plt.close()

print("Figure generated:", output_path)