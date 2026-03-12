"""
Figure 2b — Mobility Range Distribution by Race (Original vs Population-weighted)

This script generates the violin plot for Fig.2b, comparing mobility range
distributions across three racial groups under two data-processing strategies:

1. Original mobility data
2. Population-weighted mobility data (weighted by community population)

Input
-----
CSV files stored in:

figure_data/Figure2/Fig2b/

Expected files:
    White_Original.csv
    White_Weighted.csv
    Hispanic_Original.csv
    Hispanic_Weighted.csv
    Black_Original.csv
    Black_Weighted.csv

Each CSV must contain the column:
    Range

Output
------
visualization/Figure2/Fig2b.svg

"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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
DATA_DIR = ROOT / "data" / "figure2b"
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

            df = pd.read_csv(file_path, usecols=["Range"])

            df = df.melt(var_name="Device", value_name="Range")

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
# Plot function
# -------------------------------------------------

def plot_violin(data, output_path):

    sns.set_style("white")
    sns.set_palette("muted")

    fig, ax = plt.subplots(figsize=(6.5, 5.4))

    sns.violinplot(
        data=data,
        x="Group",
        y="Range",
        hue="Type",
        split=True,
        inner="quart",
        fill=True,
        palette={"Weighted": "skyblue", "Original": "salmon"},
        ax=ax
    )

    ax.set_title("Range", fontsize=28)
    ax.set_xlabel("Race", fontsize=20)
    ax.set_ylabel(r"$2A$", fontsize=20)

    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"{x:.2f}")
    )

    ax.legend(loc="upper right", fontsize=18, frameon=False)

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
        left=0.15,
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

    output_path = FIG_DIR / "Fig2b_range_distribution.svg"

    plot_violin(data, output_path)


if __name__ == "__main__":
    main()