"""
Figure 1c: Weekly patterns of R(t) for three cities.

This script reads hourly activity data from CSV files and constructs a 
continuous time series from April 1–5, 2019. It then visualizes the 
temporal pattern for New York, Los Angeles, and Chicago.

Expected data format:
- Each CSV file contains one row per day.
- Column "Date" stores the date.
- Columns "0:00"–"23:00" store hourly values.

Directory structure:
Input data:
    figure_data/Figure1/
        New York.csv
        Los Angeles.csv
        Chicago.csv

Output:
    visualization/Figure1/Fig1c.svg
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

# -------------------------------------------------
# Matplotlib configuration
# -------------------------------------------------
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.weight"] = "normal"
plt.rcParams["svg.fonttype"] = "none"

# -------------------------------------------------
# Parameters
# -------------------------------------------------
cities = ["New York", "Los Angeles", "Chicago"]

colors = ["#4b6aa8", "#f0a02f", "#ee6666"]

start_date = pd.to_datetime("2019-04-01 00:00")
end_date = pd.to_datetime("2019-04-05 23:00")

# Paths (relative paths for GitHub reproducibility)
data_dir = Path("../data")
output_dir = Path("../figures")
output_dir.mkdir(exist_ok=True)

# -------------------------------------------------
# Create continuous hourly time index
# -------------------------------------------------
time_index = pd.date_range(start=start_date, end=end_date, freq="H")

# -------------------------------------------------
# Read CSV files
# -------------------------------------------------
data_dict = {}

for city in cities:
    file_path = data_dir / f"{city}.csv"
    df = pd.read_csv(file_path)
    df["Date"] = pd.to_datetime(df["Date"])
    data_dict[city] = df

# -------------------------------------------------
# Construct hourly time series
# -------------------------------------------------
new_data = pd.DataFrame(index=time_index)

for city, df in data_dict.items():
    for _, row in df.iterrows():
        date = row["Date"]

        for hour in range(24):
            t = date + pd.Timedelta(hours=hour)
            new_data.loc[t, city] = row[f"{hour}:00"]

# -------------------------------------------------
# Plot
# -------------------------------------------------
fig, ax = plt.subplots(figsize=(17, 8))

# Background shading for alternating days
for day in range(5):

    day_start = start_date + pd.Timedelta(days=day)
    day_end = day_start + pd.Timedelta(hours=24)

    start_num = mdates.date2num(day_start)
    end_num = mdates.date2num(day_end)

    if day % 2 == 0:
        ax.axvspan(start_num, end_num, facecolor="#d9d9d9", alpha=0.3)

# Plot city curves
for i, city in enumerate(cities):

    ax.plot(
        new_data.index,
        new_data[city],
        marker="o",
        markersize=8,
        linewidth=2,
        color=colors[i],
        label=city,
    )

# -------------------------------------------------
# Styling
# -------------------------------------------------
ax.set_xlabel("Date and time", fontsize=28)
ax.set_ylabel(r"$R(t)$", fontsize=28)
ax.set_title("Weekly patterns", fontsize=32)

ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
ax.set_ylim(0.2, 0.7)

# Remove grid
ax.grid(False)

# Spine formatting
for location, spine in ax.spines.items():

    if location in ["left", "bottom"]:
        spine.set_visible(True)
        spine.set_linewidth(2)
        spine.set_color("black")
    else:
        spine.set_visible(False)

# Tick formatting
ax.tick_params(
    axis="both",
    which="both",
    direction="out",
    length=10,
    width=2,
    labelsize=28,
)

ax.yaxis.set_ticks_position("left")
ax.xaxis.set_ticks_position("bottom")

# Legend
ax.legend(
    loc="lower right",
    fontsize=28,
    frameon=False,
    ncol=3,
)

plt.subplots_adjust(
    left=0.08,
    right=0.97,
    top=0.92,
    bottom=0.10,
)

# -------------------------------------------------
# Save figure
# -------------------------------------------------
output_path = output_dir / "Fig1c.svg"

plt.savefig(output_path, format="svg")
plt.show()