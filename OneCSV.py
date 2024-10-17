import pandas as pd
import os

# Function to clean data
def clean_csv_data(df):
    df = df.dropna(how='all', axis=1)  # Drop columns that are entirely NaN
    df = df.replace('#REF!', "none")   # Replace any '#REF!' errors
    df.columns = [col.replace(' ', '_') for col in df.columns]  # Replace spaces with underscores
    return df

# Function to load data from each file
def load_data(file_path):
    segment_velocity = pd.read_excel(file_path, sheet_name='Segment Velocity')
    markers = pd.read_excel(file_path, sheet_name='Markers')  # Load Markers for activity labels

    segment_velocity = clean_csv_data(segment_velocity)
    markers = clean_csv_data(markers)
    
    return segment_velocity, markers

# Function to map the frame to the corresponding activity label
def map_activity(frame, markers):
    for _, row in markers.iterrows():
        frame_value = row['Frame']
        
        # Check if the frame value is a string and contains a valid range
        if isinstance(frame_value, str) and '-' in frame_value:
            frame_range = frame_value.split('-')
            
            # Check for valid frame ranges (i.e., exactly two values and both are digits)
            if len(frame_range) == 2 and frame_range[0].isdigit() and frame_range[1].isdigit():
                start_frame, end_frame = int(frame_range[0]), int(frame_range[1])
                
                # Map the activity if the frame falls within the range
                if start_frame <= frame <= end_frame:
                    return row['Labelling']  # Return the activity label
    
    # Return None if no valid activity is found
    return None

# Function to categorize knife sharpness based on its value
def categorize_sharpness(sharpness):
    if sharpness >= 85:
        return "Sharp"
    elif 70 <= sharpness < 85:
        return "Medium"
    else:
        return "Blunt"

# Function to combine data from Segment Velocity and assign activity labels and sharpness
def process_file(file_path, activity_type, sharpness_label):
    segment_velocity, markers = load_data(file_path)
    
    # Map activities to the frames
    segment_velocity['Label'] = segment_velocity['Frame'].apply(lambda x: map_activity(x, markers))
    
    # Add the activity type (Boning or Slicing)
    segment_velocity['Activity_Type'] = activity_type
    
    # Add the sharpness label
    segment_velocity['Knife_Sharpness'] = sharpness_label
    
    return segment_velocity

# Function to process all files and combine them into one DataFrame
def process_and_combine_files(input_directory):
    combined_data_list = []
    
    for root, dirs, files in os.walk(input_directory):
        for filename in files:
            if filename.endswith(".xlsx"):
                file_path = os.path.join(root, filename)
                
                # Determine if the file is Boning or Slicing based on its name
                activity_type = "Boning" if "Boning" in filename else "Slicing"
                
                # Extract the sharpness value from the filename (assuming format "MVN-J-Boning-64-001")
                sharpness_value = int(filename.split('-')[3])
                sharpness_label = categorize_sharpness(sharpness_value)
                
                # Process the file and append the data
                combined_data = process_file(file_path, activity_type, sharpness_label)
                combined_data_list.append(combined_data)
    
    # Concatenate all data into a single DataFrame
    final_combined_data = pd.concat(combined_data_list, ignore_index=True) if combined_data_list else pd.DataFrame()
    return final_combined_data

# Function to save the combined data to a CSV
def save_combined_data(final_combined_data, output_directory):
    os.makedirs(output_directory, exist_ok=True)
    final_combined_data.to_csv(os.path.join(output_directory, 'P2Unclean.csv'), index=False)
    print(f"Combined data saved to {os.path.join(output_directory, 'P2Unclean.csv')}")

# Define the input and output directories
input_directory = 'P2'
output_directory = 'Processed_Output'

# Process all files and save the combined data
combined_data = process_and_combine_files(input_directory)
save_combined_data(combined_data, output_directory)
