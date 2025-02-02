import json
import os
from openai_agent import ask_openai

UI_ELEMENTS_FILE = "ui_elements.json"
CLASSIFIED_FEATURES_FILE = "classified_features.json"

def load_ui_elements():
    if not os.path.exists(UI_ELEMENTS_FILE):
        print(f"Error: {UI_ELEMENTS_FILE} not found!")
        return []
    with open(UI_ELEMENTS_FILE, "r") as f:
        return json.load(f)

def classify_element(element):
    prompt = f"""
Given the following Android UI element details, classify its priority:

- Class: {element.get('class', 'N/A')}
- Text: {element.get('text', 'N/A')}
- Resource ID: {element.get('resource_id', 'N/A')}
- Content Description: {element.get('content_desc', 'N/A')}
- Clickable: {element.get('clickable', 'N/A')}
- Enabled: {element.get('enabled', 'N/A')}

Return ONLY one of: 'P0' if the element is critical for app functionality, or 'P1' if it is important but not critical.
Do not include any additional text.
"""
    response = ask_openai(prompt)
    if response not in ["P0", "P1"]:
        print(f"Warning: Unexpected response '{response}'. Defaulting to 'P1'.")
        return "P1"
    return response

def classify_features():
    elements = load_ui_elements()
    if not elements:
        print("No UI elements found to classify.")
        return

    classified_data = []
    for element in elements:
        priority = classify_element(element)
        element["priority"] = priority
        classified_data.append(element)
        print(f"Classified element '{element.get('text') or element.get('resource_id')}' as {priority}.")

    with open(CLASSIFIED_FEATURES_FILE, "w") as f:
        json.dump(classified_data, f, indent=4)
    print(f"Classification completed! Results saved to {CLASSIFIED_FEATURES_FILE}")

if __name__ == "__main__":
    classify_features()
