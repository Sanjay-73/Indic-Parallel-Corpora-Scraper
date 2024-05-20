# Parallel Corpora Scraper

## Overview
The Parallel Corpora Scraper is a robust tool designed to extract parallel data from multiple web pages across various languages. This data, consisting of aligned text segments in different languages, is invaluable for training Neural Machine Translation (NMT) models. The scraper leverages BeautifulSoup and Selenium to navigate and extract content, ensuring compatibility with dynamic web pages.

## Parallel Data Schema Definition
The structure of the data stored in our JSON files has been meticulously designed to align with the standards set forth by the WMT23 German-English document-level translation task. This schema ensures compatibility and relevance for contemporary NMT model training requirements.

- **doc_id**: A SHA1 hash code of the English text, uniquely identifying each document.
- **source**: The origin or source of the document.
- **lang_list**: A list of languages in which the text content is available.
- **data**: Language-specific text content.
- **meta_data**: Additional language-specific attributes that may include annotations or contextual information.

This README file includes all necessary sections for a GitHub repository, providing clear instructions for setting up, using, and contributing to the project. Adjust the content to fit the specific details and configurations of your scraper as needed.
 
