"""
Figure 1i: State-level daily rhythm patterns.

This script visualizes empirical hourly mobility rhythms and fitted
sinusoidal models for each U.S. state using polar coordinates.

Input data
----------
figure_data/Figure1/Fig1i/

For each state there are two files:

StateName.csv
    Hourly empirical observations (rows = observations, columns = 24 hours)

StateName_fit.csv
    Fitted sinusoidal parameters with columns:
        Amplitude
        Phase Angle
        Baseline

Output
------
visualization/Figure1/Fig1i/
    One SVG file per state.
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

input_folder = Path("../../figure_data/Figure1/Fig1i")
output_folder = Path("Fig1i")

output_folder.mkdir(exist_ok=True)

# -----------------------------------
# Collect CSV files
# -----------------------------------

csv_files = list(input_folder.glob("*.csv"))

file_names = [f.name for f in csv_files]

# -----------------------------------
# Process each state
# -----------------------------------

for file_name in file_names:

    if not file_name.endswith("_fit.csv"):

        file_name_fit = file_name.replace(".csv", "_fit.csv")

        if file_name_fit in file_names:

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

            hours = np.arange(24)

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

            fig = plt.figure(figsize=(4.3, 4.6))

            ax = fig.add_subplot(projection="polar")

            # Empirical curve
            ax.plot(
                angles,
                means,
                color="#4b6aa8",
                linewidth=4.5,
                label="Empirical",
            )

            # Confidence interval
            ax.fill_between(
                angles,
                means - ci,
                means + ci,
                color="#4b6aa8",
                alpha=0.5,
                linewidth=8,
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
                    linewidth=4.5,
                )

            # -------------------------
            # Title formatting
            # -------------------------

            title = "".join(
                [i for i in file_name if not i.isdigit()]
            ).replace(".csv", "")

            ax.set_title(
                title,
                va="bottom",
                fontsize=52,
                weight="bold",
                pad=0,
                backgroundcolor="#f0a02f",
                color="white",
            )

            # -------------------------
            # Polar axis configuration
            # -------------------------

            ax.set_theta_direction(-1)
            ax.set_theta_offset(np.pi / 2.0)

            ax.set_xticklabels([])
            ax.set_yticklabels([])

            ax.set_thetagrids([0, 90, 180, 270])

            ax.grid(
                True,
                linestyle="--",
                color="gray",
                linewidth=2,
                alpha=1.0,
            )

            ax.set_facecolor("white")

            ax.spines["polar"].set_linewidth(2.5)
            ax.spines["polar"].set_color("black")

            ax.set_rticks([0.325, 0.65])
            ax.set_rlabel_position(-225)

            # -------------------------
            # Save figure
            # -------------------------

            output_path = output_folder / f"{file_name.replace('.csv','')}.svg"

            plt.subplots_adjust(
                left=0,
                right=1,
                top=0.79,
                bottom=0,
            )

            plt.savefig(output_path, format="svg")

            plt.close(fig)

            print("Saved:", output_path)