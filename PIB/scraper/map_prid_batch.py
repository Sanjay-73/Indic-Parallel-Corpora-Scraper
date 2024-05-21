import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def extract_PRID_and_language(url):
    try:
        response = requests.get(url, timeout=(15, 30))  # Adjust timeout here
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            release_lang_div = soup.find("div", class_="ReleaseLang")
            if release_lang_div:
                language_tags = release_lang_div.find_all("a")
                prid_language_dict = {}
                for language_tag in language_tags:
                    language = language_tag.text.strip()
                    prid = re.search(r"PRID=(\d+)", str(language_tag))
                    if prid:
                        prid_language_dict[prid.group(1)] = language
                return prid_language_dict
    except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
        print(f"Timeout occurred for URL: {url} - Error: {e}")
    return None

def main(start_prid, end_prid):
    start_time = time.time()
    base_url = "https://pib.gov.in/PressReleasePage.aspx?PRID="

    data = {
        "Main_PRID": [],
        "Language": [],
        "Extracted_PRID": [],
        "Extracted_Language": [],
    }
    all_extracted_PRIDs = set()
    failed_PRIDs = set()

    for prid in range(start_prid, end_prid + 1):
        prid = str(prid)
        if prid in all_extracted_PRIDs:
            continue

        url = f"{base_url}{prid}"
        try:
            response = requests.get(url, timeout=(15, 30))  # Adjust timeout here

            if response.status_code == 200:
                extracted_PRIDs = extract_PRID_and_language(url)
                if extracted_PRIDs is not None:
                    main_language = extracted_PRIDs.get(prid)  # Language of main PRID
                    for extracted_prid, extracted_language in extracted_PRIDs.items():
                        data["Main_PRID"].append(prid)
                        data["Language"].append(
                            main_language if main_language else "NaN"
                        )
                        data["Extracted_PRID"].append(extracted_prid)
                        data["Extracted_Language"].append(extracted_language)

                        all_extracted_PRIDs.add(extracted_prid)
                        all_extracted_PRIDs.add(prid)
                else:
                    data["Main_PRID"].append(prid)
                    data["Language"].append("NaN")
                    data["Extracted_PRID"].append("NaN")
                    data["Extracted_Language"].append("NaN")
            else:
                data["Main_PRID"].append(prid)
                data["Language"].append("NaN")
                data["Extracted_PRID"].append("NaN")
                data["Extracted_Language"].append("NaN")
            all_extracted_PRIDs.add(prid)

        except requests.exceptions.Timeout:
            print(f"Connection timeout for PRID: {prid}.")
            failed_PRIDs.add(prid)
        except requests.exceptions.RequestException as e:
            print(f"Request exception for PRID: {prid} - Error: {e}")
            failed_PRIDs.add(prid)

    if failed_PRIDs:
        with open(f"failed_PRIDs_{start_prid}.txt", "w") as file:
            file.write("\n".join(failed_PRIDs))

    pd.DataFrame(data).to_csv(f"extracted_PRIDs_{start_prid}.csv", index=False)

    end_time = time.time()
    print(end_time - start_time)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process PRID range")
    parser.add_argument("start_prid", type=int, help="Start PRID")
    parser.add_argument("end_prid", type=int, help="End PRID")
    args = parser.parse_args()

    print("starting new batch")
    main(args.start_prid, args.end_prid)