"""
PRE-TEST SETUP MODULE
=====================

Handles pre-test setup for each module:
1. Checks if session exists
2. If YES → Reuse it (skip account creation)
3. If NO → Create account & login (save for future use)

This ensures:
- Only 1 account per test run
- No duplicate accounts created
- Fast test execution
- Production-like behavior

Usage in your test:
    from utils.pre_test_setup import setup_test_environment
    
    class TestOrdersModule:
        @classmethod
        def setup_class(cls):
            cls.base_page = setup_test_environment("orders")
            cls.email = cls.base_page.test_email
            cls.password = cls.base_page.test_password
"""

from selenium.webdriver.chrome.webdriver import WebDriver
from src.flows.authentication_flow import AuthFlow
from src.utils.session_manager import SessionManager
from configs.settings import Settings


class TestSetup:
    """Pre-test setup helper"""
    
    @staticmethod
    def check_and_login_or_create(driver, module_name):
        """
        Check session and login OR create account
        
        Args:
            driver: Selenium WebDriver
            module_name: Name of test module ('orders', 'multibox', etc)
        
        Returns:
            dict with email and password
        """
        print(f"\n{'='*70}")
        print(f"🚀 SETUP: {module_name.upper()} MODULE")
        print(f"{'='*70}")
        
        # Check if session already exists
        existing_session = SessionManager.get_session()
        
        if existing_session:
            print(f"\n✅ Session already exists!")
            print(f"   Email: {existing_session['email']}")
            print(f"   Type: {existing_session['account_type']}")
            print(f"   Reusing account... No new creation needed!")
            
            # Track this module's usage
            SessionManager.add_module_usage(module_name)
            
            return {
                "email": existing_session['email'],
                "password": existing_session['password'],
                "type": "reused"
            }
        
        else:
            print(f"\n📝 No session found. Creating new account...")
            
            # Create new account using AuthFlow
            auth_flow = AuthFlow(driver)
            
            # Use valid test credentials
            email = Settings.VALID_EMAIL
            password = Settings.VALID_PASSWORD
            
            try:
                # Open signup
                auth_flow.open_signup()
                
                # Fill signup form
                auth_flow.enter_email(email)
                auth_flow.enter_password(password)
                auth_flow.enter_confirm_password(password)
                auth_flow.check_terms_and_conditions()
                auth_flow.submit_signup()
                
                # Wait for verification page
                auth_flow.verify_mobile()
                
                # Save session for future use
                SessionManager.save_session(email, password, "created")
                
                # Track module usage
                SessionManager.add_module_usage(module_name)
                
                print(f"\n✅ Account created successfully!")
                print(f"   Email: {email}")
                print(f"   Password: {password}")
                print(f"   Session saved for future modules")
                
                return {
                    "email": email,
                    "password": password,
                    "type": "created"
                }
            
            except Exception as e:
                print(f"\n❌ Account creation failed: {e}")
                raise
    
    @staticmethod
    def get_test_credentials():
        """
        Get credentials (either from session or Settings)
        
        Returns:
            dict with email and password
        """
        session = SessionManager.get_session()
        
        if session:
            return {
                "email": session['email'],
                "password": session['password'],
                "from": "session"
            }
        else:
            return {
                "email": Settings.VALID_EMAIL,
                "password": Settings.VALID_PASSWORD,
                "from": "settings"
            }


def setup_test_environment(driver, module_name):
    """
    Setup environment for test module
    
    Args:
        driver: Selenium WebDriver
        module_name: Name of module ('orders', 'multibox', etc)
    
    Returns:
        dict with credentials
    """
    credentials = TestSetup.check_and_login_or_create(driver, module_name)
    return credentials
