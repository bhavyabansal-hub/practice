import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def login_session(driver):
    driver.get("https://dev.v.shipgl.in/auth/login")
    driver.find_element("name", "email").send_keys("12260@vendorexample.com")
    driver.find_element("name", "password").send_keys("123456")
    driver.find_element("xpath", "//button[@type='submit']").click()
