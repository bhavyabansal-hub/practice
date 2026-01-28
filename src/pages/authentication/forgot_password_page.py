# forgot_password_page.py placeholder
from src.core.base_page import BasePage
from src.locators.authentication_locators import ForgotPasswordLocators

class ForgotPasswordPage(BasePage):

    def open_forgot_password(self):
        self.open_url("/auth/forgot-password")

    def submit_email(self, email):
        self.type_text(ForgotPasswordLocators.EMAIL, email)
        self.click_el(ForgotPasswordLocators.SUBMIT)
