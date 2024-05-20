#Main parallel data scraper code
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Language mapping dictionary with language indices and their respective names
language_mapping = {
    1: "English",
    2: "Hindi",
    3: "Assamese",
    4: "Bengali",
    5: "Gujarati",
    6: "Kannada",
    7: "Malayalam",
    8: "Manipuri",
    9: "Marathi",
    10: "Odia",
    11: "Punjabi",
    12: "Tamil",
    13: "Telugu",
    14: "Urdu",
}

# Configuring Chrome WebDriver with headless option and user agent
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

driver = webdriver.Chrome(options=chrome_options)  # Initialize the WebDriver

try:
    read_urls = []
    with open("read_links.txt", "r") as file:
        read_urls = file.read().splitlines()  # Read URLs from a text file

    output_folder = "/home/sanjay/MKB/mkb_data"  # Output folder path

    for idx, read_url in enumerate(read_urls, start=1):
        print(f"Processing URL {idx} of {len(read_urls)}")
        driver.get(read_url)  # Open the web page for each URL

        all_articles_data = []

        for language_index in range(1, 15):
            try:
                language_selector = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "#lang_choice_polylang-2")
                    )
                )
                language_selector.click()  # Click the language selector dropdown

                other_language_option = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.CSS_SELECTOR,
                            f"#lang_choice_polylang-2 option:nth-child({language_index})",
                        )
                    )
                )
                other_language_option.click()  # Select a language option

                try:
                    confirmation_popup = WebDriverWait(driver, 5).until(
                        EC.alert_is_present()
                    )
                    confirmation_popup.accept()  # Accept any confirmation popups
                except Exception as e:
                    pass  # Ignore exceptions from popups

                current_url = driver.current_url

                title_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div.content-block.clearfix > h2")
                    )
                )
                title = title_element.text  # Extract the title from the page

                # Code to extract video URL and article content

                if any([title, video_url, article]):
                    language_name = language_mapping.get(language_index, "Unknown")
                    article_data = {
                        "read_url": read_url, 
                        "language_url": current_url,  
                        "language_index": language_index,
                        "language_name": language_name,
                        "title": title,
                        "video_url": video_url,
                        "article": article,
                    }
                    all_articles_data.append(article_data)  # Store the collected data

            except Exception as e:
                pass  # Ignore exceptions in language selection or data extraction

        output_file = os.path.join(output_folder, f"articles_data_{idx}.json")
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(all_articles_data, json_file, ensure_ascii=False, indent=4)  # Write data to JSON file

except Exception as e:
    pass  # Ignore exceptions during URL processing

finally:
    driver.quit()  # Ensure the WebDriver is closed properly