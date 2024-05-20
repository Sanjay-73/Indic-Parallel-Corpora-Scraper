import os
import json
from langdetect import detect

def detect_language(text):
    # This function takes a string as input and returns the detected language code.
    try:
        detected_language = detect(text)  # Detect the language using the langdetect library
        return detected_language
    except:
        return "undetermined"  # Return 'undetermined' if the language detection fails

def update_languages(json_file):
    # This function updates the language field in a given JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for article in data:
        if "text" in article:
            text = article["text"]
            detected_language = detect_language(text)  # Detect language of the article text

            # Update the language field with ISO 639-1 code
            article["language"] = detected_language[:2].lower()

    # Save the updated data back to the JSON file
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def update_languages_in_directory(directory):
    # This function iterates over all JSON files in a given directory and updates their language fields
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = os.path.join(directory, filename)
            update_languages(json_file)  # Update each JSON file's language field

if __name__ == "__main__":
    directory_path = "/home/sanjay/MKB/mkb_schema_final"
    update_languages_in_directory(directory_path)