from appium import webdriver
from appium.options.android import UiAutomator2Options
import os

def get_driver(device_name=None):
    device_name = device_name or os.getenv("DEVICE_NAME", "emulator-5554")

    options = UiAutomator2Options()
    options.set_capability("platformName", "Android")
    options.set_capability("deviceName", device_name)
    options.set_capability("automationName", "UiAutomator2")
    options.set_capability("appPackage", "com.spotify.music")

    # ✅ Set the correct activity
    options.set_capability("appActivity", "com.spotify.music.MainActivity")

    # ✅ Prevent app from stopping
    options.set_capability("dontStopAppOnReset", True)
    options.set_capability("noReset", True)  

    appium_url = os.getenv("APPIUM_URL", "http://127.0.0.1:4723")
    driver = webdriver.Remote(appium_url, options=options)

    return driver
