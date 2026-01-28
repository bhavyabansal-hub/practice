"""
Orders Pre-Test Setup Module
Handles mobile verification bypass and merchant agreement acceptance
Works with created accounts from authentication tests
"""

import time
import logging
from src.utils.database_manager import DatabaseManager
from src.utils.session_manager import SessionManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrdersSetup:
    """
    Complete setup for Orders testing with mobile verification and merchant agreement
    """
    
    @staticmethod
    def setup_for_orders(driver, email: str, password: str) -> Dict:
        """
        Complete flow: Verify mobile in DB -> Logout -> Login -> Accept merchant agreement
        
        Args:
            driver: SeleniumBase driver
            email: Vendor email (from authentication test)
            password: Vendor password (from authentication test)
            
        Returns:
            Dict with setup status and details
        """
        setup_result = {
            'success': False,
            'email': email,
            'password': password,
            'mobile_verified': False,
            'merchant_agreement_accepted': False,
            'logged_in': False,
            'errors': []
        }
        
        try:
            # Step 1: Update database to verify mobile
            logger.info(f"📱 Step 1: Verifying mobile in database for {email}")
            success, message = OrdersSetup._verify_mobile_in_database(email)
            setup_result['mobile_verified'] = success
            if not success:
                setup_result['errors'].append(f"Mobile verification failed: {message}")
                return setup_result
            logger.info(f"✅ {message}")
            
            # Step 2: Logout from current session
            logger.info("🚪 Step 2: Logging out from current session")
            try:
                driver.get("https://dev.v.shipgl.in/logout")
                time.sleep(2)
                logger.info("✅ Logout successful")
            except Exception as err:
                setup_result['errors'].append(f"Logout failed: {str(err)}")
                logger.warning(f"⚠️  Logout warning: {err}")
            
            # Step 3: Navigate to login page
            logger.info("📍 Step 3: Navigating to login page")
            driver.get("https://dev.v.shipgl.in/auth/login")
            time.sleep(2)
            logger.info("✅ Login page loaded")
            
            # Step 4: Enter credentials
            logger.info("🔐 Step 4: Entering credentials")
            driver.type("input[name='email']", email)
            driver.type("input[name='password']", password)
            time.sleep(1)
            logger.info("✅ Credentials entered")
            
            # Step 5: Click login button
            logger.info("🚀 Step 5: Clicking login button")
            driver.click("#kt_sign_in_submit")
            time.sleep(4)
            logger.info("✅ Login submitted")
            
            # Step 6: Handle mobile verification page (should be skipped now)
            current_url = driver.get_current_url()
            if "/verify-mobile" in current_url:
                logger.warning("⚠️  Mobile verification page appeared (unexpected)")
                setup_result['errors'].append("Mobile verification page still appears after DB update")
                return setup_result
            
            # Step 7: Handle merchant agreement popup
            logger.info("📋 Step 7: Looking for merchant agreement popup")
            try:
                # Wait for accept button to appear
                driver.wait_for_element("button[type='submit']", timeout=5)
                
                # Get all buttons and find the one with "Accept" text
                buttons = driver.find_elements("button[type='submit']")
                accept_button = None
                
                for button in buttons:
                    if button.text and "Accept" in button.text:
                        accept_button = button
                        break
                
                if accept_button:
                    logger.info("✅ Accept button found")
                    driver.execute_script("arguments[0].click();", accept_button)
                    time.sleep(3)
                    setup_result['merchant_agreement_accepted'] = True
                    logger.info("✅ Merchant agreement accepted")
                else:
                    logger.warning("⚠️  Accept button not found with text 'Accept'")
                    # Try clicking the button anyway
                    driver.click("button[type='submit']")
                    time.sleep(3)
                    setup_result['merchant_agreement_accepted'] = True
                    logger.info("✅ Button clicked (text not verified)")
                    
            except Exception as err:
                logger.warning(f"⚠️  Merchant agreement handling: {err}")
                setup_result['errors'].append(f"Merchant agreement error: {str(err)}")
            
            # Step 8: Verify login successful
            logger.info("✔️  Step 8: Verifying successful login")
            time.sleep(2)
            current_url = driver.get_current_url()
            
            if "/dashboard" in current_url or "/orders" in current_url:
                setup_result['logged_in'] = True
                setup_result['success'] = True
                logger.info(f"✅ Successfully logged in, current URL: {current_url}")
            else:
                setup_result['errors'].append(f"Unexpected URL after login: {current_url}")
                logger.warning(f"⚠️  Unexpected URL: {current_url}")
            
            return setup_result
            
        except Exception as err:
            setup_result['errors'].append(f"Setup error: {str(err)}")
            logger.error(f"❌ Setup error: {err}")
            return setup_result
    
    @staticmethod
    def _verify_mobile_in_database(email: str) -> Tuple[bool, str]:
        """
        Verify mobile in database by updating mobile_verified = 1
        
        Args:
            email: Vendor email
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            with DatabaseManager() as db:
                return db.verify_mobile_for_email(email)
        except Exception as err:
            logger.error(f"❌ Database connection error: {err}")
            return False, f"Database error: {str(err)}"
    
    @staticmethod
    def check_mobile_status(email: str) -> Dict:
        """
        Check current mobile verification status in database
        
        Args:
            email: Vendor email
            
        Returns:
            Dict with vendor details and mobile_verified status
        """
        try:
            with DatabaseManager() as db:
                vendor = db.get_vendor_by_email(email)
                if vendor:
                    return {
                        'found': True,
                        'email': vendor['email'],
                        'mobile_verified': vendor['mobile_verified'],
                        'id': vendor['id']
                    }
                return {'found': False, 'email': email}
        except Exception as err:
            logger.error(f"❌ Error checking status: {err}")
            return {'found': False, 'error': str(err)}
    
    @staticmethod
    def cleanup_mobile_verification(email: str) -> Tuple[bool, str]:
        """
        Reset mobile_verified to 0 for cleanup (optional)
        
        Args:
            email: Vendor email
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            with DatabaseManager() as db:
                return db.reset_mobile_verified(email)
        except Exception as err:
            logger.error(f"❌ Cleanup error: {err}")
            return False, f"Cleanup error: {str(err)}"


from typing import Tuple, Dict
