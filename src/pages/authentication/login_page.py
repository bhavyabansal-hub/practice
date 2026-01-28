from src.core.base_page import BasePage
from src.locators.authentication_locators import LoginLocators

class LoginPage(BasePage):

    def open_login(self):
        self.open_url("/auth/login")

    def login(self, email, password):
        self.type_text(LoginLocators.EMAIL, email)
        self.type_text(LoginLocators.PASSWORD, password)
        self.click_el(LoginLocators.SUBMIT)
        # Wait for redirect to dashboard
        self.wait_for_element("body", timeout=10)

    def go_to_signup(self):
        self.click_el(LoginLocators.CREATE_ACCOUNT_LINK)

    def go_to_forgot_password(self):
        self.click_el(LoginLocators.FORGOT_PASSWORD_LINK)
