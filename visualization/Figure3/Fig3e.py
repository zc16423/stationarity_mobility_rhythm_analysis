"""
Figure 3e
RSI_phi in individual CBGs in Atlanta at the 50% threshold.

Each scatter point represents a census block group (CBG).
The point size corresponds to the magnitude of RSI_phi.
Larger points indicate stronger temporal rhythm intensity.

Input:
    figure_data/Figure3/Fig3e/Atlanta_shapefile/Atlanta.shp
    figure_data/Figure3/Fig3e/White.csv
    figure_data/Figure3/Fig3e/Hispanic.csv
    figure_data/Figure3/Fig3e/Black.csv

Required CSV columns:
    origin_census_block_group
    phase_angle_variance

Output:
    visualization/Figure3/Fig3e.svg
"""

import geopandas as gpd
import pandas as pd
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

SHAPE_PATH = DATA_DIR / "Atlanta_shapefile" / "Atlanta.shp"


# ---------------------------
# Plot style
# ---------------------------

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.weight"] = "normal"
plt.rcParams["svg.fonttype"] = "none"


# ---------------------------
# Load shapefile
# ---------------------------

gdf = gpd.read_file(SHAPE_PATH)

gdf["GEOID"] = gdf["GEOID"].astype(str)


# ---------------------------
# Input CSV files
# ---------------------------

csv_files = {
    "White": ("White.csv", "#33bfeb"),
    "Hispanic": ("Hispanic.csv", "#ff7f0e"),
    "Black": ("Black.csv", "#d62728")
}


dfs = {}

for group, (file, color) in csv_files.items():

    df = pd.read_csv(DATA_DIR / file)

    df["origin_census_block_group"] = df["origin_census_block_group"].astype(str)

    df["color"] = color

    dfs[group] = df


# ---------------------------
# Merge data
# ---------------------------

df_all = pd.concat(dfs.values(), ignore_index=True)

merged = gdf.merge(
    df_all,
    left_on="GEOID",
    right_on="origin_census_block_group",
    how="right"
)

merged = merged.to_crs(epsg=4326)


# Convert polygons to centroids
merged["geometry"] = merged["geometry"].centroid


# ---------------------------
# Map point sizes
# ---------------------------

def map_size(value):

    if 0.03 <= value < 0.15:
        return 10
    elif 0.15 <= value < 0.27:
        return 200
    elif 0.27 <= value < 0.39:
        return 400
    elif 0.39 <= value < 0.50:
        return 600
    elif 0.50 <= value < 0.62:
        return 800
    elif 0.62 <= value < 0.74:
        return 1000
    else:
        return 50


merged["size"] = merged["phase_angle_variance"].apply(map_size)


# ---------------------------
# Plot map
# ---------------------------

fig, ax = plt.subplots(figsize=(12.5, 12.5))

gdf.plot(
    ax=ax,
    color="lightgrey",
    edgecolor="white"
)


# Scatter points
for group, (file, color) in csv_files.items():

    subset = merged[merged["color"] == color]

    ax.scatter(
        subset.geometry.x,
        subset.geometry.y,
        s=subset["size"],
        color=color,
        label=group,
        alpha=0.8,
        edgecolors="black",
        linewidth=0.7
    )


# ---------------------------
# Scale bar
# ---------------------------

scale_length = 5000

latitude_atlanta = 33.75

conversion_factor = 111320 * np.cos(np.radians(latitude_atlanta))

dist_in_deg = scale_length / conversion_factor

xmin = gdf.bounds.minx.min()
ymin = gdf.bounds.miny.min()

ax.plot(
    [xmin, xmin + dist_in_deg],
    [ymin, ymin],
    color="black",
    linewidth=2
)

ax.text(
    xmin + dist_in_deg / 2,
    ymin + 0.001,
    f"{scale_length} m",
    fontsize=24
)


# ---------------------------
# Labels
# ---------------------------

ax.set_title("Atlanta", fontsize=30)

ax.set_xlabel("Longitude", fontsize=26)
ax.set_ylabel("Latitude", fontsize=26)

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

handles = [
    plt.scatter(
        [],
        [],
        s=400,
        color=color,
        label=group,
        edgecolors="black",
        linewidth=0.7
    )
    for group, (_, color) in csv_files.items()
]

ax.legend(
    handles=handles,
    loc="lower right",
    fontsize=24,
    frameon=False
)


# ---------------------------
# Save figure
# ---------------------------

output_path = FIGURE_DIR / "Fig3e.svg"

plt.savefig(
    output_path,
    format="svg",
    bbox_inches="tight"
)

plt.show()

print(f"Figure saved to {output_path}")