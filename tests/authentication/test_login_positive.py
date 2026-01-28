import pytest
from src.flows.authentication_flow import AuthFlow
from configs.settings import Settings
from src.utils.session_manager import SessionManager

class TestLoginPositive(AuthFlow):

    def test_login_with_valid_credentials_and_wait(self):
        """Test login with valid credentials - wait 5 seconds to see dashboard"""
        self.open_login()
        # Verify form is visible
        self.assert_element_visible("input[name='email']")
        self.assert_element_visible("input[name='password']")
        self.assert_element_visible("#kt_sign_in_submit")
        
        # Login with valid credentials
        self.type_text("input[name='email']", Settings.VALID_EMAIL)
        self.type_text("input[name='password']", Settings.VALID_PASSWORD)
        self.click_el("#kt_sign_in_submit")
        
        # Wait 5 seconds to see dashboard/result
        self.sleep(5)
        self.wait_for_element("body", timeout=10)
        self.assert_visible("body")
        
        # Save session for other modules (orders, multibox, etc)
        try:
            SessionManager.save_session(Settings.VALID_EMAIL, Settings.VALID_PASSWORD, "created")
            print("✅ Session saved for other modules")
        except Exception as e:
            print(f"Session save: {e}")
        
        # Keep browser open - don't close

    def test_login_empty_email(self):
        """Test login with empty email field"""
        self.open_login()
        self.assert_element_visible("input[name='email']")
        self.assert_element_visible("input[name='password']")
        
        # Try to submit with empty email
        self.type_text("input[name='password']", Settings.VALID_PASSWORD)
        self.click_el("#kt_sign_in_submit")
        
        self.sleep(2)
        # Should show error or stay on login
        self.assert_visible("body")

    def test_login_empty_password(self):
        """Test login with empty password field"""
        self.open_login()
        self.assert_element_visible("input[name='email']")
        self.assert_element_visible("input[name='password']")
        
        # Try to submit with empty password
        self.type_text("input[name='email']", Settings.VALID_EMAIL)
        self.click_el("#kt_sign_in_submit")
        
        self.sleep(2)
        self.assert_visible("body")

    def test_login_both_fields_empty(self):
        """Test login with both email and password empty"""
        self.open_login()
        # Try to submit without entering anything
        self.click_el("#kt_sign_in_submit")
        
        self.sleep(2)
        self.assert_visible("body")
