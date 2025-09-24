import pandas as pd
import glob

# List to hold data frames
data = []

# Get all CSV file paths
all_files = glob.glob('./2023round*.csv')

# Read each file and append to data list
for file in all_files:
    df = pd.read_csv(file)
    data.append(df)

# Concatenate all data frames into one
combined_df = pd.concat(data, ignore_index=True)

# Find all unique columns
unique_columns = set()
for df in data:
    unique_columns.update(df.columns)

# Save combined data frame to a new CSV file
combined_df.to_csv('2023allrounds.csv', index=False)

# Output unique columns
print("Unique columns:", unique_columns)
