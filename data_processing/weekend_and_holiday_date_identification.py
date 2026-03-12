import pandas as pd
import os

# Folder path containing CSV files
source_folder = r"D:\Desktop\fitting_results"

# US Federal Holidays for 2019
filter_dates_2019 = [
    '2019/1/1',    # New Year's Day
    '2019/1/21',   # Martin Luther King Jr. Day
    '2019/2/18',   # Presidents' Day
    '2019/5/27',   # Memorial Day
    '2019/7/4',    # Independence Day
    '2019/9/2',    # Labor Day
    '2019/10/14',  # Columbus Day
    '2019/11/11',  # Veterans Day
    '2019/11/28',  # Thanksgiving Day
    '2019/12/25'   # Christmas Day
]

# US Federal Holidays for 2020
filter_dates_2020 = [
    '2020/1/1',    # New Year's Day
    '2020/1/20',   # Martin Luther King Jr. Day
    '2020/2/17',   # Presidents' Day
    '2020/5/25',   # Memorial Day
    '2020/7/4',    # Independence Day
    '2020/9/7',    # Labor Day
    '2020/10/12',  # Columbus Day
    '2020/11/11',  # Veterans Day
    '2020/11/26',  # Thanksgiving Day
    '2020/12/25'   # Christmas Day
]

# Convert to datetime objects
filter_dates_2019 = pd.to_datetime(filter_dates_2019, format='%Y/%m/%d')
filter_dates_2020 = pd.to_datetime(filter_dates_2020, format='%Y/%m/%d')

# Process each CSV file in the folder
for root, dirs, files in os.walk(source_folder):
    for file_name in files:
        if file_name.endswith(".csv"):
            file_path = os.path.join(root, file_name)

            # Read CSV
            df = pd.read_csv(file_path)

            # Ensure 'Date' column is datetime
            df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d', errors='coerce')

            # Filter out holidays
            df = df[~df['Date'].isin(filter_dates_2019)]
            df = df[~df['Date'].isin(filter_dates_2020)]

            # Filter out weekends
            df = df[(df['Day of Week'] != 'Saturday') & (df['Day of Week'] != 'Sunday')]

            # Overwrite the file with the filtered data
            df.to_csv(file_path, index=False)