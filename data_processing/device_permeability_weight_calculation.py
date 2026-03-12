
import os
import pandas as pd
import numpy as np

# Input folder path containing raw mobility data
input_folder = r"E:\stationarity_mobility_rhythm"
# For scientific replication, we typically overwrite or save to a derivative folder
# Here we update the files in place as per original logic

# Required columns for permeability and weighting calculation
REQUIRED_COLS = ['device_count', 'Tot_Population_ACS_15_19']

# Iterate over each CSV file in the study directory
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_folder, filename)
        
        # Load dataset with encoding robust to BOM and special characters
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue

        # Validate existence of necessary demographic and device columns
        if not all(col in df.columns for col in REQUIRED_COLS):
            print(f"File {filename} missing required columns {REQUIRED_COLS}, skipping.")
            continue

        try:
            # --- Permeability and Weight Calculation ---
            # Permeability represents the sampling rate within each census unit (%)
            df['Permeability'] = (df['device_count'] / df['Tot_Population_ACS_15_19']) * 100
            
            # Weight is the reciprocal of permeability to expand sample to total population
            # Replace 0 values with NaN to prevent infinity during division
            df['Weight'] = 100 / df['Permeability'].replace(0, np.nan)

            # --- Apply Weights to Temporal Columns ---
            # Identify target columns for expansion (typically hourly counts from the 3rd column onwards)
            # We exclude metadata and the newly created calculation columns
            exclude_metadata = set(REQUIRED_COLS) | {'Weight', 'Permeability'}
            target_cols = [col for col in df.columns[2:] if col not in exclude_metadata]

            for col in target_cols:
                # Multiply hourly raw counts by the expansion weight
                df[col] = pd.to_numeric(df[col], errors='coerce') * df['Weight']

            # Drop temporary Weight/Permeability if only weighted counts are needed
            # df.drop(columns=['Weight', 'Permeability'], inplace=True)

            # Save the expanded mobility data
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            print(f"Successfully processed: {filename}")

        except Exception as e:
            print(f"Processing failed for {filename}: {e}")

print("-" * 30)
print("Batch processing for population weighting completed.")