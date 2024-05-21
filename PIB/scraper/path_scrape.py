# CODE TO EXTRACT FILE PATH OF PRIDS (Run on Lab-1)
import os
import json
import csv
import re

def extract_prid_from_url(url):
    prid_match = re.search(r'PRID=(\d{7})', url)
    if prid_match:
        return prid_match.group(1)
    return None

def process_json_files(directory):
    with open('prid_path.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['PRID', 'File Path'])

        for root, _, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.json'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as json_file:
                        try:
                            data = json.load(json_file)
                            if 'URL' in data:
                                url = data['URL']
                                prid = extract_prid_from_url(url)
                                if prid:
                                    csv_writer.writerow([prid, file_path])
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON in file: {file_path}")
                        except KeyError:
                            print(f"Missing required fields in file: {file_path}")

if __name__ == "__main__":
    directory_path = '/mnt/sangraha/govt_websites/Govt_scrape/indian_govt_data/pib/pib_text_files'
    process_json_files(directory_path)