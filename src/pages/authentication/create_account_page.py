from src.core.base_page import BasePage
from src.locators.authentication_locators import SignupLocators

class SignupPage(BasePage):

    def open_signup(self):
        self.open_url("/auth/signup")

    def create_account(self, fn, ln, mobile, email, pwd):
        self.type_text(SignupLocators.FIRST_NAME, fn)
        self.type_text(SignupLocators.LAST_NAME, ln)
        self.type_text(SignupLocators.MOBILE, mobile)
        self.type_text(SignupLocators.EMAIL, email)
        self.type_text(SignupLocators.PASSWORD, pwd)
        self.type_text(SignupLocators.CONFIRM_PASSWORD, pwd)
        self.click_el(SignupLocators.TERMS_CHECKBOX)
        self.click_el(SignupLocators.SUBMIT)

    def go_to_login(self):
        self.click_el(SignupLocators.LOGIN_LINK)
