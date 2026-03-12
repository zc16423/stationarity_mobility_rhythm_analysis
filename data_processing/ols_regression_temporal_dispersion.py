import pandas as pd
import statsmodels.api as sm
import os

# 1. Load the data
data_path = r"D:\Desktop\econometrics_data.csv"
try:
    data = pd.read_csv(data_path, encoding='utf-8')
except UnicodeDecodeError:
    data = pd.read_csv(data_path, encoding='latin1')

# 2. Significance stars function
def significance_stars(p_value):
    """
    Return significance stars based on p-value thresholds.
    """
    if p_value < 0.01:
        return "***"
    elif p_value < 0.05:
        return "**"
    elif p_value < 0.1:
        return "*"
    else:
        return ""

# 3. OLS regression function
def run_regression(data, dependent_variable, independent_variables, output_folder, filename):
    """
    Run an OLS regression using statsmodels, format the coefficients with significance stars,
    and save the regression summary to a text file.
    """
    os.makedirs(output_folder, exist_ok=True)
    
    X = data[independent_variables]
    X = sm.add_constant(X)
    y = data[dependent_variable]

    model = sm.OLS(y, X).fit()
    results_df = model.summary2().tables[1]
    
    # Format coefficients with significance stars
    results_df["Coef."] = results_df.apply(
        lambda row: f"{row['Coef.']:.4f}{significance_stars(row['P>|t|'])}", axis=1)
    
    # Replace coefficient table in text summary with formatted coefficients
    results_text = model.summary().as_text()
    for var in results_df.index:
        results_text = results_text.replace(
            f"{var: <20}",
            f"{var: <20} {results_df.loc[var, 'Coef.']: >10}"
        )
    
    output_path = os.path.join(output_folder, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(results_text)
    print(f"Regression results saved to '{output_path}'.")

# 4. Define dependent variable and independent variable groups
dependent_variable = "log_Phase_angle_variance"
output_folder = r"D:\Desktop\ols_results"

models = [
    ["pct_Hispanic_ACS_15_19", "pct_NH_Blk_alone_ACS_15_19", "pct_Prs_Blw_Pov_Lev_ACS_15_19"],
    ["pct_Hispanic_ACS_15_19", "pct_NH_Blk_alone_ACS_15_19", "pct_Prs_Blw_Pov_Lev_ACS_15_19",
     "E_PctLowWage", "Unemployed_rate"],
    ["pct_Hispanic_ACS_15_19", "pct_NH_Blk_alone_ACS_15_19", "pct_Prs_Blw_Pov_Lev_ACS_15_19",
     "E_PctLowWage", "Unemployed_rate", "pct_College_ACS_15_19", "pct_Not_HS_Grad_ACS_15_19",
     "pct_Owner_Occp_HU_ACS_15_19", "pct_Vacant_Units_ACS_15_19"],
    ["pct_Hispanic_ACS_15_19", "pct_NH_Blk_alone_ACS_15_19", "pct_Prs_Blw_Pov_Lev_ACS_15_19",
     "E_PctLowWage", "Unemployed_rate", "pct_College_ACS_15_19", "pct_Not_HS_Grad_ACS_15_19",
     "pct_Owner_Occp_HU_ACS_15_19", "pct_Vacant_Units_ACS_15_19", "NatWalkInd_Normalized"]
]

# 5. Run regressions and save results
for i, indep_vars in enumerate(models, start=1):
    filename = f"all_gidbg_regression_{i}.txt"
    run_regression(data, dependent_variable, indep_vars, output_folder, filename)
