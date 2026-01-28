from src.core.base_page import BasePage
from src.locators.authentication_locators import LogoutLocators

class LogoutPage(BasePage):

    def logout(self):
        """Click logout button/link"""
        try:
            # Try to find and click logout button
            self.click_el(LogoutLocators.LOGOUT_BUTTON)
            # Wait for redirect to login page
            self.verify_login_page()
        except Exception as e:
            print(f"Logout failed: {e}")
            raise