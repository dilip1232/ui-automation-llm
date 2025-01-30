from scripts.appium_driver import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_app():
    driver = get_driver()
    wait = WebDriverWait(driver, 10)


    # Step 1: Click on the 'Sign up free' button.
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@text='Sign up free']")))
        element.click()
        print("✅ Click on the 'Sign up free' button.")
    except Exception as e:
        print("Failed: Click on the 'Sign up free' button. -", str(e))

    # Step 2: Click on the 'Log in' button.
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@text='Log in']")))
        element.click()
        print("✅ Click on the 'Log in' button.")
    except Exception as e:
        print("Failed: Click on the 'Log in' button. -", str(e))

    driver.quit()

if __name__ == "__main__":
    test_app()
