import json
import os
from selenium.webdriver.support import expected_conditions as EC
from scripts.gemini_agent import ask_gemini

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
    """Find a matching UI element."""
    for element in elements:
        if text.lower() in element["text"].lower():
            return element["resource_id"]
    return None


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
        resource_id = find_matching_element(text_in_command, elements)

        if not resource_id:
            print(f"⚠️ Skipping test step (no matching UI element): {test}")
            continue

        test_script += f"""
    # Step {step_num}: {test}
    try:
        element = wait.until(EC.presence_of_element_located((By.ID, "{resource_id}")))
        element.click()
        print("✅ {test}")
    except Exception as e:
        print("❌ Failed: {test} -", str(e))
"""
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
