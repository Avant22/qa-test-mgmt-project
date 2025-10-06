import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@pytest.mark.regression
def test_checkout_flow(browser):
    wait = WebDriverWait(browser, 20)
    browser.get("https://www.saucedemo.com/")

    browser.find_element(By.ID, "user-name").send_keys("standard_user")
    browser.find_element(By.ID, "password").send_keys("secret_sauce")
    browser.find_element(By.ID, "login-button").click()

    wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
    browser.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    # Retry clicking checkout up to 3 times for CI reliability
    checkout_clicked = False
    for i in range(3):
        try:
            elem = wait.until(EC.presence_of_element_located((By.ID, "checkout")))
            wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
            elem.click()
            checkout_clicked = True
            break
        except TimeoutException:
            time.sleep(2)

    if not checkout_clicked:
        browser.save_screenshot("screenshots/checkout_fail_retry.png")
        pytest.fail("Checkout button not clickable after multiple retries — likely CI timing issue")

    wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("John")
    browser.find_element(By.ID, "last-name").send_keys("Doe")
    browser.find_element(By.ID, "postal-code").send_keys("12345")
    browser.find_element(By.ID, "continue").click()
    browser.find_element(By.ID, "finish").click()
