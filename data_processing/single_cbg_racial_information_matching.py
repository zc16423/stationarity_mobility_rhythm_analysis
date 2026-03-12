import pandas as pd
import os

def update_race_column(reference_file):
    """
    Update the 'Race' column in the reference demographic CSV based on majority population thresholds.
    Race codes: 1=White, 2=Hispanic, 3=Black, 4=Other/Unknown (default).
    """
    try:
        df = pd.read_csv(reference_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(reference_file, encoding='latin1')
    
    df['Race'] = 4  # Default race code is 4 (Other/Unknown)
    df.loc[df['pct_NH_White_alone_ACS_15_19'] >= 50, 'Race'] = 1
    df.loc[df['pct_Hispanic_ACS_15_19'] >= 50, 'Race'] = 2
    df.loc[df['pct_NH_Blk_alone_ACS_15_19'] >= 50, 'Race'] = 3

    df.to_csv(reference_file, index=False, encoding='utf-8')
    print(f"Reference file '{reference_file}' updated with 'Race' column.")

def process_od_files(folder_path, reference_file):
    """
    For each CSV file in the OD folder, merge 'Race' information from the reference file
    and insert it as the second column (after 'origin_census_block_group').
    """
    try:
        reference_df = pd.read_csv(reference_file, encoding='utf-8')
    except UnicodeDecodeError:
        reference_df = pd.read_csv(reference_file, encoding='latin1')
    
    files_processed = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            csv_file = os.path.join(folder_path, filename)
            try:
                csv_df = pd.read_csv(csv_file, encoding='utf-8')
            except UnicodeDecodeError:
                csv_df = pd.read_csv(csv_file, encoding='latin1')
            
            # Merge with reference dataframe on Census Block Group ID
            merged_df = pd.merge(csv_df, reference_df[['GIDBG', 'Race']], 
                                 left_on='origin_census_block_group', right_on='GIDBG', how='left')
            
            # Remove existing 'Race' column to avoid duplicates
            if 'Race' in csv_df.columns:
                csv_df.drop(columns=['Race'], inplace=True)
            
            # Insert 'Race' as second column
            csv_df.insert(1, 'Race', merged_df['Race'])
            csv_df.to_csv(csv_file, index=False, encoding='utf-8')
            print(f"Processed file '{filename}' saved.")
            files_processed += 1

    print(f"All files processed. Total {files_processed} files updated.")

if __name__ == "__main__":
    reference_file_path = r"D:\Desktop\USA_CBG_race_data.csv"
    od_folder_path = r"D:\Desktop\2019_mobility_data"
    
    update_race_column(reference_file_path)
    process_od_files(od_folder_path, reference_file_path)
