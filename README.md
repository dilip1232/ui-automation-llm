# Automated Appium Test Script Generator

## Overview

This project automates the generation of Appium test scripts by converting conversational test steps into executable Python code. It uses a JSON file containing classified UI elements to map user-friendly commands to corresponding Appium actions. This allows for test creation using natural language, simplifying the process and making it more accessible to those without deep Appium expertise.  The project also leverages an LLM (Large Language Model) for intelligent feature prioritization.

## Features

*   **Conversational Test Steps:** Define test scenarios in natural language.
*   **Dynamic Locator Generation:** Automatically generates locators based on UI element attributes.
*   **Error Handling:** Gracefully handles missing or invalid UI elements.
*   **LLM-Powered Feature Classification:** Classifies features into priority levels (P0 and P1) using an LLM for efficient testing.
*   **Emulator and APK Management:** Includes scripts for emulator control, APK installation, and UI element extraction.

## Requirements

*   Python 3.x
*   Appium
*   Selenium WebDriver
*   LLM (Large Language Model) access (e.g., Gemini, etc.)
*   Android SDK Platform Tools (for emulator management)

## Setup

1.  **Clone the Repository:**

2.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure LLM API Key:**

    Refer .env.example

4.  **Set up Android SDK:**

    Ensure you have the Android SDK Platform Tools installed and the `adb` command is in your system's PATH.

## Running the Tests

1.  **Start Appium Server:**

    ```bash
    appium
    ```

2.  **Run Emulator and Install APK:**

    ```bash
    python scripts/emulator.py -a <path_to_your_apk_file.apk>  # Replace with your APK path
    ```
   You can use -p flag to mention specific port for emulator. By default it will use port 5554.

3.  **Extract UI Elements:**

    ```bash
    python scripts/extract_elements.py
    ```

4.  **Classify Features (using LLM):**

    ```bash
    python scripts/classify_features.py
    ```

5.  **Generate Test Scripts:**

    ```bash
    python scripts/generate_tests.py
    ```

6.  **Run Generated Tests:**

    ```bash
    python test_appium.py
    ```