from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RateCalculatorValidations:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # --------------------------------------------------
    # Positive result validation
    # --------------------------------------------------
    def verify_results_present(self):
        try:
            self.wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//*[contains(text(),'₹') or contains(text(),'INR') or contains(text(),'Courier')]"
                ))
            )
            return True
        except:
            return False

    # --------------------------------------------------
    # Any validation / form error
    # --------------------------------------------------
    def verify_any_error_present(self):
        try:
            self.wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//*[contains(text(),'Invalid') or contains(text(),'required') or contains(text(),'Error')]"
                ))
            )
            return True
        except:
            return False
