import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

url = "https://sites.google.com/nptel.iitm.ac.in/books/english"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

# Use a webdriver to open the URL and retrieve the dynamic content
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# Wait for the page to load
try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'JNdkSc-SmKAyb'))
    WebDriverWait(driver, 10).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")

# Get the page source after it has loaded
html_content = driver.page_source

# Close the webdriver
driver.quit()

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract information and write to CSV
with open('course_info_english.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Course Name', 'Link'])  # Write header

    for div in soup.find_all('div', class_='JNdkSc-SmKAyb LkDMRd'):
        link_element = div.find('a')
        if link_element:
            link = link_element.get('href', '')

            # Search for "Course :" span, then other spans if not found
            course_name = ''
            course_span = div.find('span', text=lambda t: t and 'Course :' in t)
            if course_span:
                # Extract text after "Course :" (excluding the colon)
                course_name = course_span.get_text(strip=True).split(':', 1)[-1].strip()
            else:
                # If no "Course :" span found, try other spans with a specific style
                spans = div.find_all('span', style=lambda value: value and 'font-size: 12pt' in value.lower())
                for element in spans:
                    if not course_name:
                        course_name = element.get_text(strip=True)

            # Write the information to the CSV file
            csv_writer.writerow([course_name, link])

print("CSV file created successfully.")
