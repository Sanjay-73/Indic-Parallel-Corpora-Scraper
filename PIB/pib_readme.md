# Press Information Bureau (PIB)

Introducing parallelism into the previously scraped data from the [Press Information Bureau (PIB)](https://pib.gov.in/indexd.aspx), which was overlooked during the initial scraping process. The primary objective was to create a system that could efficiently handle and create mappings for multiple languages associated with each press release.

The approach involved dynamically altering the PRIDs https://pib.gov.in/PressReleasePage.aspx?PRID=XXXXXX within the [URL](https://pib.gov.in/PressReleasePage.aspx?PRID=190000) in the code and generating a CSV file structured with `Main_PRID` and `Main_PRID_Language` entries. As each press release encompassed multiple languages, each associated with a unique PRID, I systematically navigated through each language on the webpage. For every language encountered, we extracted its corresponding PRID and incorporated it into the CSV as `Child_PRID` along with its respective `Child_PRID_Language`.

## Challenges

1. **Language Detection for `Main_PRID`**:
   - The `Main_PRID` lacks explicit language indication on the page.
   - Unlike other languages where language information is embedded within the link names below the article, retrieving the corresponding `Main_PRID_Language` directly from the page was not feasible.

2. **Extraction Failures**:
   - Connectivity issues resulted in timeout errors.
   - Unstable network connections or server unresponsiveness disrupted the data retrieval process.

3. **Duplicate PRIDs**:
   - The iterative nature of updating PRIDs led to duplicates, as the `Child_PRID` may eventually coincide with a `Main_PRID`.

4. **Range of PRIDs**:
   - Extracting PRIDs within the range of 147983 to 1963000 proved challenging due to server constraints and high computational demands.

## Solutions

1. **Language Detection for Main_PRID**:
   - Utilized the `langdetect` library to detect the language of `Main_PRID` text.
   - Mapped the detected language code to its corresponding name and updated the JSON data under the `Main_PRID_Language` key.

2. **Handling Duplicate PRIDs**:
   - Maintained a set named `all_extracted_PRIDs` to track processed or extracted PRIDs.
   - Skipped duplicates by checking if the current `PRID` is already in the `all_extracted_PRIDs` set.

3. **Error Logging**:
   - Logged every URL fetch attempt, capturing successful and failed retrievals.
   - Stored failed PRIDs in `failed_PRIDs` for manual review and processing later.

4. **Parallel Processing**:
   - Leveraged Python's `ThreadPoolExecutor` from the `concurrent.futures` module for asynchronous web scraping.
   - Configured the executor with `max_workers=10` for balanced system utilization.
   - Implemented a batch processing approach using a bash script to divide the range of PRIDs into ten batches, running the scraper in parallel.

## Features

1. **Parallel Processing with `ThreadPoolExecutor`**:
   - Used `ThreadPoolExecutor` to distribute tasks across multiple threads.
   - The primary function, `process_prid`, constructs URLs, fetches web pages, and parses HTML content to extract PRIDs and languages.
   - Introduced improvements like thread safety, rate-limiting strategies, and robust error handling.

2. **Batch Processing with Bash Script**:
   - Divided the PRID range into batches and executed the Python script for each batch concurrently.
   - Optimized data extraction by running each batch simultaneously in the background.

3. **Mapping PRIDs to Languages**:
   - Created mappings where the `Main_PRID` links to subsequent `Child_PRID`s.
   - Updated the CSV file with extracted file paths, facilitating parallel mapping.

4. **Schema Integration**:
   - Developed a code to extract "text" from the file paths and integrate it into the JSON format.
   - Included available metadata for each PRID, adhering to the predefined schema.
