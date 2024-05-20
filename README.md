# Indic Parallel Corpora Scraper

The Indic Parallel Corpora Scraper is a tool tailored for extracting parallel corpora from various Indian websites, including government portals, news outlets, and tourism sites. This tool meticulously gathers aligned text segments across multiple Indian languages, which are essential for training Neural Machine Translation (NMT) models. By leveraging the capabilities of BeautifulSoup and Selenium, the scraper effectively navigates and extracts content from both static and dynamic web pages, ensuring comprehensive and reliable datasets for linguistic research and development.

## Parallel Data Schema Definition
The structure of the data stored in our JSON files has been meticulously designed to align with the standards set forth by the WMT23 German-English document-level translation task. This schema ensures compatibility and relevance for contemporary NMT model training requirements.

- **doc_id**: A SHA1 hash code of the English text, uniquely identifying each document.
- **source**: The origin or source of the document.
- **lang_list**: A list of languages in which the text content is available.
- **data**: Language-specific text content.
- **meta_data**: Additional language-specific attributes that may include annotations or contextual information.
 
