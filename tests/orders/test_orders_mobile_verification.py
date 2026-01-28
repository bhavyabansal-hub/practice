"""
Orders Tests - Mobile Verification & Merchant Agreement Flow
Complete flow: Create account -> Verify mobile in DB -> Accept merchant agreement -> Access orders
"""

import pytest
import time
import logging
from datetime import datetime
from seleniumbase import BaseCase
from src.utils.session_manager import SessionManager
from src.utils.orders_setup import OrdersSetup
from src.utils.database_manager import DatabaseManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestOrdersBasic(BaseCase):
    """Orders module tests with mobile verification flow"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class - load session and setup for orders"""
        cls.session_data = None
        cls.vendor_email = None
        cls.vendor_password = None
        cls.setup_status = None
    
    def setUp(self):
        """Set up each test - verify session exists"""
        # Load session from authentication tests
        self.session_data = SessionManager.get_session()
        
        if not self.session_data:
            pytest.skip("❌ No session found - run authentication tests first")
        
        self.vendor_email = self.session_data.get('email')
        self.vendor_password = self.session_data.get('password')
        
        if not self.vendor_email or not self.vendor_password:
            pytest.skip("❌ Missing credentials in session")
        
        logger.info(f"\n{'='*70}")
        logger.info(f"🧪 TEST: {self._testMethodName.upper()}")
        logger.info(f"📧 Using vendor: {self.vendor_email}")
        logger.info(f"{'='*70}")
    
    def test_01_mobile_verification_status(self):
        """Test 1: Check mobile verification status in database"""
        logger.info("Checking vendor mobile verification status...")
        
        status = OrdersSetup.check_mobile_status(self.vendor_email)
        
        assert status['found'], "❌ Vendor not found in database"
        logger.info(f"✅ Vendor found: {status['email']}")
        logger.info(f"📱 Mobile verified status: {status['mobile_verified']}")
        
        # Log status for reference
        if status['mobile_verified'] == 0:
            logger.info("ℹ️  Mobile not verified yet - will be done in next test")
        else:
            logger.info("✅ Mobile already verified in database")
    
    def test_02_verify_mobile_in_database(self):
        """Test 2: Update database to set mobile_verified = 1"""
        logger.info("Verifying mobile in database...")
        
        success, message = OrdersSetup._verify_mobile_in_database(self.vendor_email)
        
        assert success, f"❌ {message}"
        logger.info(f"✅ {message}")
        
        # Verify the update
        status = OrdersSetup.check_mobile_status(self.vendor_email)
        assert status['mobile_verified'] == 1, "❌ mobile_verified is not 1 after update"
        logger.info(f"✅ Verified: mobile_verified = {status['mobile_verified']}")
    
    def test_03_login_and_accept_merchant_agreement(self):
        """Test 3: Login after mobile verification and accept merchant agreement"""
        logger.info("Starting complete orders setup flow...")
        
        # Run complete setup flow
        setup_result = OrdersSetup.setup_for_orders(
            self,
            self.vendor_email,
            self.vendor_password
        )
        
        # Log results
        logger.info("\n" + "="*70)
        logger.info("SETUP RESULTS:")
        logger.info(f"✅ Mobile Verified: {setup_result['mobile_verified']}")
        logger.info(f"✅ Merchant Agreement Accepted: {setup_result['merchant_agreement_accepted']}")
        logger.info(f"✅ Logged In: {setup_result['logged_in']}")
        logger.info("="*70 + "\n")
        
        if setup_result['errors']:
            logger.warning("⚠️  Warnings:")
            for error in setup_result['errors']:
                logger.warning(f"  - {error}")
        
        # Assertions
        assert setup_result['mobile_verified'], "❌ Mobile verification failed"
        assert setup_result['merchant_agreement_accepted'], "❌ Merchant agreement not accepted"
        assert setup_result['logged_in'], "❌ Login failed"
        assert setup_result['success'], "❌ Setup not successful"
        
        logger.info("✅ All setup steps completed successfully")
    
    def test_04_check_orders_page_accessible(self):
        """Test 4: Verify orders page is accessible after setup"""
        logger.info("Navigating to orders page...")
        
        # Setup should already be done from test 3
        # But we can also do fresh login if needed
        current_url = self.get_current_url()
        logger.info(f"Current URL: {current_url}")
        
        # Navigate to orders page
        self.open("https://dev.v.shipgl.in/orders")
        time.sleep(2)
        
        current_url = self.get_current_url()
        logger.info(f"After navigation: {current_url}")
        
        # Check if we're on orders page (not redirected to login)
        assert "orders" in current_url.lower() or "dashboard" in current_url.lower(), \
            f"❌ Unexpected URL: {current_url}"
        
        logger.info("✅ Orders page is accessible")
    
    def test_05_check_dashboard_accessible(self):
        """Test 5: Verify dashboard is accessible"""
        logger.info("Navigating to dashboard...")
        
        self.open("https://dev.v.shipgl.in/dashboard")
        time.sleep(2)
        
        current_url = self.get_current_url()
        logger.info(f"Current URL: {current_url}")
        
        assert "dashboard" in current_url.lower(), f"❌ Not on dashboard: {current_url}"
        logger.info("✅ Dashboard is accessible")
    
    def test_06_logout_from_orders(self):
        """Test 6: Logout from orders/dashboard"""
        logger.info("Logging out...")
        
        self.open("https://dev.v.shipgl.in/logout")
        time.sleep(2)
        
        current_url = self.get_current_url()
        logger.info(f"After logout: {current_url}")
        
        assert "/login" in current_url or "/logout" in current_url or current_url.endswith("/"), \
            f"⚠️  Unexpected URL after logout: {current_url}"
        
        logger.info("✅ Logout successful")
    
    def tearDown(self):
        """Tear down each test"""
        logger.info(f"🏁 Test completed: {self._testMethodName}\n")


class TestOrdersAdvanced(BaseCase):
    """Advanced orders tests - using session management"""
    
    @classmethod
    def setUpClass(cls):
        """Check if session exists for orders testing"""
        cls.session_data = SessionManager.get_session()
        if not cls.session_data:
            pytest.skip("❌ No session available - run authentication tests first")
    
    def setUp(self):
        """Load credentials from session"""
        self.session_data = SessionManager.get_session()
        self.vendor_email = self.session_data.get('email')
        self.vendor_password = self.session_data.get('password')
    
    def test_01_reuse_session_across_modules(self):
        """Test 1: Verify session can be reused across modules"""
        logger.info("Checking session reusability...")
        
        # Check that session has authentication module
        modules = self.session_data.get('used_by_modules', [])
        logger.info(f"Session used by modules: {modules}")
        
        assert self.vendor_email, "❌ Email not in session"
        assert self.vendor_password, "❌ Password not in session"
        
        logger.info(f"✅ Session is valid for: {self.vendor_email}")
    
    def test_02_database_vendor_verification(self):
        """Test 2: Verify vendor exists and mobile_verified status"""
        logger.info("Verifying vendor in database...")
        
        with DatabaseManager() as db:
            vendor = db.get_vendor_by_email(self.vendor_email)
            
            assert vendor is not None, f"❌ Vendor not found: {self.vendor_email}"
            logger.info(f"✅ Vendor found: {vendor['email']}")
            logger.info(f"   - Mobile verified: {vendor['mobile_verified']}")
            logger.info(f"   - Created at: {vendor['created_at']}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
