import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

@pytest.fixture
def browser():
    if not os.getenv("CI"):
        pytest.skip("Skipping Selenium tests locally (CI-only).")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.mark.regression
def test_checkout_flow(browser):
    browser.get("https://www.saucedemo.com/")
    browser.find_element(By.ID, "user-name").send_keys("standard_user")
    browser.find_element(By.ID, "password").send_keys("secret_sauce")
    browser.find_element(By.ID, "login-button").click()

    browser.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    browser.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    browser.find_element(By.ID, "checkout").click()

    assert "Checkout" in browser.page_source
