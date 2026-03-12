import os
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# Input and output folder paths
input_folder = r"D:\Desktop\hourly_mobility_ratio"
output_folder = r"D:\Desktop\fit_results"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

def fit_func(x, a, c, d):
    """
    Sinusoidal fitting function:
    y = a * sin(x + c) + d
    where:
    a = amplitude,
    c = phase shift,
    d = baseline offset.
    """
    return a * np.sin(x + c) + d

# Iterate over each CSV file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_folder, filename)
        
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Time columns start from the 4th column (index 3)
        time_columns = df.columns[3:]
        num_hours = len(time_columns)
        
        # Check if there are exactly 24 hourly columns
        if num_hours != 24:
            print(f"File {filename} has {num_hours} time columns (expected 24), skipping.")
            continue
        
        results = []
        
        # Iterate over each row (each community)
        for _, row in df.iterrows():
            
            cbg = row['origin_census_block_group']
            race = row['Race']
            device_count = row['device_count']
            y = row[time_columns].values  # y values for hours 0:00 to 23:00
            
            # Generate x values as linspace from 0 to 2π
            x = np.linspace(0, 2 * np.pi, num_hours)
            
            try:
                # Fit the sinusoidal function to data
                params, params_covariance = curve_fit(fit_func, x, y, maxfev=10000)
                
                # Predicted values from the fit
                predicted_ratios = fit_func(x, *params)
                
                # Residuals calculation
                residuals = y - predicted_ratios
                
                # Calculate R-squared and adjusted R-squared
                r2 = r2_score(y, predicted_ratios)
                n = len(y)
                p = len(params)
                adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
                
                # Sum of squared residuals
                residuals_sum = np.sum(residuals**2)
                
                # Calculate range as double the amplitude
                amplitude = params[0]
                range_value = amplitude * 2
                
                # Append fitting results
                results.append({
                    'origin_census_block_group': cbg,
                    'Race': race,
                    'device_count': device_count,
                    'Amplitude': amplitude,
                    'Phase Angle': params[1],
                    'Baseline': params[2],
                    'R2': r2,
                    'Adjusted R2': adjusted_r2,
                    'Residuals Sum': residuals_sum,
                    'Range': range_value
                })
            
            except RuntimeError:
                print(f"Could not fit data for community {cbg}, skipping this row.")
        
        # Save results into a new DataFrame
        results_df = pd.DataFrame(results)
        
        # Save results to output folder with same filename (CSV)
        output_file_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.csv")
        results_df.to_csv(output_file_path, index=False)