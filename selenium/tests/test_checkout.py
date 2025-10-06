import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.regression
def test_checkout_flow(browser):
    wait = WebDriverWait(browser, 20)
    browser.get("https://www.saucedemo.com/")
    browser.find_element(By.ID, "user-name").send_keys("standard_user")
    browser.find_element(By.ID, "password").send_keys("secret_sauce")
    browser.find_element(By.ID, "login-button").click()

    # Add item to basket
    wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
    browser.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    # Simplified checkout click with JS fallback
    elem = wait.until(EC.presence_of_element_located((By.ID, "checkout")))
    browser.execute_script("arguments[0].click();", elem)

    # Verify the next page loaded
    assert "Your Information" in browser.page_source
