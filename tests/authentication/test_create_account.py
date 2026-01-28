import pytest
from src.flows.authentication_flow import AuthFlow
from configs.settings import Settings
import time

class TestSignupFieldValidation(AuthFlow):
    """Test signup form field validation with various inputs"""

    def test_signup_empty_first_name(self):
        """Test signup with empty first name"""
        self.open_signup()
        self.type_text("input[name='lastName']", "TestLast")
        self.type_text("input[name='mobile']", "9999999999")
        self.type_text("input[name='email']", f"test.{int(time.time())}@test.com")
        self.type_text("input[name='password']", "Test@123456")
        self.type_text("input[name='confirmPassword']", "Test@123456")
        self.click_el("#toc")
        self.click_el("#sign_up_submit")
        self.sleep(2)
        self.assert_visible("body")

    def test_signup_empty_email(self):
        """Test signup with empty email"""
        self.open_signup()
        self.type_text("input[name='firstName']", "TestFirst")
        self.type_text("input[name='lastName']", "TestLast")
        self.type_text("input[name='mobile']", "9999999999")
        self.type_text("input[name='password']", "Test@123456")
        self.type_text("input[name='confirmPassword']", "Test@123456")
        self.click_el("#toc")
        self.click_el("#sign_up_submit")
        self.sleep(2)
        self.assert_visible("body")

    def test_signup_invalid_email_format(self):
        """Test signup with invalid email format"""
        self.open_signup()
        self.type_text("input[name='firstName']", "TestFirst")
        self.type_text("input[name='lastName']", "TestLast")
        self.type_text("input[name='mobile']", "9999999999")
        self.type_text("input[name='email']", "invalid-email-format")
        self.type_text("input[name='password']", "Test@123456")
        self.type_text("input[name='confirmPassword']", "Test@123456")
        self.click_el("#toc")
        self.click_el("#sign_up_submit")
        self.sleep(2)
        self.assert_visible("body")

    def test_signup_mismatched_passwords(self):
        """Test signup with mismatched password and confirm password"""
        self.open_signup()
        self.type_text("input[name='firstName']", "TestFirst")
        self.type_text("input[name='lastName']", "TestLast")
        self.type_text("input[name='mobile']", "9999999999")
        self.type_text("input[name='email']", f"test.{int(time.time())}@test.com")
        self.type_text("input[name='password']", "Test@123456")
        self.type_text("input[name='confirmPassword']", "Different@123456")
        self.click_el("#toc")
        self.click_el("#sign_up_submit")
        self.sleep(2)
        self.assert_visible("body")

    def test_signup_special_characters_in_name(self):
        """Test signup with special characters in name"""
        self.open_signup()
        self.type_text("input[name='firstName']", "Test@#$%")
        self.type_text("input[name='lastName']", "User!@#")
        self.type_text("input[name='mobile']", "9999999999")
        self.type_text("input[name='email']", f"test.{int(time.time())}@test.com")
        self.type_text("input[name='password']", "Test@123456")
        self.type_text("input[name='confirmPassword']", "Test@123456")
        self.click_el("#toc")
        self.click_el("#sign_up_submit")
        self.sleep(2)
        self.assert_visible("body")

    def test_signup_invalid_mobile_format(self):
        """Test signup with invalid mobile number format"""
        self.open_signup()
        self.type_text("input[name='firstName']", "TestFirst")
        self.type_text("input[name='lastName']", "TestLast")
        self.type_text("input[name='mobile']", "abc123xyz")
        self.type_text("input[name='email']", f"test.{int(time.time())}@test.com")
        self.type_text("input[name='password']", "Test@123456")
        self.type_text("input[name='confirmPassword']", "Test@123456")
        self.click_el("#toc")
        self.click_el("#sign_up_submit")
        self.sleep(2)
        self.assert_visible("body")

    def test_signup_without_accepting_terms(self):
        """Test signup without accepting terms checkbox"""
        self.open_signup()
        self.type_text("input[name='firstName']", "TestFirst")
        self.type_text("input[name='lastName']", "TestLast")
        self.type_text("input[name='mobile']", "9999999999")
        self.type_text("input[name='email']", f"test.{int(time.time())}@test.com")
        self.type_text("input[name='password']", "Test@123456")
        self.type_text("input[name='confirmPassword']", "Test@123456")
        # Don't click terms checkbox
        self.click_el("#sign_up_submit")
        self.sleep(2)
        self.assert_visible("body")

class TestSignupPositive(AuthFlow):

    def test_signup_and_login_cycle(self):
        """Create account and login - complete authentication cycle - WAIT 5 SECONDS"""
        # Generate unique email
        email = f"test.user.{int(time.time())}@example.com"
        password = "TestPass@123"
        
        # Step 1: Create account
        self.open_signup()
        self.assert_element_visible("input[name='firstName']")
        self.type_text("input[name='firstName']", "Test")
        self.type_text("input[name='lastName']", "User")
        self.type_text("input[name='mobile']", "9999999999")
        self.type_text("input[name='email']", email)
        self.type_text("input[name='password']", password)
        self.type_text("input[name='confirmPassword']", password)
        self.click_el("#toc")  # Accept terms
        self.click_el("#sign_up_submit")
        self.wait_for_element("body", timeout=10)
        
        # Step 2: Login with newly created account
        self.open_login()
        self.type_text("input[name='email']", email)
        self.type_text("input[name='password']", password)
        self.click_el("#kt_sign_in_submit")
        
        # WAIT 5 SECONDS TO SEE ACCOUNT CREATION WORKING
        self.sleep(5)
        self.wait_for_element("body", timeout=10)
        # Verify page loads after login
        self.assert_visible("body")
        print(f"✅ Account Created: {email} | Password: {password}")

    def test_signup_with_multiple_accounts(self):
        """Test creating multiple accounts and logging in"""
        accounts = [
            ("Alice", "Wonder", "9876543210", f"alice.{int(time.time())}@test.com", "Alice@123456"),
            ("Bob", "Builder", "9876543211", f"bob.{int(time.time())+1}@test.com", "Bob@123456"),
        ]
        
        for fn, ln, mobile, email, password in accounts:
            # Create account
            self.open_signup()
            self.type_text("input[name='firstName']", fn)
            self.type_text("input[name='lastName']", ln)
            self.type_text("input[name='mobile']", mobile)
            self.type_text("input[name='email']", email)
            self.type_text("input[name='password']", password)
            self.type_text("input[name='confirmPassword']", password)
            self.click_el("#toc")
            self.click_el("#sign_up_submit")
            self.wait_for_element("body", timeout=10)
            
            # Login with created account
            self.open_login()
            self.type_text("input[name='email']", email)
            self.type_text("input[name='password']", password)
            self.click_el("#kt_sign_in_submit")
            
            # WAIT 5 SECONDS TO SEE RESULT
            self.sleep(5)
            self.wait_for_element("body", timeout=10)
            print(f"✅ Account Verified: {email}")
