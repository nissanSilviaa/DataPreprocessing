import pandas as pd

# Load the CSV file into a DataFrame
file_path = 'P2Dropped.csv'  # Replace with your actual file path
df = pd.read_csv(file_path)

# Drop the specified columns
columns_to_drop = ['Action_Type', 'Activity_Type', 'Knife_Sharpness']
df = df.drop(columns=columns_to_drop)

# Optionally, save the modified DataFrame back to a new CSV file
output_file_path = 'modified_data.csv'  # Replace with your desired output file name
df.to_csv(output_file_path, index=False)

print("Columns deleted and data saved to", output_file_path)
