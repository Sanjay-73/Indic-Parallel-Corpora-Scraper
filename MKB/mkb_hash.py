#Code to generate hashcode of the English text generated by the SHA1 algorithm for the 'doc_id' i.e the filename
import os
import json
import hashlib
import csv

# Directory path
directory_path = "/home/sanjay/MKB/mkb_data"

# Function to extract the last number from the filename
def extract_last_number(filename):
    return int(''.join(filter(str.isdigit, filename)))

# Function to calculate the hash value
def calculate_hash(text):
    hash_object = hashlib.sha1(text.encode())
    return hash_object.hexdigest()

# List to store hash codes
hash_codes = []

# Iterate through each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".json"):
        file_path = os.path.join(directory_path, filename)

        # Read JSON file
        with open(file_path, 'r', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)

                # Extract article with "language_name" equal to "English"
                english_articles = [item['article'] for item in data if item.get('language_name') == 'English']

                # Calculate hash value for each article and store in the list
                for article in english_articles:
                    hash_value = calculate_hash(article)
                    hash_codes.append({'filename': filename, 'hash_code': hash_value})

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in {filename}: {str(e)}")

# Sort hash codes based on the last number in the filename
hash_codes.sort(key=lambda x: extract_last_number(x['filename']))

# Save hash codes to a CSV file with updated filenames
csv_file_path = "/home/sanjay/MKB/hash_codes.csv"
with open(csv_file_path, 'w', newline='') as csv_file:
    fieldnames = ['filename', 'hash_code']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write header
    writer.writeheader()

    # Write sorted data with updated filenames
    for idx, hash_entry in enumerate(hash_codes, start=1):
        new_filename = f"articles_data_{idx}.json"
        hash_entry['filename'] = new_filename
        writer.writerow(hash_entry)

print(f"Hash codes saved to {csv_file_path}")