"""
Figure 3d
Valley time corresponding to phi for each CBG at the 50% threshold.

Scatter points represent 10,000 randomly sampled CBGs from each
racial group. The dashed black line indicates the mean valley
time across all communities within each group.

Time is mapped to polar angles:
    11:00 → 0°
    16:00 → 90°

Input:
    figure_data/Figure3/Fig3d

Required column:
    Time2  (format HH:MM)

Output:
    visualization/Figure3/Fig3d_White.svg
    visualization/Figure3/Fig3d_Hispanic.svg
    visualization/Figure3/Fig3d_Black.svg
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
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


# ---------------------------
# Input files
# ---------------------------

files = {
    "White": DATA_DIR / "White.csv",
    "Hispanic": DATA_DIR / "Hispanic.csv",
    "Black": DATA_DIR / "Black.csv"
}

colors = {
    "White": "#33bfeb",
    "Hispanic": "#ff7f0e",
    "Black": "#d62728"
}


# ---------------------------
# Time → angle conversion
# ---------------------------

def time_to_angle(time_str):

    base_time = datetime.datetime.strptime("11:00", "%H:%M")
    max_time = datetime.datetime.strptime("16:00", "%H:%M")

    current_time = datetime.datetime.strptime(time_str, "%H:%M")

    total_minutes = (max_time - base_time).total_seconds() / 60
    elapsed_minutes = (current_time - base_time).total_seconds() / 60

    return (elapsed_minutes / total_minutes) * 90


# ---------------------------
# Process each group
# ---------------------------

for group, path in files.items():

    if not path.exists():
        print(f"{path} not found. Skipping.")
        continue

    df = pd.read_csv(path)

    # Convert time to angle
    df["Angle"] = df["Time2"].apply(time_to_angle)

    # Mean angle
    mean_angle = np.radians(df["Angle"].mean())

    # Random sampling
    df_sampled = df.sample(
        n=min(10000, len(df)),
        random_state=42
    )

    # ---------------------------
    # Create polar plot
    # ---------------------------

    fig, ax = plt.subplots(
        subplot_kw={"projection": "polar"},
        figsize=(5.5, 5.5)
    )

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    ax.set_ylim(0, 1)

    ax.set_thetamin(0)
    ax.set_thetamax(90)

    # Random radii
    radii = np.random.uniform(
        0.15,
        1,
        len(df_sampled)
    )

    angles = np.radians(df_sampled["Angle"])

    # Scatter points
    ax.scatter(
        angles,
        radii,
        color=colors[group],
        s=6,
        alpha=0.6,
        edgecolors="none"
    )

    # Mean line
    ax.plot(
        [mean_angle, mean_angle],
        [0, 1],
        color="black",
        linestyle="--",
        linewidth=2,
        label=r"Mean valley of time ($\phi$)"
    )


    # ---------------------------
    # Time ticks
    # ---------------------------

    tick_labels = [
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00"
    ]

    tick_angles = np.radians(
        np.linspace(0, 90, len(tick_labels))
    )

    ax.set_xticks(tick_angles)
    ax.set_xticklabels(
        tick_labels,
        fontsize=20
    )

    ax.grid(True, linewidth=2.0)

    ax.set_title(
        group,
        fontsize=22,
        pad=5
    )

    ax.spines["polar"].set_linewidth(2.0)

    ax.set_yticks([])

    ax.legend(
        loc="upper right",
        fontsize=22,
        frameon=False
    )


    # ---------------------------
    # Save figure
    # ---------------------------

    output_path = FIGURE_DIR / f"Fig3d_{group}.svg"

    plt.savefig(
        output_path,
        format="svg",
        bbox_inches="tight"
    )

    plt.show()

    print(f"{group} figure saved to {output_path}")