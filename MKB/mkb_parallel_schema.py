#Convert the structure of the scraped data as per the parallel schema definiton
import os
import json

def convert_json(input_path, output_path):
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    for filename in os.listdir(input_path):
        if filename.endswith(".json"):
            # Extract numeric part of the filename
            doc_id_str = ''.join(filter(str.isdigit, filename))
            doc_id = int(doc_id_str)

            with open(os.path.join(input_path, filename), 'r') as file:
                data = json.load(file)
            
            # Initialize the converted structure
            converted_data = {
                "doc_id": doc_id,
                "source": "MKB",
                "lang_list": ["eng", "hin", "asm", "ben", "guj", "kan", "mal", "mni", "mar", "ori", "pan", "tam", "tel", "urd"],
                "data": [],
                "meta_data": {}
            }

            for article in data:
                language_code = article["language_name"][:3].lower()
                text = article["article"]

                converted_data["data"].append({
                    "language": language_code,
                    "text": text
                })

                meta_data = {
                    "language_url": article["language_url"],
                    "title": article["title"],
                    "video_url": article["video_url"]
                }
                converted_data["meta_data"][language_code] = meta_data

            output_filename = os.path.join(output_path, f"{doc_id}.json")
            with open(output_filename, 'w') as output_file:
                json.dump(converted_data, output_file, indent=2)

if __name__ == "__main__":
    input_directory = "/home/sanjay/MKB/mkb_scraped"
    output_directory = "/home/sanjay/MKB/mkb_schema_final"

    convert_json(input_directory, output_directory)