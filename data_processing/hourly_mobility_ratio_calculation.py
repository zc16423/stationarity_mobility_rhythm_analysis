import os
import pandas as pd

def process_csv_files(input_folder, output_folder):
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
    
    for file in csv_files:
        data = pd.read_csv(os.path.join(input_folder, file))
        
        # Keep required columns (make sure device_count is also loaded)
        data = data[['origin_census_block_group', 'at_home_by_each_hour', 'device_count']]
        
        # Define a function to expand JSON string into separate hourly columns
        def expand_json(row):
            at_home_data = eval(row)  # Convert JSON string to list; assumes correct and safe format
            hour_columns = {}
            for hour in range(1, 25):
                hour_columns[f'{hour}:00'] = at_home_data[hour - 1]
            return pd.Series(hour_columns)
        
        expanded_data = data['at_home_by_each_hour'].apply(expand_json)
        
        # Divide each hourly value by device_count, row-wise to avoid division by zero
        for hour_col in expanded_data.columns:
            expanded_data[hour_col] = expanded_data[hour_col] / data['device_count']
        
        # Combine original census block group and processed 24 hourly columns
        final_data = pd.concat([data['origin_census_block_group'], expanded_data], axis=1)
        
        # Save the result to output folder
        output_file = os.path.join(output_folder, file)
        final_data.to_csv(output_file, index=False)
        
        print(f"File {file} processed successfully and saved to {output_file}")

    print(f"All files in folder {input_folder} have been processed.")

if __name__ == "__main__":
    input_folder = r"D:\Desktop\2019_mobility_data"
    output_folder = r"D:\Desktop\calculation_result"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    process_csv_files(input_folder, output_folder)

    print("All files processed.")
