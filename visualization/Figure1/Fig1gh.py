"""
Figure 1g–h: Spatial distribution of peak and valley mobility ratios.

This script visualizes county-level spatial patterns of the peak and 
valley values of the mobility ratio R(t) across the United States.

Input data
----------
figure_data/Figure1/Fig1gh.csv

Required columns
----------------
county   : 5-digit county FIPS code
max_y    : peak value of R(t)
min_y    : valley value of R(t)

Shapefile
---------
figure_data/Figure1/Fig1gh/county_shapefile/county.shp

Output
------
visualization/Figure1/Fig1gh.svg
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from pathlib import Path

# -----------------------------------
# Matplotlib configuration
# -----------------------------------

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.weight"] = "normal"
plt.rcParams["svg.fonttype"] = "none"

plt.style.use("seaborn-white")

# -----------------------------------
# Path configuration
# -----------------------------------

shapefile_path = Path("../../figure_data/Figure1/Fig1gh/county_shapefile/county.shp")
csv_path = Path("../../figure_data/Figure1/Fig1gh.csv")
output_path = Path("Fig1gh.svg")

# -----------------------------------
# Load spatial data
# -----------------------------------

gdf = gpd.read_file(shapefile_path)

# Construct county FIPS
gdf["FIPS"] = gdf["STATEFP"].str.zfill(2) + gdf["COUNTYFP"].str.zfill(3)

# -----------------------------------
# Load attribute data
# -----------------------------------

df = pd.read_csv(csv_path, dtype={"county": str})

# Ensure FIPS codes have leading zeros
df["county"] = df["county"].str.zfill(5)

# Merge spatial and attribute data
merged_gdf = gdf.merge(df, left_on="FIPS", right_on="county", how="left")

# -----------------------------------
# Data validation (printed for reproducibility checks)
# -----------------------------------

print("Valid observations for max_y:", merged_gdf["max_y"].notna().sum())
print("Unique values for max_y:", merged_gdf["max_y"].nunique())

print("Valid observations for min_y:", merged_gdf["min_y"].notna().sum())
print("Unique values for min_y:", merged_gdf["min_y"].nunique())

# -----------------------------------
# Visualization parameters
# -----------------------------------

cmap = plt.cm.plasma_r

vmin = 0.19
vmax = 0.72

# -----------------------------------
# Create figure
# -----------------------------------

fig, axes = plt.subplots(1, 2, figsize=(26, 14))

# Peak map
merged_gdf.plot(
    column="max_y",
    cmap=cmap,
    linewidth=0.2,
    edgecolor="#767171",
    ax=axes[0],
    missing_kwds={"color": "lightgrey"},
    legend=False,
    vmin=vmin,
    vmax=vmax,
)

# Valley map
merged_gdf.plot(
    column="min_y",
    cmap=cmap,
    linewidth=0.2,
    edgecolor="#767171",
    ax=axes[1],
    missing_kwds={"color": "lightgrey"},
    legend=False,
    vmin=vmin,
    vmax=vmax,
)

plt.draw()

# -----------------------------------
# Titles
# -----------------------------------

axes[0].set_title("Peak", fontsize=36, pad=1)
axes[1].set_title("Valley", fontsize=36, pad=1)

# Remove axes
for ax in axes:
    ax.set_axis_off()

# -----------------------------------
# Shared colorbar
# -----------------------------------

norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

cbar = fig.colorbar(
    sm,
    ax=axes,
    orientation="horizontal",
    fraction=0.03,
    pad=0.05,
)

ticks = np.arange(0.2, 0.8, 0.1).round(1)

cbar.set_ticks(ticks)
cbar.set_ticklabels([str(t) for t in ticks])

cbar.set_label(r"$R(t)$", fontsize=36)

cbar.ax.tick_params(
    labelsize=28,
    width=2,
    length=5,
)

# Ensure SVG compatibility
cbar.solids.set_edgecolor("face")
cbar.solids.set_rasterized(False)

# -----------------------------------
# Layout
# -----------------------------------

plt.subplots_adjust(
    left=0.01,
    right=0.99,
    top=0.98,
    bottom=0.15,
)

# -----------------------------------
# Save figure
# -----------------------------------

plt.savefig(output_path, format="svg", bbox_inches="tight")

print("Figure saved to:", output_path)

plt.close()