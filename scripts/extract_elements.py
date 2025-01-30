import time
from appium_driver import get_driver
from selenium.webdriver.common.by import By

def extract_ui_elements(driver):
    """Extract UI elements from the app."""
    # Give time for the app to load
    time.sleep(20)
    
    elements = []

    # Extract Button elements
    buttons = driver.find_elements(By.XPATH, "//android.widget.Button")
    for button in buttons:
        element_info = {
            "resource_id": button.get_attribute("resource-id"),
            "text": button.text,
            "type": "Button",
            "location": button.location,
            "size": button.size
        }
        elements.append(element_info)
    
    # Extract TextView elements
    text_views = driver.find_elements(By.XPATH, "//android.widget.TextView")
    for text_view in text_views:
        element_info = {
            "resource_id": text_view.get_attribute("resource-id"),
            "text": text_view.text,
            "type": "TextView",
            "location": text_view.location,
            "size": text_view.size
        }
        elements.append(element_info)
    
    # Extract EditText elements
    edit_texts = driver.find_elements(By.XPATH, "//android.widget.EditText")
    for edit_text in edit_texts:
        element_info = {
            "resource_id": edit_text.get_attribute("resource-id"),
            "text": edit_text.text,
            "type": "EditText",
            "location": edit_text.location,
            "size": edit_text.size
        }
        elements.append(element_info)
    
    # Extract CheckBox elements
    check_boxes = driver.find_elements(By.XPATH, "//android.widget.CheckBox")
    for check_box in check_boxes:
        element_info = {
            "resource_id": check_box.get_attribute("resource-id"),
            "text": check_box.text,
            "type": "CheckBox",
            "location": check_box.location,
            "size": check_box.size
        }
        elements.append(element_info)
    
    # Extract RadioButton elements
    radio_buttons = driver.find_elements(By.XPATH, "//android.widget.RadioButton")
    for radio_button in radio_buttons:
        element_info = {
            "resource_id": radio_button.get_attribute("resource-id"),
            "text": radio_button.text,
            "type": "RadioButton",
            "location": radio_button.location,
            "size": radio_button.size
        }
        elements.append(element_info)
    
    # Add more element types as needed...

    return elements

def save_elements(elements):
    """Save the extracted elements to a JSON file."""
    import json
    with open("ui_elements.json", "w") as f:
        json.dump(elements, f, indent=4)
    print(f"Extracted {len(elements)} UI elements.")

def main():
    # Get Appium driver
    driver = get_driver()
    
    # Extract UI elements
    elements = extract_ui_elements(driver)
    
    # Save extracted elements to a file
    save_elements(elements)
    
    # Quit the driver after extraction is complete
    driver.quit()

if __name__ == "__main__":
    main()