import sys
import os
import pytest

# 🔥 FIX src IMPORT PATH (UNCHANGED)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from src.core.driver_factory import DriverFactory
from src.flows.rate_calculator_flow import RateCalculatorFlow
from src.validations.rate_calculator_validations import RateCalculatorValidations


# ❌ NO INDIA ANYWHERE
SUPPORTED_COUNTRIES = [
    "Germany",
    "United States",
    "Netherlands",
    "Nigeria",
    "Afghanistan"
]


@pytest.fixture(scope="class")
def setup(request):
    driver = DriverFactory.create_driver(headless=False)
    wait = WebDriverWait(driver, 15)  # ⏩ faster than 20

    driver.get("https://dev.v.shipgl.in/auth/login")

    # ---- LOGIN ----
    wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys(
        "12260@vendorexample.com"
    )
    driver.find_element(By.NAME, "password").send_keys("Krishna@1234@1234")
    driver.find_element(By.ID, "kt_sign_in_submit").click()

    # ---- WAIT FOR DASHBOARD ----
    wait.until(EC.url_contains("/dashboard"))

    # ---- 🔥 CRITICAL FIX: CLOSE PASSWORD POPUP IF PRESENT ----
    try:
        ok_button = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[normalize-space()='OK' or normalize-space()='Close']"
            ))
        )
        ok_button.click()
        print("✅ Password change popup closed")
    except TimeoutException:
        print("ℹ️ Password popup not shown")

    request.cls.driver = driver
    yield
    driver.quit()


@pytest.mark.usefixtures("setup")
class TestRateCalculator:

    @pytest.mark.parametrize("country", SUPPORTED_COUNTRIES)
    def test_rate_calculator_positive(self, country):
        flow = RateCalculatorFlow(self.driver)
        validation = RateCalculatorValidations(self.driver)

        flow.open_rate_calculator()
        flow.fill_details(
            country=country,
            pincode="10115",  # ❌ NOT INDIA
            weight=5,
            length=50,
            breadth=50,
            height=50
        )
        flow.click_calculate()

        assert validation.verify_results_present(), \
            f"Expected results not displayed for {country}"

    @pytest.mark.parametrize("country", SUPPORTED_COUNTRIES)
    def test_rate_calculator_negative_weight(self, country):
        flow = RateCalculatorFlow(self.driver)
        validation = RateCalculatorValidations(self.driver)

        flow.open_rate_calculator()
        flow.fill_details(
            country=country,
            pincode="10115",
            weight=-5,
            length=50,
            breadth=50,
            height=50
        )
        flow.click_calculate()

        assert validation.verify_any_error_present(), \
            f"Expected an error for negative weight but none shown for {country}"

    @pytest.mark.parametrize("country", SUPPORTED_COUNTRIES)
    def test_rate_calculator_negative_dimensions(self, country):
        flow = RateCalculatorFlow(self.driver)
        validation = RateCalculatorValidations(self.driver)

        flow.open_rate_calculator()
        flow.fill_details(
            country=country,
            pincode="10115",
            weight=5,
            length=150,
            breadth=50,
            height=50
        )
        flow.click_calculate()

        assert validation.verify_any_error_present(), \
            f"Expected an error for invalid dimensions but none shown for {country}"
