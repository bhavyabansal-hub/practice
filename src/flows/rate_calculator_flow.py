import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException

class RateCalculatorFlow:
    SUPPORTED_COUNTRIES = ["Germany", "United States", "Netherlands", "Nigeria", "Afghanistan"]

    def __init__(self, driver, wait_time=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_time)

    def open_rate_calculator(self):
        self.driver.get("https://dev.v.shipgl.in/rate-calculator")
        self.wait.until(
            EC.visibility_of_element_located((By.NAME, "deadWeight"))
        )

    def select_country(self, country):
        """
        Select a country from Radix dropdown by partial text match.
        Works for e.g., "Germany" → "Germany (DEU)"
        """
        try:
            # 1️⃣ Click the dropdown button
            dropdown_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "button-country-destCountry"))
            )
            dropdown_btn.click()

            # 2️⃣ Wait until at least one option is visible
            option_to_click = None
            def find_option(driver):
                options = driver.find_elements(By.XPATH, "//div[@role='option']")
                for option in options:
                    try:
                        if country in option.text.strip() and option.is_displayed():
                            return option
                    except StaleElementReferenceException:
                        continue
                return False

            option_to_click = WebDriverWait(self.driver, 10).until(find_option)

            if not option_to_click:
                raise Exception(f"Country '{country}' not found in dropdown")

            # 3️⃣ Click safely
            try:
                option_to_click.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", option_to_click)

        except TimeoutException:
            raise Exception(f"Dropdown or options not loaded for country '{country}'")

    def fill_details(self, country, pincode, weight, length, breadth, height):
        self.select_country(country)
        self._fill_input("destPincode", pincode)
        self._fill_input("deadWeight", weight)
        self._fill_input("packageLength", length)
        self._fill_input("packageBreadth", breadth)
        self._fill_input("packageHeight", height)

    def _fill_input(self, name, value):
        field = self.wait.until(
            EC.visibility_of_element_located((By.NAME, name))
        )
        field.clear()
        field.send_keys(str(value))

    def click_calculate(self):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        ).click()

    def click_reset(self):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='reset']"))
        ).click()
