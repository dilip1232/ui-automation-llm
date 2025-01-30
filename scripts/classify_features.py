import json
import os
from scripts.gemini_agent import ask_gemini

# Load UI elements extracted from the app
UI_ELEMENTS_FILE = "ui_elements.json"
CLASSIFIED_FEATURES_FILE = "classified_features.json"

def load_ui_elements():
    """Load extracted UI elements from JSON file."""
    if not os.path.exists(UI_ELEMENTS_FILE):
        print(f"Error: {UI_ELEMENTS_FILE} not found!")
        return []

    with open(UI_ELEMENTS_FILE, "r") as f:
        return json.load(f)

def classify_element(element):
    """Use Gemini to classify UI elements as P0 or P1."""
    prompt = f"""
    Classify the following Android UI element as either P0 (critical) or P1 (important but not critical):
    
    Element details:
    - Type: {element.get('type')}
    - Text: {element.get('text', 'N/A')}
    - Resource ID: {element.get('resource_id', 'N/A')}

    Return ONLY 'P0' or 'P1'.
    """

    response = ask_gemini(prompt).strip()
    
    if response not in ["P0", "P1"]:
        print(f"Warning: Unexpected response from Gemini: {response}")
        return "P1"  # Default to P1 if response is invalid
    
    return response

def classify_features():
    """Classify all UI elements and save to JSON."""
    elements = load_ui_elements()
    if not elements:
        print("No UI elements found to classify.")
        return

    classified_data = []

    for element in elements:
        priority = classify_element(element)
        element["priority"] = priority
        classified_data.append(element)
        print(f"Classified: {element['text']} -> {priority}")

    # Save classification results
    with open(CLASSIFIED_FEATURES_FILE, "w") as f:
        json.dump(classified_data, f, indent=4)

    print(f"Classification completed! Saved to {CLASSIFIED_FEATURES_FILE}")

if __name__ == "__main__":
    classify_features()
