# Mann Ki Baat (MKB)
Developed a sophisticated web scraper utilizing Selenium WebDriver to systematically gather content from the Mann Ki Baat (MKB) website. This dynamic scraper adeptly navigates through article links, selects content across 14 languages from dropdown menus, and handles various web page interactions, ensuring the comprehensive acquisition of diverse data.

Implemented robust logic to extract essential metadata from each webpage, including article titles, video URLs, and complete article texts. This organized data, categorized by language, facilitates structured and accessible data analysis, simplifies downstream processing, and enables detailed comparative linguistic analysis for generating high-quality parallel datasets.

Optimized the scraping script for efficiency by executing it in headless mode, minimizing resource consumption, and accelerating data collection. This streamlined approach not only enhances access to valuable multilingual content but also lays the groundwork for in-depth linguistic and semantic analysis across languages.

Enhanced multilingual text datasets by incorporating language detection capabilities using the langdetect library. Each article's language is identified and updated with ISO 639-1 language codes, ensuring standardized language tagging for improved dataset management and reference.

Developed a post-procurement script to standardize JSON file structures according to a unified parallel schema, as defined earlier. Additionally, unique SHA-1 hash codes were generated for each article, serving as distinct identifiers for efficient data management and reference.

## Stats
→ 107 articles in the form of .json files

→ Total word count across all files: 4,812,156

→ Word count by language:
- eng: 402,571
- hin: 412,090
- ass: 346,536
- ben: 322,627
- guj: 358,325
- kan: 279,209
- mal: 253,702
- man: 315,771
- mar: 327,190
- odi: 349,099
- pun: 416,482
- tam: 311,591
- tel: 288,562
- urd: 428,401
