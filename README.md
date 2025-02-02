# Automated Appium Test Script and NLP Test Case Generator

## Overview

This project automates the conversion of Appium test scripts into natural language test cases using an LLM (Large Language Model). Additionally, it supports UI element extraction, feature classification, and dynamic test script generation. This allows for seamless testing across different applications without requiring prior knowledge of package names or activities.

## Features

*   **Appium Script to NLP Conversion:** Automatically translates Appium test steps into human-readable test cases.
*   **Dynamic APK-Based Appium Driver:** Detects package name and launches the app dynamically.
*   **UI Element Extraction:** Captures all interactive elements from the app.
*   **Feature Classification:** Uses an LLM to classify UI elements into priority levels (P0 - critical, P1 - important but non-critical).
*   **Test Script Generation:** Generates Appium test scripts based on extracted UI elements.
*   **Emulator and APK Management:** Automates launching the emulator and installing APKs.
*   **Error Handling:** Ensures robustness by handling missing or invalid UI elements.

## Requirements

*   Python 3.x
*   Appium
*   Selenium WebDriver
*   OpenAI API Key (for LLM-based conversion)
*   Android SDK Platform Tools (for emulator and APK management)

## Setup

### 1. **Clone the Repository**

```bash
    git clone <repository_url>
    cd <repository_name>
```

### 2. **Install Dependencies**

```bash
    pip install -r requirements.txt
```

### 3. **Configure API Key**

Create a `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=<your_api_key>
```

Refer to `.env.example` for an example configuration.

### 4. **Ensure Android SDK is Installed**

Ensure you have Android SDK Platform Tools installed and `adb` is available in your system's PATH.

## Running the Workflow

### **1. Start Appium Server**

```bash
    appium
```

### **2. Run Emulator and Install APK**

```bash
    python scripts/emulator.py -a <path_to_your_apk_file.apk>
```

You can use the `-p` flag to specify a custom emulator port. The default is `5554`.

### **3. Extract UI Elements**

```bash
    python scripts/extract_elements.py
```

### **4. Classify UI Elements Using LLM**

```bash
    python scripts/classify_features.py
```

### **5. Generate Appium Test Scripts**

```bash
    python scripts/generate_tests.py
```

### **6. Convert Appium Scripts to Natural Language Test Cases**

```bash
    python scripts/convert_appium_to_nlp.py
```

### **7. Run Generated Tests**

```bash
    python test_appium.py
```

## How It Works

### **1. Extract UI Elements**
The tool extracts UI elements (buttons, text fields, etc.) using Appium and saves them as a JSON file (`ui_elements.json`).

### **2. Classify Features**
Using an LLM, elements are classified into:

- **P0 (Critical)**: Essential features for app functionality.
- **P1 (Important but Non-Critical)**: Secondary features that enhance user experience.

### **3. Generate Test Scripts**
The tool maps classified UI elements to generate Appium test scripts dynamically.

### **4. Convert Appium Test Steps to NLP**
The script `convert_appium_to_nlp.py` extracts test steps from Appium scripts and converts them into natural language using an LLM.

Example:

**Appium Code:**
```python
    element = wait.until(EC.presence_of_element_located((By.ID, "com.example:id/button")))
    element.click()
```

**Converted NLP Instruction:**
```
    Step 1: Wait until the button is visible, then click on it.
```

## Future Enhancements

- Advanced NLP summarization of test cases.
- Integration with CI/CD pipelines for automated testing.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

