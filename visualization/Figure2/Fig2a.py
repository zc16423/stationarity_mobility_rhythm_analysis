"""
Figure 2a: Daily mobility rhythms by racial groups.

This script visualizes empirical hourly mobility ratios and fitted
sinusoidal rhythm models for different racial groups using polar plots.

Input data
----------
figure_data/Figure2/Fig2a/

Each group has two files:

GroupName.csv
    Empirical hourly observations (24 columns representing hours)

GroupName_fit.csv
    Sinusoidal model parameters:
        Amplitude
        Phase Angle
        Baseline

Output
------
visualization/Figure2/Fig2a/
    Polar plots for each racial group.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
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

input_folder = Path("../../figure_data/Figure2/Fig2a")
output_folder = Path("Fig2a")

output_folder.mkdir(exist_ok=True)

# -----------------------------------
# Collect CSV files
# -----------------------------------

csv_files = [f.name for f in input_folder.glob("*.csv")]

# -----------------------------------
# Process each racial group
# -----------------------------------

for file_name in csv_files:

    if not file_name.endswith("_fit.csv"):

        file_name_fit = file_name.replace(".csv", "_fit.csv")

        if file_name_fit in csv_files:

            file_path_1 = input_folder / file_name
            file_path_2 = input_folder / file_name_fit

            # -------------------------
            # Load data
            # -------------------------

            data_empirical = pd.read_csv(file_path_1)
            data_fit = pd.read_csv(file_path_2)

            # -------------------------
            # Empirical statistics
            # -------------------------

            means = data_empirical.mean(axis=0)
            stderr = data_empirical.sem(axis=0)

            confidence_level = 0.95

            ci = stderr * t.ppf(
                (1 + confidence_level) / 2.0,
                len(data_empirical) - 1,
            )

            # Close circular curve
            means = np.concatenate([means, [means[0]]])
            ci = np.concatenate([ci, [ci[0]]])

            angles = np.deg2rad(
                np.linspace(0, 360, 25, endpoint=True)
            )

            # -------------------------
            # Model parameters
            # -------------------------

            amplitudes = data_fit["Amplitude"]
            phase_angles = data_fit["Phase Angle"]
            baselines = data_fit["Baseline"]

            x = np.linspace(0, 2 * np.pi, 1000)

            # -------------------------
            # Create polar plot
            # -------------------------

            fig = plt.figure(figsize=(5.5, 5.5))

            ax = fig.add_subplot(projection="polar")

            # Empirical curve
            ax.plot(
                angles,
                means,
                color="#4b6aa8",
                linewidth=4,
                label="Empirical",
            )

            # Confidence interval
            ax.fill_between(
                angles,
                means - ci,
                means + ci,
                color="#4b6aa8",
                linewidth=7,
                alpha=0.5,
                label="95% CI",
            )

            # Model curves
            for a, b, c in zip(
                amplitudes,
                phase_angles,
                baselines,
            ):

                y = a * np.sin(x + b) + c

                ax.plot(
                    x,
                    y,
                    color="#ee6666",
                    linestyle="--",
                    linewidth=4,
                    label="Model",
                )

            # -------------------------
            # Title
            # -------------------------

            title = file_name.replace(".csv", "")

            ax.set_title(
                title,
                va="bottom",
                fontsize=32,
                weight="bold",
                pad=20,
                backgroundcolor="#f0a02f",
                color="white",
            )

            # -------------------------
            # Polar axis configuration
            # -------------------------

            ax.set_theta_direction(-1)
            ax.set_theta_offset(np.pi / 2.0)

            ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2])

            ax.set_xticklabels(
                ["00:00", "06:00", "12:00", "18:00"],
                fontsize=24,
            )

            ax.set_thetagrids([0, 90, 180, 270])

            ax.grid(
                True,
                linestyle="--",
                color="gray",
                linewidth=1.5,
                alpha=1.0,
            )

            ax.set_facecolor("white")

            ax.tick_params(labelsize=24)

            ax.spines["polar"].set_linewidth(1.5)
            ax.spines["polar"].set_color("black")

            ax.set_rticks([0.21, 0.42, 0.63])
            ax.set_rlabel_position(-225)

            # -------------------------
            # Save figure
            # -------------------------

            output_path = output_folder / f"{title}_polar_plot.svg"

            plt.subplots_adjust(
                left=0,
                right=1,
                top=0.8,
                bottom=0.05,
            )

            plt.savefig(output_path, format="svg")

            plt.close(fig)

            print("Saved:", output_path)