"""
Figure 2c — Phase Angle Distribution by Race (Original vs Population-weighted)

This script generates the violin plot for Fig.2c, comparing the distribution
of the phase angle (time of mobility valley) across racial groups under
two data-processing strategies:

1. Original mobility data
2. Population-weighted mobility data

Input
-----
CSV files stored in:

figure_data/Figure2/Fig2c/

Expected files:
    White_Original.csv
    White_Weighted.csv
    Hispanic_Original.csv
    Hispanic_Weighted.csv
    Black_Original.csv
    Black_Weighted.csv

Each CSV must contain the column:
    Time1

Time1 represents the phase angle (valley time) in decimal hours.

Output
------
visualization/Figure2/Fig2c.svg
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


# -------------------------------------------------
# Matplotlib configuration
# -------------------------------------------------

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'
plt.rcParams['svg.fonttype'] = 'none'


# -------------------------------------------------
# Repository paths
# -------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "figure2c"
FIG_DIR = ROOT / "figures"

FIG_DIR.mkdir(exist_ok=True)


# -------------------------------------------------
# Group definitions
# -------------------------------------------------

groups = {
    "White": ["White_Original.csv", "White_Weighted.csv"],
    "Hispanic": ["Hispanic_Original.csv", "Hispanic_Weighted.csv"],
    "Black": ["Black_Original.csv", "Black_Weighted.csv"]
}


# -------------------------------------------------
# Load and process data
# -------------------------------------------------

def load_and_process_data():

    data = pd.DataFrame()

    for group, files in groups.items():

        for file_name in files:

            file_path = DATA_DIR / file_name

            df = pd.read_csv(file_path, usecols=["Time1"])

            df = df.melt(var_name="Device", value_name="Time1")

            df["Group"] = group

            if "Original" in file_name:
                df["Type"] = "Original"
            else:
                df["Type"] = "Weighted"

            data = pd.concat([data, df], ignore_index=True)

    data["Group"] = pd.Categorical(
        data["Group"],
        categories=["White", "Hispanic", "Black"],
        ordered=True
    )

    data["Type"] = pd.Categorical(
        data["Type"],
        categories=["Weighted", "Original"],
        ordered=True
    )

    return data


# -------------------------------------------------
# Convert decimal hour to HH:MM format
# -------------------------------------------------

def convert_time_to_hm(time_val):

    hours = int(time_val)

    minutes = int((time_val - hours) * 60)

    return f"{hours:02}:{minutes:02}"


# -------------------------------------------------
# Plot function
# -------------------------------------------------

def plot_violin(data, output_path):

    sns.set_style("white")
    sns.set_palette("muted")

    fig, ax = plt.subplots(figsize=(7, 5.4))

    sns.violinplot(
        data=data,
        x="Group",
        y="Time1",
        hue="Type",
        split=True,
        inner="quart",
        fill=True,
        palette={"Weighted": "skyblue", "Original": "salmon"},
        ax=ax
    )

    ax.set_ylim(10.5, 16.5)

    ticks = np.linspace(10.5, 16.5, 7)

    labels = [convert_time_to_hm(t) for t in ticks]

    ax.set_yticks(ticks)
    ax.set_yticklabels(labels)

    ax.set_title("Phase Angle", fontsize=28)

    ax.set_xlabel("Race", fontsize=20)

    ax.set_ylabel(r"Time of valley ($\phi$)", fontsize=20)

    ax.legend(loc="lower right", fontsize=18, frameon=False)

    ax.grid(False)

    for spine_location, spine in ax.spines.items():

        if spine_location in ["left", "bottom"]:

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

    plt.subplots_adjust(
        left=0.17,
        right=0.98,
        top=0.92,
        bottom=0.13
    )

    plt.savefig(output_path, format="svg")

    plt.close()


# -------------------------------------------------
# Main
# -------------------------------------------------

def main():

    data = load_and_process_data()

    output_path = FIG_DIR / "Fig2c_phase_angle_distribution.svg"

    plot_violin(data, output_path)


if __name__ == "__main__":
    main()