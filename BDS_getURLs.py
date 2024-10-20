from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from collections import defaultdict
import re  # Import re for regex
from group_properties import group_properties  # Import the grouping function

app = FastAPI()

def load_urls(filename='urls.json'):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['urls']

def load_existing_properties(filename='all_properties.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist

def is_duplicate(new_property, existing_properties):
    # Check for duplicates by comparing specific fields (e.g., title, price, location)
    for existing_property in existing_properties:
        if (new_property.get('title') == existing_property.get('title') and
            new_property.get('price') == existing_property.get('price') and
            new_property.get('area') == existing_property.get('area') and
            new_property.get('location') == existing_property.get('location')):
            return True
    return False

def extract_road_info(road_text):
    # Use regex to extract the part that starts with "Đường" and ends before the next comma
    match = re.search(r'Đường [^,]+', road_text)
    if match:
        return match.group(0)  # Return the matched road name, e.g., "Đường Kim Giang"
    return road_text

def get_road_info(driver, detail_url):
    # Open a new tab for the detail page
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab

    driver.get(detail_url)
    time.sleep(3)  # Wait for the page to load

    try:
        road_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".re__pr-short-description"))
        )
        full_address = road_element.text
        road_info = extract_road_info(full_address)
    except Exception as e:
        print(f"Error fetching road info for {detail_url}: {e}")
        road_info = "N/A"

    # Close the tab and switch back to the main window
    driver.close()
    driver.switch_to.window(driver.window_handles[0])  # Go back to the original tab

    return road_info

@app.get("/scrape")
def scrape_property_details():
    urls = load_urls()  # Load the list of URLs from the JSON file
    all_properties = load_existing_properties()  # Load existing properties
    new_properties = []  # List to store new properties

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Loop through url
    for url in urls:
        driver.get(url)

        # Wait a bit to ensure the page loads completely
        time.sleep(5)

        # List to store data for each page
        properties = []

        # Find all property containers
        property_containers = driver.find_elements(By.CSS_SELECTOR, ".re__card-config.js__card-config")
        # info_containers = driver.find_elements(By.CSS_SELECTOR, ".re__card-info")  # New block

        # Extract data from the first type of containers (previous block)
        for container in property_containers:
            data = {}
            
            try:
                price_element = container.find_element(By.CSS_SELECTOR, ".re__card-config-price")
                data['price'] = price_element.text
            except:
                data['price'] = "N/A"

            try:
                area_element = container.find_element(By.CSS_SELECTOR, ".re__card-config-area")
                data['area'] = area_element.text
            except:
                data['area'] = "N/A"

            try:
                price_per_m2_element = container.find_element(By.CSS_SELECTOR, ".re__card-config-price_per_m2")
                data['price_per_m2'] = price_per_m2_element.text
            except:
                data['price_per_m2'] = "N/A"

            try:
                bedrooms_element = container.find_element(By.CSS_SELECTOR, ".re__card-config-bedroom span")
                data['bedrooms'] = bedrooms_element.text
            except:
                data['bedrooms'] = "N/A"

            try:
                toilets_element = container.find_element(By.CSS_SELECTOR, ".re__card-config-toilet span")
                data['toilets'] = toilets_element.text
            except:
                data['toilets'] = "N/A"

            try:
                location_element = container.find_element(By.XPATH, "./following-sibling::div[contains(@class, 're__card-location')]//span")
                data['location'] = location_element.text
            except:
                data['location'] = "N/A"

            # Extract detail page URL and road info
            try:
                detail_link_element = container.find_element(By.XPATH, "../../../../../descendant::a")
                detail_url = detail_link_element.get_attribute('href')
                data['url'] = detail_url
                road_info = get_road_info(driver, detail_url)
                road_info = extract_road_info(road_info)
                data['road'] = road_info
                # print(detail_url)
            except:
                data['road'] = "N/A"
                data['url'] = "N/A"

            properties.append(data)

        # Add new properties to new_properties list if not duplicates
        for property in properties:
            if not is_duplicate(property, all_properties):
                new_properties.append(property)

    # driver.quit()

    # Append new properties to the existing list
    all_properties.extend(new_properties)

    # Save all properties back to all_properties.json
    with open('all_properties.json', 'w', encoding='utf-8') as file:
        json.dump(all_properties, file, ensure_ascii=False, indent=4)

    # Call the grouping function after appending new properties
    group_properties()

    return {
        "message": "Scraping completed",
        "new_properties_count": len(new_properties),
        "total_properties": len(all_properties)
    }