"""
Figure 2e — State-level Mobility Range Comparison by Race

This script generates the state-level comparison plot (dumbbell-style)
for the mobility range parameter (2A) across racial groups in the United States.

Each state is represented by a horizontal line connecting the values
for different racial groups.

Input
-----
CSV file located in:

figure_data/Figure2/Fig2e/Fig2e_range.csv

Expected columns:
    name      : state abbreviation (e.g., CA, NY, TX)
    White     : parameter value for White population
    Hispanic  : parameter value for Hispanic population
    Black     : parameter value for Black population

Output
------
visualization/Figure2/Fig2e/Fig2e_range_state_comparison.svg

"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
DATA_FILE = ROOT / "data" / "figure2e" / "Fig2e_range.csv"
FIG_DIR = ROOT / "figures"

FIG_DIR.mkdir(exist_ok=True)


# -------------------------------------------------
# Strict state order
# -------------------------------------------------

STRICT_ORDER = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
    'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
    'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
    'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
    'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]


# -------------------------------------------------
# Color mapping
# -------------------------------------------------

COLORS = {
    "White": "#71b7ed",
    "Hispanic": "#f2b56f",
    "Black": "#f57c6e"
}


# -------------------------------------------------
# Utility
# -------------------------------------------------

def transform_value(value):

    try:
        return float(value) if not pd.isna(value) else None
    except ValueError:
        return None


# -------------------------------------------------
# Load data
# -------------------------------------------------

def load_data():

    df = pd.read_csv(DATA_FILE)

    df["name"] = pd.Categorical(
        df["name"],
        categories=STRICT_ORDER,
        ordered=True
    )

    df = df.sort_values("name")

    df["y_position"] = range(len(df))

    return df


# -------------------------------------------------
# Plot function
# -------------------------------------------------

def plot_state_comparison(df, output_path):

    fig, ax = plt.subplots(figsize=(7, 12))

    # Remove top/right spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.xaxis.grid(True, linestyle="--", alpha=1)
    ax.yaxis.grid(False)

    # -----------------------------
    # Draw connecting lines
    # -----------------------------

    for _, row in df.iterrows():

        x_values = {
            "White": transform_value(row["White"]),
            "Hispanic": transform_value(row["Hispanic"]),
            "Black": transform_value(row["Black"])
        }

        valid_values = {k: v for k, v in x_values.items() if v is not None}

        if len(valid_values) >= 2:

            sorted_x = sorted(valid_values.values())

            ax.plot(
                sorted_x,
                [row["y_position"]] * len(sorted_x),
                color="black",
                lw=1.5
            )

    # -----------------------------
    # Draw scatter points
    # -----------------------------

    for _, row in df.iterrows():

        x_values = {
            "White": transform_value(row["White"]),
            "Hispanic": transform_value(row["Hispanic"]),
            "Black": transform_value(row["Black"])
        }

        valid_values = {k: v for k, v in x_values.items() if v is not None}

        for group, x_value in valid_values.items():

            ax.scatter(
                x_value,
                row["y_position"],
                color=COLORS[group],
                s=150,
                edgecolors="black",
                linewidth=1,
                zorder=3
            )

    # -----------------------------
    # Axis configuration
    # -----------------------------

    ax.set_xlim(0.11, 0.36)

    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.04))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%.2f"))

    ax.set_yticks(df["y_position"])
    ax.set_yticklabels(df["name"])

    ax.invert_yaxis()

    # Legend

    handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=COLORS[k],
            markersize=10,
            markeredgecolor="black",
            label=k
        )
        for k in COLORS
    ]

    ax.legend(handles=handles, loc="upper left", fontsize=14, frameon=False)

    ax.set_xlabel(r"$2A$", fontsize=20)
    ax.set_ylabel("State", fontsize=20)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

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
        color="black"
    )

    ax.yaxis.set_ticks_position("left")
    ax.xaxis.set_ticks_position("bottom")

    plt.subplots_adjust(
        left=0.15,
        right=0.96,
        top=0.99,
        bottom=0.06
    )

    plt.savefig(output_path, format="svg")

    plt.close()


# -------------------------------------------------
# Main
# -------------------------------------------------

def main():

    df = load_data()

    output_path = FIG_DIR / "Fig2e_range_state_comparison.svg"

    plot_state_comparison(df, output_path)


if __name__ == "__main__":
    main()