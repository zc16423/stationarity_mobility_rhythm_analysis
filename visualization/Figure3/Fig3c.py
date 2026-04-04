"""
Figure 3c
Stratification of RSI_phi by data density.

CBGs are grouped into quartiles based on their device counts:
    Q1: 0–25% (lowest device count)
    Q2: 25–50%
    Q3: 50–75%
    Q4: 75–100% (highest device count)

This stratification controls for potential sparsity effects.
The persistence of racial disparities across quartiles
demonstrates the robustness of the RSI_phi signal.

Input:
    figure_data/Figure3/Fig3c/Fig3c.csv

Required columns:
 group_Q
   phase_angle_variance	

Output:
    visualization/Figure3/Fig3c/Fig3c.svg
"""

from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# ==============================
# 0. Reproducibility
# ==============================
np.random.seed(42)

# ==============================
# 1. Paths (GitHub-friendly)
# ==============================
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "figure_data" / "Figure3" / "Fig3c"
OUT_DIR = BASE_DIR / "visualization" / "Figure3" / "Fig3c"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ==============================
# 2. Plot style (NC compliant)
# ==============================
plt.rcParams.update({
    'font.family': ['Arial', 'DejaVu Sans'],
    'font.weight': 'normal',
    'svg.fonttype': 'none'
})
sns.set_theme(style="white")

# ==============================
# 3. Load data with validation
# ==============================
files = {
    'Black': DATA_DIR / "Black.csv",
    'Hispanic': DATA_DIR / "Hispanic.csv",
    'White': DATA_DIR / "White.csv"
}

required_cols = {'group_Q', 'phase_angle_variance'}

data_list = []

for race, path in files.items():
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    df = pd.read_csv(path)

    if not required_cols.issubset(df.columns):
        raise ValueError(f"{path} missing required columns {required_cols}")

    df = df.copy()
    df['Race'] = race
    data_list.append(df)

df_all = pd.concat(data_list, ignore_index=True)

# ==============================
# 4. Data processing
# ==============================
group_map = {
    1: 'Low',
    2: 'Medium-Low',
    3: 'Medium-High',
    4: 'High'
}

df_all['Device_Count_Group'] = df_all['group_Q'].map(group_map)

if df_all['Device_Count_Group'].isna().any():
    raise ValueError("Invalid values found in group_Q")

df_all = df_all.rename(columns={'phase_angle_variance': 'RSI_phi'})

group_order = ['Low', 'Medium-Low', 'Medium-High', 'High']
race_order = ['White', 'Hispanic', 'Black']

colors = {
    'White': '#33bfeb',
    'Hispanic': '#ff7f0e',
    'Black': '#d62728'
}

# ==============================
# 5. Plot
# ==============================
fig, ax = plt.subplots(figsize=(11, 8))

sns.boxplot(
    data=df_all,
    x='Device_Count_Group',
    y='RSI_phi',
    hue='Race',
    order=group_order,
    hue_order=race_order,
    palette=colors,
    showfliers=False,
    linewidth=1.5,
    width=0.7,
    showmeans=True,
    meanprops={
        "marker": "d",
        "markerfacecolor": "white",
        "markeredgecolor": "black",
        "markersize": 8
    },
    ax=ax
)

# ==============================
# 6. Styling
# ==============================
ax.set_ylabel(r'$\mathrm{RSI}_{\phi}$', fontsize=28)
ax.set_xlabel('Device Count', fontsize=28)

ax.set_xticks(range(len(group_order)))
ax.set_xticklabels(group_order, fontsize=22)

ax.set_ylim(0, 0.7)

# spine
for spine in ['left', 'bottom']:
    ax.spines[spine].set_linewidth(2)
    ax.spines[spine].set_color('black')

sns.despine(ax=ax, top=True, right=True)

# ticks
ax.tick_params(
    axis='both',
    which='major',
    direction='out',
    length=8,
    width=2,
    labelsize=22
)

# legend
ax.legend(
    title=None,
    loc='upper right',
    fontsize=20,
    frameon=False
)

plt.tight_layout()

# ==============================
# 7. Save (with metadata)
# ==============================
output_path = OUT_DIR / "Fig3c.svg"

plt.savefig(
    output_path,
    format='svg',
    bbox_inches='tight',
    metadata={
        "Creator": "Matplotlib",
        "Description": "Figure 3c: RSI_phi stratified by device density quartiles"
    }
)

plt.close()

print(f"Figure saved to: {output_path}")

# ==============================
# 8. Entry point
# ==============================
if __name__ == "__main__":
    pass