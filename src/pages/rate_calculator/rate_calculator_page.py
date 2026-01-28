from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from src.core.base_page import BasePage
from src.locators.rate_calculator_locators import RateCalculatorLocators

class RateCalculatorPage(BasePage):
    def enter_destination_country(self, country_name):
        select = Select(self.find_element(RateCalculatorLocators.DESTINATION_COUNTRY))
        select.select_by_visible_text(country_name)

    def enter_pincode(self, pincode):
        self.send_keys(RateCalculatorLocators.PINCODE, pincode)

    def enter_weight(self, weight):
        self.send_keys(RateCalculatorLocators.WEIGHT, weight)

    def enter_dimensions(self, length, breadth, height):
        self.send_keys(RateCalculatorLocators.LENGTH, length)
        self.send_keys(RateCalculatorLocators.BREADTH, breadth)
        self.send_keys(RateCalculatorLocators.HEIGHT, height)

    def click_calculate(self):
        self.click(RateCalculatorLocators.CALCULATE_BTN)

    def click_reset(self):
        self.click(RateCalculatorLocators.RESET_BTN)

    def get_results(self):
        table = self.find_element(RateCalculatorLocators.RESULTS_TABLE)
        rows = table.find_elements(By.TAG_NAME, "tr")
        result_list = []
        for row in rows[1:]:  # skip header
            cols = row.find_elements(By.TAG_NAME, "td")
            result_list.append({
                "shipper": cols[0].text,
                "price": cols[1].text
            })
        return result_list

    def get_error_message(self):
        return self.get_text(RateCalculatorLocators.ERROR_MSG)
