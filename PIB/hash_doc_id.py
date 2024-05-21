import os
import json
import hashlib

# Directory path
directory_path = "/home/mtech_22/sanjay/PIB/pib_schema_final"

# Function to calculate the hash value
def calculate_hash(text):
    hash_object = hashlib.sha1(text.encode())
    return hash_object.hexdigest()

# Iterate through each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".json"):
        file_path = os.path.join(directory_path, filename)

        # Read JSON file
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # Extract English text
        english_text = next((item['text'] for item in data['data'] if item['language'] == 'eng'), None)

        if english_text:
            # Calculate hash value
            hash_value = calculate_hash(english_text)

            # Update doc_id and create new filename
            data['doc_id'] = hash_value
            new_filename = f"{hash_value}.json"

            # Write updated JSON to new file
            new_file_path = os.path.join(directory_path, new_filename)
            with open(new_file_path, 'w', encoding='utf-8') as new_json_file:
                json.dump(data, new_json_file, ensure_ascii=False, indent=2)

            print(f"Updated doc_id and created new file for {filename}: {hash_value}.json")
        else:
            print(f"No English text found in {filename}")

print("Processing complete.")