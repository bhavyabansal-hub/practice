from selenium.webdriver.common.by import By

class RateCalculatorLocators:
    DESTINATION_COUNTRY = (By.ID, "destination_country")  # select element
    PINCODE = (By.ID, "pincode")
    WEIGHT = (By.ID, "weight")
    LENGTH = (By.ID, "length")
    BREADTH = (By.ID, "breadth")
    HEIGHT = (By.ID, "height")
    CALCULATE_BTN = (By.ID, "calculateBtn")
    RESET_BTN = (By.ID, "resetBtn")
    RESULTS_TABLE = (By.ID, "resultsTable")  # table showing shipper and rates
    ERROR_MSG = (By.CLASS_NAME, "error-message")
