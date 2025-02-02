import subprocess
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options

def get_driver(device_name=None, apk_path=None):
    """
    Initializes and returns an Appium driver.

    - Extracts `appPackage` & `appActivity` using `apkanalyzer` (fallback to `aapt` if needed).
    - If `appActivity` is missing, starts the app using ADB `monkey`.
    - Installs the APK only if it's not already installed.
    - Ensures the app is running before Appium connects.
    """

    device_name = device_name or os.getenv("DEVICE_NAME", "emulator-5554")
    apk_path = apk_path or os.getenv("APK_PATH")

    if not apk_path:
        raise ValueError("APK path must be provided to launch the app.")

    print(f"Extracting package name and main activity from APK: {apk_path}")
    
    # Extract package name and main activity
    app_package, app_activity = extract_package_and_activity(apk_path)

    if not app_package:
        raise RuntimeError("Could not determine app package from APK.")

    # If app is not installed, install it
    if not is_app_installed(app_package):
        print(f"Installing APK: {apk_path}")
        subprocess.run(["adb", "install", apk_path], check=True)

    # If appActivity is missing, start the app using ADB `monkey`
    if not app_activity:
        print(f"Starting {app_package} using ADB monkey...")
        subprocess.run(["adb", "shell", "monkey", "-p", app_package, "-c", "android.intent.category.LAUNCHER", "1"], check=True)

    wait_for_app_to_launch(app_package)

    # Initialize Appium driver
    options = UiAutomator2Options()
    options.set_capability("platformName", "Android")
    options.set_capability("deviceName", device_name)
    options.set_capability("automationName", "UiAutomator2")
    options.set_capability("appPackage", app_package)

    if app_activity:
        options.set_capability("appActivity", app_activity)

    options.set_capability("dontStopAppOnReset", False)
    options.set_capability("noReset", False)

    appium_url = os.getenv("APPIUM_URL", "http://127.0.0.1:4723")
    driver = webdriver.Remote(appium_url, options=options)
    
    return driver

def extract_package_and_activity(apk_path):
    """
    Extracts the package name and main activity using `apkanalyzer`.
    Falls back to `aapt` if `apkanalyzer` is not available.
    """
    try:
        # Try extracting package name & main activity using `apkanalyzer`
        package_name = subprocess.run(
            ["apkanalyzer", "manifest", "application-id", apk_path],
            stdout=subprocess.PIPE, text=True
        ).stdout.strip()

        activities = subprocess.run(
            ["apkanalyzer", "manifest", "activities", apk_path],
            stdout=subprocess.PIPE, text=True
        ).stdout.strip().split("\n")

        # Get first activity as main (if available)
        main_activity = activities[0] if activities and activities[0] else None

        if package_name:
            return package_name, main_activity

        print("apkanalyzer failed, falling back to aapt...")

    except Exception as e:
        print(f"Error using apkanalyzer: {e}")
    
    # Fallback to `aapt` if `apkanalyzer` fails
    try:
        result = subprocess.run(["aapt", "dump", "badging", apk_path], stdout=subprocess.PIPE, text=True)
        package_name, main_activity = None, None

        for line in result.stdout.split("\n"):
            if "package: name=" in line:
                package_name = line.split("name='")[1].split("'")[0]
            if "launchable-activity: name='" in line:
                main_activity = line.split("name='")[1].split("'")[0]
        
        return package_name, main_activity

    except Exception as e:
        print(f"Error using aapt: {e}")

    return None, None

def is_app_installed(app_package):
    """
    Checks if the app is already installed on the device.
    Returns True if installed, False otherwise.
    """
    result = subprocess.run(["adb", "shell", "pm", "list", "packages"], stdout=subprocess.PIPE, text=True)
    installed_packages = [line.split(":")[-1].strip() for line in result.stdout.split("\n") if line]

    return app_package in installed_packages

def wait_for_app_to_launch(app_package, timeout=10):
    """
    Waits for the app to be in the foreground before proceeding.
    """
    import time

    print(f"⏳ Waiting for {app_package} to be in the foreground...")
    for _ in range(timeout):
        result = subprocess.run(["adb", "shell", "dumpsys", "window", "windows"], stdout=subprocess.PIPE, text=True)
        if app_package in result.stdout:
            print(f"{app_package} is now running in the foreground.")
            return True
        time.sleep(1)

    print(f"{app_package} did not launch in time. Proceeding anyway.")
    return False
