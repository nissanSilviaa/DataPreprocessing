#pip install openpyxl
import pandas as pd
import os


def categorize_sharpness(sharpness_factor):
    if sharpness_factor >= 85:
        return "Sharp"
    elif 70 <= sharpness_factor < 85:
        return "Medium"
    else:
        return "Blunt"


def clean_csv_data(df):
    # get rid of columns with NaN values
    df = df.dropna(how='all', axis=1)
    
    # replace '#REF!' with "none"
    df = df.replace('#REF!', "none")
    
    #flatten tuples
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]
    
    #rename the columns if needed
    df.columns = [col.replace(' ', '_') for col in df.columns]
    
    return df



def load_data(file_path):
    #Load sheets
    segment_velocity = pd.read_excel(file_path, sheet_name='Segment Velocity')
    segment_acceleration = pd.read_excel(file_path, sheet_name='Segment Acceleration')
    
    segment_velocity = clean_csv_data(segment_velocity)
    segment_acceleration = clean_csv_data(segment_acceleration)
    
    return segment_velocity, segment_acceleration

#Save data to CSV files in the output folder
def save_to_csv(segment_velocity, segment_acceleration, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    segment_velocity.to_csv(os.path.join(output_folder, 'Segment_velocity.csv'), index=False)

    segment_acceleration.to_csv(os.path.join(output_folder, 'Segment_acceleration.csv'), index=False)
    
    print(f"Data saved to {output_folder}")

def process_all_files_in_directory(input_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(input_directory, filename)

            sharpness_factor = int(filename.split('-')[3])

            segment_velocity, segment_acceleration = load_data(file_path)
            
            output_folder = os.path.join(input_directory, filename.replace('.xlsx', ''))

            save_to_csv(segment_velocity, segment_acceleration, output_folder)


input_directory = 'P1/Boning'  # Replace with correct path
process_all_files_in_directory(input_directory)
