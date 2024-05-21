# USING "langdetect" TO GET THE MAIN_PRID LANGUAGE AND UPDATE IN THE SAME .json FILE

import os
import json
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

def process_json_file(json_data):
    main_prid_text = json_data.get("Main_PRID_Text", "")
    language = detect_language(main_prid_text)
    
    # Check if "Main_PRID_Language" key is present
    if "Main_PRID_Language" in json_data:
        json_data["Main_PRID_Language"] = language

def detect_language(text):
    try:
        # Attempt to detect language
        lang_code = detect(text)
        
        # Map language code to language name
        lang_name = lang_code_to_name(lang_code)
        
        return lang_name
    except LangDetectException:
        # Handle exceptions, e.g., if text is too short
        return "Unknown"

def lang_code_to_name(code):
    # Language mapping for Indian languages
    indian_language_mapping = {
        "en": "English",
        "bn": "Bengali",
        "gu": "Gujarati",
        "hi": "Hindi",
        "kn": "Kannada",
        "ml": "Malayalam",
        "mr": "Marathi",
        "ne": "Nepali",
        "pa": "Punjabi",
        "ta": "Tamil",
        "te": "Telugu",
        "ur": "Urdu",
    }
    return indian_language_mapping.get(code, "Unknown")


def process_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    json_data = json.load(json_file)
                    process_json_file(json_data)
                    
                    # Save the modified JSON back to the file
                    with open(file_path, 'w', encoding='utf-8') as updated_json_file:
                        json.dump(json_data, updated_json_file, indent=4, ensure_ascii=False)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in {file_path}: {e}")
                continue

if __name__ == "__main__":
    directory_path = "/home/mtech_22/sanjay/pib_final"

    process_directory(directory_path)
    print("Language detection and modification completed.")