from src.core.base_page import BasePage
from src.locators.authentication_locators import MobileVerificationLocators

class MobileVerificationPage(BasePage):

    def submit_otp(self, otp):
        self.type_text(MobileVerificationLocators.OTP_INPUT, otp)
        self.click_el(MobileVerificationLocators.SUBMIT)
