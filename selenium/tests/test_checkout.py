import pytest, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, ElementNotInteractableException

@pytest.mark.regression
def test_checkout_flow(browser):
    wait = WebDriverWait(browser, 25)
    browser.get("https://www.saucedemo.com/")
    browser.find_element(By.ID, "user-name").send_keys("standard_user")
    browser.find_element(By.ID, "password").send_keys("secret_sauce")
    browser.find_element(By.ID, "login-button").click()

    wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
    browser.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    # Ultra-stable checkout button click logic
    success = False
    for attempt in range(5):
        try:
            elem = wait.until(EC.presence_of_element_located((By.ID, "checkout")))
            browser.execute_script("arguments[0].scrollIntoView(true);", elem)
            wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
            elem.click()
            success = True
            break
        except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException):
            time.sleep(3)

    if not success:
        browser.save_screenshot("screenshots/checkout_fail_final.png")
        page_source = browser.page_source
        with open("screenshots/checkout_page_source.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        pytest.fail("Checkout button could not be clicked after retries and scrolls.")

    wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("John")
    browser.find_element(By.ID, "last-name").send_keys("Doe")
    browser.find_element(By.ID, "postal-code").send_keys("12345")
    browser.find_element(By.ID, "continue").click()
    browser.find_element(By.ID, "finish").click()

    assert "Thank you" in browser.page_source or "Complete" in browser.page_source
