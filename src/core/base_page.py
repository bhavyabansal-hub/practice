# base_page.py placeholder
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def wait_for_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait_for_element(locator).click()

    def type(self, locator, text):
        el = self.wait_for_element(locator)
        el.clear()
        el.send_keys(text)

    def is_elements_present(self, locator):
        elements = self.driver.find_elements(*locator)
        return len(elements) > 0
