import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os

@pytest.fixture
def browser():
    # Skip locally if not in CI
    if not os.getenv("CI"):  
        pytest.skip("Skipping Selenium tests locally (CI-only).")

    # In CI → use Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_login_page(browser):
    browser.get("https://www.saucedemo.com/")
    assert "Swag Labs" in browser.title
