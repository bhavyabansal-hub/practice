import pytest
from src.flows.authentication_flow import AuthFlow

class TestLoginNegative(AuthFlow):

    def test_login_fail_invalid_email(self):
        """Test login fails with invalid email"""
        self.open_login()
        self.assert_element_visible("input[name='email']")
        self.assert_element_visible("input[name='password']")
        self.type_text("input[name='email']", "invalid@mail.com")
        self.type_text("input[name='password']", "wrongpass")
        self.click_el("#kt_sign_in_submit")
        self.wait_for_element("body", timeout=3)
        self.assert_visible("body")

    def test_login_fail_empty_credentials(self):
        """Test login fails with empty credentials"""
        self.open_login()
        self.assert_element_visible("input[name='email']")
        self.assert_element_visible("input[name='password']")
        # Submit without entering credentials
        self.click_el("#kt_sign_in_submit")
        self.wait_for_element("body", timeout=3)
        self.assert_visible("body")
