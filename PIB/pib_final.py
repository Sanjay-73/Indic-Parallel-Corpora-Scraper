# FINAL CODE TO EXTRACT TEXT FROM THE FILE PATH AND STORE IN SEPERATE JSON

import pandas as pd
import json
import os
import zipfile
import shutil

# Function to extract text from JSON file
def extract_text(file_path):
    if pd.notnull(file_path) and os.path.exists(str(file_path)):
        with open(str(file_path), 'r') as json_file:
            content = json.load(json_file)
            return content.get('text', '')
    else:
        return ''  # Return an empty string if file path is missing or file doesn't exist

# Path to your CSV file
csv_file_path = '/home/mtech_22/sanjay/PIB/initial_map_modified.csv'
output_directory = '/home/mtech_22/sanjay/pib_final'
zip_file_name = '/home/mtech_22/sanjay/pib_final.zip'

# Read the entire CSV file (remove nrows parameter)
data = pd.read_csv(csv_file_path)

# Create a temporary directory to store JSON files
temp_directory = '/home/mtech_22/sanjay/temp_json'
os.makedirs(temp_directory, exist_ok=True)

# Group data by 'Main_PRID' column
grouped_data = data.groupby('Main_PRID')

# Create separate JSON files for each 'Main_PRID' containing all language texts
for group_name, group_df in grouped_data:
    json_data = {'Main_PRID': group_name, 'Main_PRID_Language': '', 'Main_PRID_Text': '', 'Languages': []}

    # Get unique Language_PRIDs in the group
    unique_language_prids = group_df['Language_PRID'].unique()

    # Extract text for each language within the group
    for language_prid in unique_language_prids:
        language_df = group_df[group_df['Language_PRID'] == language_prid].iloc[0]  # Get the first row for the language
        language_details = {
            'Language': language_df['Language'],
            'Language_PRID': language_df['Language_PRID'],
            'Text': extract_text(language_df['Language_File_Path'])  # Extract text using the provided file path
        }
        json_data['Languages'].append(language_details)

    # Extract and add text associated with Main_PRID
    main_prid_text = extract_text(group_df['Main_File_Path'].iloc[0])
    json_data['Main_PRID_Language'] = ''  # Add an empty element for Main_PRID_Language
    json_data['Main_PRID_Text'] = main_prid_text

    # Write the JSON data to a separate file for the Main_PRID in the temporary directory
    output_file_path = os.path.join(temp_directory, f"data_{group_name}.json")
    with open(output_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

# Create a ZIP file containing all JSON files
with zipfile.ZipFile(zip_file_name, 'w') as zipf:
    for foldername, subfolders, filenames in os.walk(temp_directory):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            zipf.write(file_path, os.path.relpath(file_path, temp_directory))

# Remove the temporary directory and its contents
shutil.rmtree(temp_directory)