from scripts.appium_driver import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_app():
    driver = get_driver()
    wait = WebDriverWait(driver, 10)

    try:
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "android.view.ViewGroup")))
        element.click()
        print('Step 1 passed')
    except Exception as e:
        print('Step 1 failed -', str(e))

    try:
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "android.widget.Button")))
        element.click()
        print('Step 2 passed')
    except Exception as e:
        print('Step 2 failed -', str(e))

    try:
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "android.view.ViewGroup")))
        element.click()
        print('Step 3 passed')
    except Exception as e:
        print('Step 3 failed -', str(e))

    try:
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "android.widget.EditText")))
        element.click()
        print('Step 4 passed')
    except Exception as e:
        print('Step 4 failed -', str(e))

    try:
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "android.widget.EditText")))
        element.send_keys("sample text")
        print('Step 4 passed')
    except Exception as e:
        print('Step 4 failed -', str(e))

    try:
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "android.view.ViewGroup")))
        element.click()
        print('Step 5 passed')
    except Exception as e:
        print('Step 5 failed -', str(e))

    try:
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "android.widget.EditText")))
        element.click()
        print('Step 6 passed')
    except Exception as e:
        print('Step 6 failed -', str(e))

    try:
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "android.widget.EditText")))
        element.send_keys("sample text")
        print('Step 6 passed')
    except Exception as e:
        print('Step 6 failed -', str(e))

    try:
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "android.widget.Button")))
        element.click()
        print('Step 7 passed')
    except Exception as e:
        print('Step 7 failed -', str(e))

    try:
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "android.widget.Button")))
        element.click()
        print('Step 8 passed')
    except Exception as e:
        print('Step 8 failed -', str(e))

    try:
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "android.widget.Button")))
        element.click()
        print('Step 9 passed')
    except Exception as e:
        print('Step 9 failed -', str(e))

    driver.quit()

if __name__ == '__main__':
    test_app()
