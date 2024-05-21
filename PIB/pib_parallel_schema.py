import os
import json

def convert_json(json_data, doc_id):
    new_json = {
        "doc_id": doc_id,
        "source": "PIB",
        "lang_list": [],
        "data": [],
        "meta_data": {}  
    }

    # Process the "Main_PRID" language
    main_language = json_data["Main_PRID_Language"].lower()[:3]
    main_text = json_data["Main_PRID_Text"]

    new_json["data"].append({
        "language": main_language,
        "text": main_text
    })

    new_json["lang_list"].append(main_language)
    new_json["meta_data"][main_language] = {"PRID": str(int(json_data["Main_PRID"]))}  

    # Process the "Languages" group
    for language_data in json_data["Languages"]:
        language = language_data["Language"].lower()[:3]
        text = language_data["Text"]

        new_json["data"].append({
            "language": language,
            "text": text
        })

        new_json["lang_list"].append(language)
        new_json["meta_data"][language] = {"PRID": str(int(language_data["Language_PRID"]))}  

    return new_json

def process_directory(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    json_file_count = 0

    for root, dirs, files in os.walk(input_directory):
        for file_name in files:
            if file_name.endswith(".json"):
                json_file_count += 1

                file_path = os.path.join(root, file_name)

                with open(file_path, 'r', encoding='utf-8') as file:
                    json_data = json.load(file)

                doc_id = json_file_count
                new_json_data = convert_json(json_data, doc_id)

                new_file_name = f"{doc_id}.json"
                new_file_path = os.path.join(output_directory, new_file_name)

                with open(new_file_path, 'w', encoding='utf-8') as new_file:
                    json.dump(new_json_data, new_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    input_directory = "/home/mtech_22/sanjay/pib_final"
    output_directory = "/home/mtech_22/sanjay/PIB/pib_schema_final" 
    process_directory(input_directory, output_directory)
