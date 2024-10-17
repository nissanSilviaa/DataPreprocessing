import pandas as pd
import re

# Load your dataset into a DataFrame
file_path = 'modified_data.csv'  # Replace with your actual file path
df = pd.read_csv(file_path)

# Function to remove letters and spaces from the Action_Type column
def clean_action_type(action):
    # Use regular expression to extract only digits
    return re.sub(r'\D', '', str(action))

# Clean the Action_Type column
df['Action_Type'] = df['Action_Type'].apply(clean_action_type)

# Replace values in Activity_Type column
activity_mapping = {'Boning': 0, 'Slicing': 1}
df['Activity_Type'] = df['Activity_Type'].replace(activity_mapping)

# Replace values in Knife_Sharpness column
knife_sharpness_mapping = {'Blunt': 0, 'Medium': 1, 'Sharp': 2}
df['Knife_Sharpness'] = df['Knife_Sharpness'].replace(knife_sharpness_mapping)

# Save the cleaned DataFrame to a new CSV
output_file_path = 'MainP2_CF.csv'
df.to_csv(output_file_path, index=False)

print(f"Data cleaned and saved to {output_file_path}")
