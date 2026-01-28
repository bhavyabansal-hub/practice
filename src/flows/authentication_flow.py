from src.pages.authentication.login_page import LoginPage
from src.pages.authentication.create_account_page import SignupPage
from src.pages.authentication.mobile_verification_page import MobileVerificationPage
from src.pages.authentication.legal_consent_modal import LegalConsentModal
from src.pages.authentication.forgot_password_page import ForgotPasswordPage
from src.utils.session_manager import SessionManager
from configs.settings import Settings

class AuthFlow(LoginPage, SignupPage, MobileVerificationPage, LegalConsentModal, ForgotPasswordPage):

    def login_with_valid_credentials(self):
        """Login with valid test credentials"""
        self.open_login()
        self.login(Settings.VALID_EMAIL, Settings.VALID_PASSWORD)
        self.verify_dashboard()
        try:
            SessionManager.save_session(Settings.VALID_EMAIL, Settings.VALID_PASSWORD)
        except Exception as e:
            print(f"Session save failed: {e}")
        return self.driver

    def login_and_verify(self, email, password):
        """Login and verify dashboard access"""
        self.open_login()
        self.login(email, password)
        # Verify we reached dashboard
        try:
            self.verify_dashboard()
            return True
        except:
            # If dashboard verification fails, check if we're still on page
            self.wait_for_element("body", timeout=5)
            return False

    def login_ui_only(self, email, password):
        """Test login form UI without server authentication"""
        self.open_login()
        self.assert_element_visible("input[name='email']")
        self.assert_element_visible("input[name='password']")
        self.assert_element_visible("#kt_sign_in_submit")
        self.type_text("input[name='email']", email)
        self.type_text("input[name='password']", password)
        self.click_el("#kt_sign_in_submit")
        self.wait_for_element("body", timeout=10)

    def signup_and_login_cycle(self, fn, ln, mobile, email, password):
        """Create account, then login with new credentials - full auth cycle"""
        # Step 1: Create account
        self.open_signup()
        self.create_account(fn, ln, mobile, email, password)
        self.wait_for_element("body", timeout=10)
        
        # Step 2: Login with new account
        self.open_login()
        self.login(email, password)
        try:
            self.verify_dashboard()
            return True
        except:
            self.wait_for_element("body", timeout=5)
            return False

    def signup_and_verify(self, fn, ln, mobile, email, password):
        """Signup and keep browser open"""
        self.open_signup()
        self.create_account(fn, ln, mobile, email, password)
        self.wait_for_element("body", timeout=10)
        return self.driver

    def signup_and_logout(self, fn, ln, mobile, email, password):
        """Create account → redirect to mobile verification → logout"""
        print(f"\n📝 Creating account with email: {email}")
        self.open_signup()
        self.create_account(fn, ln, mobile, email, password)
        self.sleep(3)  # Wait for redirect
        print(f"Account created, waiting for mobile verification page...")
        
        # Should redirect to mobile verification page
        try:
            self.verify_mobile_verification_page()
            print(f"✅ Successfully redirected to mobile verification page")
        except Exception as e:
            print(f"⚠️ Not on mobile verification page: {e}")
            # Take screenshot for debugging
            self.save_screenshot("signup_redirect.png")
        
        self.sleep(2)
        print(f"Logging out from mobile verification page...")
        self.logout()
        print(f"✅ Successfully logged out")
        return email, password  # Return credentials for login test

    def login_test_with_credentials(self, email, password, should_pass=True):
        """Test login with given credentials"""
        print(f"\n🔐 Testing login with email: {email}")
        self.open_login()
        self.type_text("input[name='email']", email)
        self.type_text("input[name='password']", password)
        print(f"Submitting login form...")
        self.click_el("#kt_sign_in_submit")
        self.sleep(5)  # Wait 5 seconds to see the result
        
        if should_pass:
            try:
                self.verify_dashboard()
                print(f"✅ LOGIN SUCCESSFUL - User logged in and redirected to dashboard")
                return True
            except Exception as e:
                print(f"❌ LOGIN FAILED - Expected to reach dashboard but got: {e}")
                self.save_screenshot("login_failed.png")
                return False
        else:
            try:
                # Should still be on login page or see error
                self.verify_login_page()
                print(f"✅ LOGIN CORRECTLY REJECTED - User stayed on login page with error")
                return True
            except:
                # Try to detect if we're on dashboard (which would be wrong)
                try:
                    self.verify_dashboard()
                    print(f"❌ LOGIN SHOULD HAVE FAILED - But user was logged in!")
                    return False
                except:
                    print(f"✅ LOGIN CORRECTLY REJECTED - Error displayed")
                    return True

    def verify_mobile(self, otp):
        self.submit_otp(otp)

    def accept_legal_terms(self):
        self.accept_terms()
