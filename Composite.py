import numpy as np
import pandas as pd
import os

# Load the CSV file into a DataFrame
df = pd.read_csv('P2clean.csv')

# List of body parts (all prefixes without _x, _y, _z)
body_parts = ['Pelvis', 'L5', 'L3', 'T12', 'T8', 'Neck', 'Head',
              'Right_Shoulder', 'Right_Upper_Arm', 'Right_Forearm', 'Right_Hand',
              'Left_Shoulder', 'Left_Upper_Arm', 'Left_Forearm', 'Left_Hand',
              'Right_Upper_Leg', 'Right_Lower_Leg', 'Right_Foot', 'Right_Toe',
              'Left_Upper_Leg', 'Left_Lower_Leg', 'Left_Foot', 'Left_Toe']

# Create an empty dictionary to store the new columns
composite_columns = {}

# Function to calculate composite features for a body part
def calculate_composites(part):
    x_col = part + '_x'
    y_col = part + '_y'
    z_col = part + '_z'
    
    # 1) RMS of x and y
    composite_columns[f'RMS_{part}_xy'] = np.sqrt((df[x_col]**2 + df[y_col]**2) / 2)
    
    # 2) RMS of y and z
    composite_columns[f'RMS_{part}_yz'] = np.sqrt((df[y_col]**2 + df[z_col]**2) / 2)
    
    # 3) RMS of z and x
    composite_columns[f'RMS_{part}_zx'] = np.sqrt((df[z_col]**2 + df[x_col]**2) / 2)
    
    # 4) RMS of x, y, and z
    composite_columns[f'RMS_{part}_xyz'] = np.sqrt((df[x_col]**2 + df[y_col]**2 + df[z_col]**2) / 3)
    
    # 5) Roll
    composite_columns[f'Roll_{part}'] = 180 * np.arctan2(df[y_col], np.sqrt(df[x_col]**2 + df[z_col]**2)) / np.pi
    
    # 6) Pitch
    composite_columns[f'Pitch_{part}'] = 180 * np.arctan2(df[x_col], np.sqrt(df[y_col]**2 + df[z_col]**2)) / np.pi

# Apply the function to each body part
for part in body_parts:
    calculate_composites(part)

# Convert the dictionary of composite columns into a DataFrame
composite_df = pd.DataFrame(composite_columns)

# Retain Action_Type, Activity_Type, and Knife_Sharpness from the original DataFrame
non_numeric_columns = df[['Action_Type', 'Activity_Type', 'Knife_Sharpness']]

# Concatenate the composite DataFrame with the original DataFrame and the non-numeric columns
df = pd.concat([df, composite_df, non_numeric_columns], axis=1)

# Save the new DataFrame with all features (including non-numeric) to a CSV file
df.to_csv(os.path.join('P2_Composite.csv'), index=False)
