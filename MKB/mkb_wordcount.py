import os
import json

def count_words_and_languages(json_file_path):
    """
    Counts the words in the "text" elements and aggregates counts by language.
    
    Parameters:
    - json_file_path: Path to the JSON file.
    
    Returns:
    - A tuple containing the total word count and a dictionary of word counts by language.
    """
    total_word_count = 0
    word_count_by_language = {}
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            
            if "data" in json_data and isinstance(json_data["data"], list):
                for item in json_data["data"]:
                    if "text" in item and "language" in item and isinstance(item["text"], str):
                        word_count = len(item["text"].split())
                        total_word_count += word_count
                        
                        # Increment count for the specific language
                        language = item["language"]
                        if language in word_count_by_language:
                            word_count_by_language[language] += word_count
                        else:
                            word_count_by_language[language] = word_count
    except Exception as e:
        print(f"Error reading {json_file_path}: {e}")

    return total_word_count, word_count_by_language

def main(directory):
    grand_total_word_count = 0
    grand_total_word_count_by_language = {}
    json_file_count = 0  # Initialize counter for JSON files
    
    with open("wordcount_mkb.txt", "w", encoding='utf-8') as output_file:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    json_file_count += 1  # Increment JSON file counter
                    full_path = os.path.join(root, file)
                    word_count, word_count_by_language = count_words_and_languages(full_path)
                    
                    output_file.write(f"{file}: {word_count} words\n")
                    
                    grand_total_word_count += word_count
                    
                    for language, count in word_count_by_language.items():
                        if language in grand_total_word_count_by_language:
                            grand_total_word_count_by_language[language] += count
                        else:
                            grand_total_word_count_by_language[language] = count
        
        output_file.write(f"\nTotal JSON files processed: {json_file_count}\n")
        output_file.write(f"Total word count across all files: {grand_total_word_count}\n")
        
        output_file.write("\nWord count by language:\n")
        for language, count in grand_total_word_count_by_language.items():
            output_file.write(f"{language}: {count}\n")

if __name__ == "__main__":
    directory = "/home/sanjay/MKB/mkb_schema_final" 
    main(directory)
