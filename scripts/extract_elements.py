# scripts/extract_elements.py
import time
import json
from appium_driver import get_driver
from selenium.webdriver.common.by import By

def extract_all_elements(driver):
    """Extract all UI elements using a broad XPath query."""
    elements = []
    time.sleep(20)  # Allow time for the app to load
    all_elements = driver.find_elements(By.XPATH, "//*")
    for elem in all_elements:
        try:
            element_info = {
                "resource_id": elem.get_attribute("resource-id"),
                "text": elem.get_attribute("text") or elem.text,
                "class": elem.get_attribute("class"),
                "content_desc": elem.get_attribute("content-desc"),
                "clickable": elem.get_attribute("clickable"),
                "enabled": elem.get_attribute("enabled"),
                "location": elem.location,
                "size": elem.size,
            }
            # Filter out elements without useful information
            if not element_info["resource_id"] and not element_info["text"]:
                continue
            elements.append(element_info)
        except Exception as e:
            print(f"Error processing element: {e}")
    return elements

def save_elements(elements, filename="ui_elements.json"):
    with open(filename, "w") as f:
        json.dump(elements, f, indent=4)
    print(f"Extracted {len(elements)} UI elements to {filename}.")

def main():
    driver = get_driver()
    elements = extract_all_elements(driver)
    save_elements(elements)
    driver.quit()

if __name__ == "__main__":
    main()
