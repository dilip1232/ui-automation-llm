import json
import os

CLASSIFIED_FEATURES_FILE = "classified_features.json"
TEST_CASE_FILE = "test_appium.py"

# Conversational test steps
CONVERSATIONAL_TESTS = [
    "Click on the 'Sign up free' button.",
    "Enter 'testuser' in the username field.",
    "Enter 'mypassword' in the password field.",
    "Click on the 'Log in' button.",
    "Scroll down to find 'Millions of songs. Free on Spotify.'.",
    "Verify if the version label is displayed."
]

def load_classified_elements():
    """Load UI elements from JSON."""
    if not os.path.exists(CLASSIFIED_FEATURES_FILE):
        print(f"Error: {CLASSIFIED_FEATURES_FILE} not found!")
        return []

    with open(CLASSIFIED_FEATURES_FILE, "r") as f:
        return json.load(f)

def find_matching_element(text, elements):
    """Find a matching UI element, prioritizing resource_id, then text."""
    for element in elements:
        # Check if text in the element matches
        if text.lower() in element.get("text", "").lower():
            if element.get("resource_id") and element["resource_id"] != "null":  # Check for resource_id first
                return element["resource_id"], "id"  # Return resource_id and locator type
            elif element.get("text"):
                return element["text"], "text"  # Fallback to text if resource_id is null
    return None, None  # Return None, None if no match

def generate_appium_action(test_step, by_strategy, locator):
    """Generates the appropriate Appium action based on the test step."""

    if "click" in test_step.lower():
        return f'element = wait.until(EC.presence_of_element_located(({by_strategy}, "{locator}")))\n        element.click()'
    elif "enter" in test_step.lower():
        text_to_enter = test_step.split("'")[1] if "'" in test_step else ""  # Handle enter without text
        return f'element = wait.until(EC.presence_of_element_located(({by_strategy}, "{locator}")))\n        element.send_keys("{text_to_enter}")'
    elif "verify" in test_step.lower() and "displayed" in test_step.lower():
        return f'element = wait.until(EC.presence_of_element_located(({by_strategy}, "{locator}")))\n        assert element.is_displayed()'
    elif "scroll down" in test_step.lower():
        return f'# Implement Scroll Down logic if needed'  # Placeholder for scroll down
    elif "get text" in test_step.lower():
        return f'element = wait.until(EC.presence_of_element_located(({by_strategy}, "{locator}")))\n        text = element.text\n        print(f"Text of element: {{text}}")'
    # ... other actions

    return None  # Return None if no action is defined


def generate_test_script(conversational_tests, elements):
    test_script = """from scripts.appium_driver import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_app():
    driver = get_driver()
    wait = WebDriverWait(driver, 10)

"""

    step_num = 1
    for test in conversational_tests:
        text_in_command = test.split("'")[1] if "'" in test else test

        identifier, locator_type = find_matching_element(text_in_command, elements)

        if not identifier:
            print(f"⚠️ Skipping test step (no matching UI element): {test}")
            continue

        if locator_type == "id":
            by_strategy = "By.ID"
            locator = identifier
        elif locator_type == "text":  # Use exact text match for XPath
            by_strategy = "By.XPATH"
            locator = f"//android.widget.Button[@text='{identifier}']"  # Example for Button - adapt for other types

        action = generate_appium_action(test, by_strategy, locator)

        if action:
            test_script += f"""
    # Step {step_num}: {test}
    try:
        {action}
        print("✅ {test}")
    except Exception as e:
        print("Failed: {test} -", str(e))
"""
        else:
            print(f"⚠️ No Appium action defined for test step: {test}")

        step_num += 1

    test_script += """
    driver.quit()

if __name__ == "__main__":
    test_app()
"""

    with open(TEST_CASE_FILE, "w") as f:
        f.write(test_script)

    print(f"✅ Python Appium test script generated: {TEST_CASE_FILE}")


def main():
    elements = load_classified_elements()
    if not elements:
        print("⚠️ No UI elements found for test generation.")
        return

    generate_test_script(CONVERSATIONAL_TESTS, elements)


if __name__ == "__main__":
    main()
