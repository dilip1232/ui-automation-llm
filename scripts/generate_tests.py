import json
import os

CLASSIFIED_FEATURES_FILE = "classified_features.json"
TEST_CASE_FILE = "test_appium.py"

# Define valid locator strategies (excluding Accessibility ID)
VALID_LOCATORS = {
    "ID": "By.ID",
    "XPATH": "By.XPATH",
    "LINK_TEXT": "By.LINK_TEXT",
    "PARTIAL_LINK_TEXT": "By.PARTIAL_LINK_TEXT",
    "NAME": "By.NAME",
    "TAG_NAME": "By.TAG_NAME",
    "CLASS_NAME": "By.CLASS_NAME",
    "CSS_SELECTOR": "By.CSS_SELECTOR"
}

def load_classified_elements():
    """Loads classified UI elements from a JSON file."""
    if not os.path.exists(CLASSIFIED_FEATURES_FILE):
        print(f"Error: {CLASSIFIED_FEATURES_FILE} not found!")
        return []

    with open(CLASSIFIED_FEATURES_FILE, "r") as f:
        return json.load(f)

def get_valid_locator(element):
    """
    Determines the best valid Selenium locator strategy for the given UI element.
    Excludes Accessibility ID since it's not a valid Selenium locator.
    """
    if element.get("resource_id") and element["resource_id"] != "null":
        return VALID_LOCATORS["ID"], element["resource_id"]
    elif element.get("text") and element["text"].strip():
        return VALID_LOCATORS["XPATH"], f"//{element['class']}[@text='{element['text']}']"
    elif element.get("class") and element["class"].strip():
        return VALID_LOCATORS["CLASS_NAME"], element["class"]
    return None, None  # No valid locator found

def generate_appium_action(element):
    """
    Generates an Appium action for the given UI element.
    Uses only valid Selenium locators.
    """
    actions = []
    locator_strategy, locator_value = get_valid_locator(element)

    if not locator_strategy:
        return None  # Skip elements with no valid locator

    clickable = element.get("clickable", "false") == "true"
    
    if clickable:
        actions.append(f'element = wait.until(EC.presence_of_element_located(({locator_strategy}, "{locator_value}")))\n        element.click()')

    if "EditText" in element.get("class", ""):
        actions.append(f'element = wait.until(EC.presence_of_element_located(({locator_strategy}, "{locator_value}")))\n        element.send_keys("sample text")')

    if "TextView" in element.get("class", "") and element.get("text", "").strip():
        actions.append(f'element = wait.until(EC.presence_of_element_located(({locator_strategy}, "{locator_value}")))\n        assert element.is_displayed()')

    return actions

def generate_test_script(elements):
    """Generates an Appium test script based on classified UI elements."""
    test_script = """from scripts.appium_driver import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_app():
    driver = get_driver()
    wait = WebDriverWait(driver, 10)
"""
    
    step_num = 1
    for element in elements:
        priority = element.get("priority", "P1")
        if priority not in ["P0", "P1"]:  # Ignore non-priority elements
            continue

        actions = generate_appium_action(element)
        if not actions:
            continue

        for action in actions:
            test_script += f"\n    try:\n        {action}\n        print('Step {step_num} passed')\n    except Exception as e:\n        print('Step {step_num} failed -', str(e))\n"
        step_num += 1

    test_script += "\n    driver.quit()\n\nif __name__ == '__main__':\n    test_app()\n"

    with open(TEST_CASE_FILE, "w") as f:
        f.write(test_script)

    print(f"Generated Appium test script: {TEST_CASE_FILE}")

def main():
    elements = load_classified_elements()
    if not elements:
        return
    generate_test_script(elements)

if __name__ == "__main__":
    main()
