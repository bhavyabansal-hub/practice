"""
SIMPLE AUTHENTICATION TEST SUITE
=================================
Easy to read, understand, and extend!
Anyone can copy this pattern to add new tests.

HOW TO USE THIS FILE:
- NEGATIVE TEST: Test that should FAIL/REJECT
- POSITIVE TEST: Test that should SUCCEED/PASS

TO ADD A NEW TEST:
1. Copy an existing test function
2. Change the test data
3. Run it!

Example NEGATIVE test structure:
    def test_negative_example(self):
        self.open_signup()
        self.type_text("input[name='email']", "invalid_data")
        self.click_el("#sign_up_submit")
        self.sleep(2)
        # Should stay on signup page (not redirect)
        try:
            self.assert_url_contains("/auth/signup")
            print("✓ Correctly rejected invalid data")
        except:
            pytest.fail("✗ Invalid data was incorrectly accepted")

Example POSITIVE test structure:
    def test_positive_example(self):
        self.open_signup()
        self.type_text("input[name='email']", "valid@test.com")
        self.click_el("#sign_up_submit")
        self.sleep(2)
        # Should redirect to success page
        try:
            self.assert_url_contains("/verify-mobile")
            print("✓ Successfully created account")
        except:
            pytest.fail("✗ Account creation failed")
"""
import pytest
import time
import os
from src.flows.authentication_flow import AuthFlow
from configs.settings import Settings
from src.utils.session_manager import SessionManager

# GLOBAL TEST COUNTER - Automatically numbers each test
test_counter = 0

def get_next_test_number():
    """Get and increment test number"""
    global test_counter
    test_counter += 1
    return test_counter

def take_screenshot_on_failure(self, test_name, test_number):
    """Take screenshot and save error message when test fails"""
    screenshots_dir = "screenshots/authentication/test_results"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    timestamp = int(time.time() * 1000)
    screenshot_file = f"{screenshots_dir}/test_{test_name}_FAILED.png"
    error_file = f"{screenshots_dir}/test_{test_name}_FAILED_error.txt"
    
    try:
        # Take screenshot
        self.save_screenshot(screenshot_file)
        print(f"\n📸 Screenshot saved: {screenshot_file}")
    except Exception as e:
        print(f"⚠️ Could not save screenshot: {e}")
    
    # Save error message
    try:
        with open(error_file, 'w') as f:
            f.write(f"❌ TEST CASE {test_number} FAILED\n")
            f.write(f"Test Name: {test_name}\n")
            f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            f.write("Check screenshot for visual details.\n")
        print(f"📝 Error log saved: {error_file}")
    except Exception as e:
        print(f"⚠️ Could not save error log: {e}")


class TestSignupNegative(AuthFlow):
    """
    NEGATIVE TESTS - Email/Password Signup
    These tests should FAIL or REJECT the user input
    Expected: User stays on signup page with error message
    """

    def test_email_empty(self):
        """Test: Email field is EMPTY"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: Email field EMPTY")
        print("="*70)
        
        self.open_signup()
        self.type_text("input[name='firstName']", "Test")
        self.type_text("input[name='lastName']", "User")
        self.type_text("input[name='mobile']", "9876500001")
        self.type_text("input[name='email']", "")  # ← EMPTY!
        self.type_text("input[name='password']", "TestPass@123")
        self.type_text("input[name='confirmPassword']", "TestPass@123")
        self.click_el("#toc")
        self.click_el("#sign_up_submit")
        self.sleep(2)
        
        try:
            self.assert_url_contains("/auth/signup")
            print(f"✅ TEST CASE {test_num} PASSED: Empty email was correctly REJECTED")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Empty email was incorrectly accepted")
            take_screenshot_on_failure(self, "email_empty", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Empty email was incorrectly accepted - {e}")

    def test_email_invalid_format(self):
        """Test: Email format INVALID (no @ symbol)"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: Email format INVALID (no @)")
        print("="*70)
        
        self.open_signup()
        self.type_text("input[name='firstName']", "Test")
        self.type_text("input[name='lastName']", "User")
        self.type_text("input[name='mobile']", "9876500002")
        self.type_text("input[name='email']", "invalidemail.com")  # ← NO @!
        self.type_text("input[name='password']", "TestPass@123")
        self.type_text("input[name='confirmPassword']", "TestPass@123")
        self.click_el("#toc")
        self.click_el("#sign_up_submit")
        self.sleep(2)
        
        try:
            self.assert_url_contains("/auth/signup")
            print(f"✅ TEST CASE {test_num} PASSED: Invalid email format was correctly REJECTED")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Invalid email was incorrectly accepted")
            take_screenshot_on_failure(self, "email_invalid_format", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Invalid email was incorrectly accepted - {e}")

    def test_password_empty(self):
        """Test: Password field is EMPTY"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: Password field EMPTY")
        print("="*70)
        
        self.open_signup()
        self.type_text("input[name='firstName']", "Test")
        self.type_text("input[name='lastName']", "User")
        self.type_text("input[name='mobile']", "9876500003")
        self.type_text("input[name='email']", f"test_{int(time.time())}@test.com")
        self.type_text("input[name='password']", "")  # ← EMPTY!
        self.type_text("input[name='confirmPassword']", "TestPass@123")
        self.click_el("#toc")
        self.click_el("#sign_up_submit")
        self.sleep(2)
        
        try:
            self.assert_url_contains("/auth/signup")
            print(f"✅ TEST CASE {test_num} PASSED: Empty password was correctly REJECTED")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Empty password was incorrectly accepted")
            take_screenshot_on_failure(self, "password_empty", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Empty password was incorrectly accepted - {e}")

    def test_password_mismatch(self):
        """Test: Passwords DO NOT MATCH"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: Password confirmation MISMATCH")
        print("="*70)
        
        self.open_signup()
        self.type_text("input[name='firstName']", "Test")
        self.type_text("input[name='lastName']", "User")
        self.type_text("input[name='mobile']", "9876500004")
        self.type_text("input[name='email']", f"test_{int(time.time())}@test.com")
        self.type_text("input[name='password']", "TestPass@123")
        self.type_text("input[name='confirmPassword']", "DifferentPass@123")  # ← DIFFERENT!
        self.click_el("#toc")
        self.click_el("#sign_up_submit")
        self.sleep(2)
        
        try:
            self.assert_url_contains("/auth/signup")
            print(f"✅ TEST CASE {test_num} PASSED: Mismatched passwords were correctly REJECTED")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Mismatched passwords were incorrectly accepted")
            take_screenshot_on_failure(self, "password_mismatch", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Mismatched passwords were incorrectly accepted - {e}")

    def test_terms_not_accepted(self):
        """Test: Terms checkbox NOT CHECKED"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: Terms checkbox NOT ACCEPTED")
        print("="*70)
        
        self.open_signup()
        self.type_text("input[name='firstName']", "Test")
        self.type_text("input[name='lastName']", "User")
        self.type_text("input[name='mobile']", "9876500005")
        self.type_text("input[name='email']", f"test_{int(time.time())}@test.com")
        self.type_text("input[name='password']", "TestPass@123")
        self.type_text("input[name='confirmPassword']", "TestPass@123")
        # ← DO NOT click terms checkbox!
        self.click_el("#sign_up_submit")
        self.sleep(2)
        
        try:
            self.assert_url_contains("/auth/signup")
            print(f"✅ TEST CASE {test_num} PASSED: Signup without terms was correctly REJECTED")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Signup without terms was incorrectly accepted")
            take_screenshot_on_failure(self, "terms_not_accepted", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Signup without terms was incorrectly accepted - {e}")

    def test_mobile_empty(self):
        """Test: Mobile number field is EMPTY"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: Mobile number EMPTY")
        print("="*70)
        
        self.open_signup()
        self.type_text("input[name='firstName']", "Test")
        self.type_text("input[name='lastName']", "User")
        self.type_text("input[name='mobile']", "")  # ← EMPTY!
        self.type_text("input[name='email']", f"test_{int(time.time())}@test.com")
        self.type_text("input[name='password']", "TestPass@123")
        self.type_text("input[name='confirmPassword']", "TestPass@123")
        self.click_el("#toc")
        self.click_el("#sign_up_submit")
        self.sleep(2)
        
        try:
            self.assert_url_contains("/auth/signup")
            print(f"✅ TEST CASE {test_num} PASSED: Empty mobile was correctly REJECTED")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Empty mobile was incorrectly accepted")
            take_screenshot_on_failure(self, "mobile_empty", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Empty mobile was incorrectly accepted - {e}")


class TestLoginNegative(AuthFlow):
    """
    NEGATIVE LOGIN TESTS
    These tests should REJECT login attempts with invalid credentials
    Expected: User stays on login page with error
    """

    def test_login_empty_email(self):
        """Test: Login with EMPTY EMAIL"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: Login with EMPTY EMAIL")
        print("="*70)
        
        self.open_login()
        self.type_text("input[name='email']", "")  # ← EMPTY!
        self.type_text("input[name='password']", "TestPass@123")
        self.click_el("#kt_sign_in_submit")
        self.sleep(2)
        
        try:
            self.assert_url_contains("/auth/login")
            print(f"✅ TEST CASE {test_num} PASSED: Login with empty email was correctly REJECTED")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Login with empty email was incorrectly accepted")
            take_screenshot_on_failure(self, "login_empty_email", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Login with empty email was incorrectly accepted - {e}")

    def test_login_empty_password(self):
        """Test: Login with EMPTY PASSWORD"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: Login with EMPTY PASSWORD")
        print("="*70)
        
        self.open_login()
        self.type_text("input[name='email']", "test@test.com")
        self.type_text("input[name='password']", "")  # ← EMPTY!
        self.click_el("#kt_sign_in_submit")
        self.sleep(2)
        
        try:
            self.assert_url_contains("/auth/login")
            print(f"✅ TEST CASE {test_num} PASSED: Login with empty password was correctly REJECTED")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Login with empty password was incorrectly accepted")
            take_screenshot_on_failure(self, "login_empty_password", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Login with empty password was incorrectly accepted - {e}")

    def test_login_wrong_password(self):
        """Test: Login with WRONG PASSWORD"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: Login with WRONG PASSWORD")
        print("="*70)
        
        self.open_login()
        self.type_text("input[name='email']", Settings.VALID_EMAIL)
        self.type_text("input[name='password']", "WrongPassword@123")  # ← WRONG!
        self.click_el("#kt_sign_in_submit")
        self.sleep(2)
        
        try:
            self.assert_url_contains("/auth/login")
            print(f"✅ TEST CASE {test_num} PASSED: Login with wrong password was correctly REJECTED")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Login with wrong password was incorrectly accepted")
            take_screenshot_on_failure(self, "login_wrong_password", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Login with wrong password was incorrectly accepted - {e}")

    def test_login_nonexistent_user(self):
        """Test: Login with NON-EXISTENT USER"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: Login with NON-EXISTENT USER")
        print("="*70)
        
        self.open_login()
        self.type_text("input[name='email']", "nonexistent@nonexistent.com")  # ← DOESN'T EXIST!
        self.type_text("input[name='password']", "TestPass@123")
        self.click_el("#kt_sign_in_submit")
        self.sleep(2)
        
        try:
            self.assert_url_contains("/auth/login")
            print(f"✅ TEST CASE {test_num} PASSED: Login with non-existent user was correctly REJECTED")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Login with non-existent user was incorrectly accepted")
            take_screenshot_on_failure(self, "login_nonexistent_user", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Login with non-existent user was incorrectly accepted - {e}")

    def test_login_sql_injection(self):
        """Test: SQL INJECTION ATTEMPT"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: SQL INJECTION ATTACK PREVENTION")
        print("="*70)
        
        self.open_login()
        self.type_text("input[name='email']", "' OR '1'='1")  # ← SQL INJECTION!
        self.type_text("input[name='password']", "' OR '1'='1")  # ← SQL INJECTION!
        self.click_el("#kt_sign_in_submit")
        self.sleep(2)
        
        try:
            self.assert_url_contains("/auth/login")
            print(f"✅ TEST CASE {test_num} PASSED: SQL injection was correctly BLOCKED! ⭐ SECURE!")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: SQL injection was NOT blocked - SECURITY ISSUE!")
            take_screenshot_on_failure(self, "login_sql_injection", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - SQL injection was NOT blocked - SECURITY ISSUE! - {e}")


class TestSignupValidationEnhanced(AuthFlow):
    """
    ENHANCED VALIDATION TESTS
    Additional critical tests for security & data quality
    """

    def test_password_strength_weak(self):
        """Test: WEAK PASSWORD REJECTION (numbers only)"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: PASSWORD STRENGTH - WEAK (numbers only)")
        print("="*70)
        
        self.open_signup()
        self.type_text("input[name='firstName']", "Test")
        self.type_text("input[name='lastName']", "User")
        self.type_text("input[name='mobile']", "9876500020")
        self.type_text("input[name='email']", f"test_{int(time.time())}@test.com")
        self.type_text("input[name='password']", "123456")  # ← WEAK! Numbers only
        self.type_text("input[name='confirmPassword']", "123456")
        self.click_el("#toc")
        self.click_el("#sign_up_submit")
        self.sleep(2)
        
        try:
            self.assert_url_contains("/auth/signup")
            print(f"✅ TEST CASE {test_num} PASSED: Weak password correctly REJECTED ⭐ SECURE!")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Weak password was ACCEPTED - SECURITY ISSUE!")
            take_screenshot_on_failure(self, "password_strength_weak", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Weak password not validated - {e}")

    def test_email_case_insensitive(self):
        """Test: EMAIL CASE-INSENSITIVITY"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: EMAIL CASE-INSENSITIVITY")
        print("="*70)
        
        unique_timestamp = int(time.time())
        base_email = f"testuser_{unique_timestamp}@test.com"
        uppercase_email = base_email.upper()  # ← Uppercase variation
        
        print(f"Base email: {base_email}")
        print(f"Uppercase: {uppercase_email}")
        print("System should treat them as SAME email (case-insensitive)")
        
        self.open_signup()
        self.type_text("input[name='firstName']", "Test")
        self.type_text("input[name='lastName']", "User")
        self.type_text("input[name='mobile']", f"98765{unique_timestamp % 100000:05d}")
        self.type_text("input[name='email']", uppercase_email)  # ← UPPERCASE
        self.type_text("input[name='password']", "ValidPass@123")
        self.type_text("input[name='confirmPassword']", "ValidPass@123")
        self.click_el("#toc")
        self.click_el("#sign_up_submit")
        self.sleep(5)
        
        try:
            self.assert_url_contains("/verify-mobile")
            print(f"✅ TEST CASE {test_num} PASSED: Uppercase email accepted ✓ System is case-insensitive")
            # Now try lowercase version - should reject as duplicate
            self.logout()
            self.sleep(2)
            
            self.open_signup()
            self.type_text("input[name='firstName']", "Test2")
            self.type_text("input[name='lastName']", "User2")
            self.type_text("input[name='mobile']", f"98765{(unique_timestamp+1) % 100000:05d}")
            self.type_text("input[name='email']", base_email.lower())  # ← lowercase
            self.type_text("input[name='password']", "ValidPass@123")
            self.type_text("input[name='confirmPassword']", "ValidPass@123")
            self.click_el("#toc")
            self.click_el("#sign_up_submit")
            self.sleep(2)
            
            self.assert_url_contains("/auth/signup")
            print(f"   ✓ Lowercase rejected as duplicate - CORRECT! ⭐ GOOD!")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Email case sensitivity issue")
            take_screenshot_on_failure(self, "email_case_insensitive", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Email case handling failed - {e}")

    def test_xss_attack_prevention_name(self):
        """Test: XSS PREVENTION in name fields"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: XSS ATTACK PREVENTION (Name Fields)")
        print("="*70)
        
        self.open_signup()
        self.type_text("input[name='firstName']", "<script>alert('XSS')</script>")  # ← XSS!
        self.type_text("input[name='lastName']", "<img src=x onerror=alert('XSS')>")  # ← XSS!
        self.type_text("input[name='mobile']", "9876500021")
        self.type_text("input[name='email']", f"test_{int(time.time())}@test.com")
        self.type_text("input[name='password']", "ValidPass@123")
        self.type_text("input[name='confirmPassword']", "ValidPass@123")
        self.click_el("#toc")
        self.click_el("#sign_up_submit")
        self.sleep(2)
        
        try:
            self.assert_url_contains("/auth/signup")
            print(f"✅ TEST CASE {test_num} PASSED: XSS payload correctly BLOCKED ⭐ SECURE!")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: XSS was NOT blocked - SECURITY ISSUE!")
            take_screenshot_on_failure(self, "xss_attack_prevention", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - XSS not prevented - CRITICAL SECURITY ISSUE! - {e}")

    def test_mobile_format_validation(self):
        """Test: MOBILE NUMBER FORMAT VALIDATION"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: MOBILE NUMBER FORMAT VALIDATION")
        print("="*70)
        
        self.open_signup()
        self.type_text("input[name='firstName']", "Test")
        self.type_text("input[name='lastName']", "User")
        self.type_text("input[name='mobile']", "ABCDEFGHIJ")  # ← INVALID! Letters only
        self.type_text("input[name='email']", f"test_{int(time.time())}@test.com")
        self.type_text("input[name='password']", "ValidPass@123")
        self.type_text("input[name='confirmPassword']", "ValidPass@123")
        self.click_el("#toc")
        self.click_el("#sign_up_submit")
        self.sleep(2)
        
        try:
            self.assert_url_contains("/auth/signup")
            print(f"✅ TEST CASE {test_num} PASSED: Invalid mobile format correctly REJECTED")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Invalid mobile was ACCEPTED - DATA QUALITY ISSUE!")
            take_screenshot_on_failure(self, "mobile_format_invalid", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Mobile format validation missing - {e}")

    def test_duplicate_mobile_prevention(self):
        """Test: DUPLICATE MOBILE NUMBER PREVENTION"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: DUPLICATE MOBILE NUMBER PREVENTION")
        print("="*70)
        
        unique_mobile = f"98765{int(time.time()) % 100000:05d}"
        print(f"Using mobile: {unique_mobile}")
        print("Will try to register same mobile twice - should reject second attempt")
        
        # First registration with this mobile
        self.open_signup()
        self.type_text("input[name='firstName']", "Test")
        self.type_text("input[name='lastName']", "User")
        self.type_text("input[name='mobile']", unique_mobile)
        self.type_text("input[name='email']", f"test_{int(time.time())}@test.com")
        self.type_text("input[name='password']", "ValidPass@123")
        self.type_text("input[name='confirmPassword']", "ValidPass@123")
        self.click_el("#toc")
        self.click_el("#sign_up_submit")
        self.sleep(5)
        
        try:
            self.assert_url_contains("/verify-mobile")
            print(f"✓ First registration successful")
            
            # Logout and try second registration with same mobile
            self.logout()
            self.sleep(2)
            
            self.open_signup()
            self.type_text("input[name='firstName']", "Test2")
            self.type_text("input[name='lastName']", "User2")
            self.type_text("input[name='mobile']", unique_mobile)  # ← SAME MOBILE
            self.type_text("input[name='email']", f"test_{int(time.time())+1000}@test.com")
            self.type_text("input[name='password']", "ValidPass@123")
            self.type_text("input[name='confirmPassword']", "ValidPass@123")
            self.click_el("#toc")
            self.click_el("#sign_up_submit")
            self.sleep(2)
            
            self.assert_url_contains("/auth/signup")
            print(f"✅ TEST CASE {test_num} PASSED: Duplicate mobile correctly REJECTED ✓ GOOD!")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Duplicate mobile detection failed")
            take_screenshot_on_failure(self, "duplicate_mobile", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Duplicate mobile not detected - {e}")


class TestSignupPositive(AuthFlow):
    """
    POSITIVE SIGNUP TESTS
    These tests should SUCCEED and create an account
    Expected: User is redirected to /verify-mobile
    
    IMPORTANT: Each test generates unique email/mobile to avoid duplicates
    """
    
    # Store created credentials for login tests
    created_email = None
    created_password = None

    def test_create_account_all_valid(self):
        """Test: Create account with ALL VALID DATA"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: CREATE ACCOUNT - ALL VALID DATA")
        print("="*70)
        
        # Generate unique credentials
        unique_timestamp = int(time.time())
        email = f"testuser_{unique_timestamp}@test.com"
        password = "ValidPass@123"
        mobile = f"98765{unique_timestamp % 100000:05d}"
        
        print(f"Email: {email}")
        print(f"Mobile: {mobile}")
        print(f"Password: {'*' * len(password)}")
        
        self.open_signup()
        self.type_text("input[name='firstName']", "Test")
        self.type_text("input[name='lastName']", "User")
        self.type_text("input[name='mobile']", mobile)
        self.type_text("input[name='email']", email)
        self.type_text("input[name='password']", password)
        self.type_text("input[name='confirmPassword']", password)
        self.click_el("#toc")
        self.click_el("#sign_up_submit")
        self.sleep(5)
        
        try:
            self.assert_url_contains("/verify-mobile")
            print(f"✅ TEST CASE {test_num} PASSED: Account created successfully!")
            print("✓ Redirected to /verify-mobile")
            
            # Save credentials for next test
            TestSignupPositive.created_email = email
            TestSignupPositive.created_password = password
            
            # 💾 SAVE SESSION FOR OTHER MODULES
            SessionManager.save_session(email, password, "created")
            print(f"💾 Session saved! Other modules can now reuse this account.")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Account creation failed")
            take_screenshot_on_failure(self, "create_account_all_valid", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Account creation failed - {e}")

    def test_logout_from_verification(self):
        """Test: LOGOUT from mobile verification page"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: LOGOUT from /verify-mobile")
        print("="*70)
        
        print("Using URL: https://dev.v.shipgl.in/logout")
        
        self.logout()
        self.sleep(3)
        
        try:
            self.assert_url_contains("/auth/login")
            print(f"✅ TEST CASE {test_num} PASSED: Successfully logged out")
            print("✓ Redirected back to login page")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Logout failed")
            take_screenshot_on_failure(self, "logout_from_verification", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Logout failed - {e}")


class TestLoginPositive(AuthFlow):
    """
    POSITIVE LOGIN TESTS
    These tests should SUCCEED and allow user to login
    Expected: User is redirected to /verify-mobile or /dashboard
    """

    def test_login_system_valid_credentials(self):
        """Test: LOGIN with SYSTEM VALID CREDENTIALS"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: LOGIN - SYSTEM VALID CREDENTIALS")
        print("="*70)
        
        print(f"Email: {Settings.VALID_EMAIL}")
        print(f"Password: {'*' * len(Settings.VALID_PASSWORD)}")
        
        self.open_login()
        self.type_text("input[name='email']", Settings.VALID_EMAIL)
        self.type_text("input[name='password']", Settings.VALID_PASSWORD)
        self.click_el("#kt_sign_in_submit")
        self.sleep(5)
        
        current_url = self.get_current_url()
        print(f"Redirected to: {current_url}")
        
        try:
            if "/dashboard" in current_url:
                self.assert_url_contains("/dashboard")
                print(f"✅ TEST CASE {test_num} PASSED: Login successful!")
                print("✓ Redirected to /dashboard")
            elif "/verify-mobile" in current_url:
                self.assert_url_contains("/verify-mobile")
                print(f"✅ TEST CASE {test_num} PASSED: Login successful!")
                print("✓ Redirected to /verify-mobile (OTP required)")
            else:
                pytest.fail(f"Unexpected redirect: {current_url}")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Login failed")
            take_screenshot_on_failure(self, "login_system_valid_credentials", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Login failed - {e}")

    def test_logout_from_dashboard(self):
        """Test: LOGOUT from dashboard"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: LOGOUT from dashboard/verification")
        print("="*70)
        
        print("Using URL: https://dev.v.shipgl.in/logout")
        
        self.logout()
        self.sleep(3)
        
        try:
            self.assert_url_contains("/auth/login")
            print(f"✅ TEST CASE {test_num} PASSED: Successfully logged out")
            print("✓ Redirected back to login page")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Logout failed")
            take_screenshot_on_failure(self, "logout_from_dashboard", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Logout failed - {e}")

    def test_login_with_created_account(self):
        """Test: LOGIN with CREATED ACCOUNT CREDENTIALS"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: LOGIN - WITH CREATED ACCOUNT")
        print("="*70)
        
        if TestSignupPositive.created_email is None:
            pytest.skip("No created account available (run signup test first)")
        
        email = TestSignupPositive.created_email
        password = TestSignupPositive.created_password
        
        print(f"Email: {email}")
        print(f"Password: {'*' * len(password)}")
        
        self.open_login()
        self.type_text("input[name='email']", email)
        self.type_text("input[name='password']", password)
        self.click_el("#kt_sign_in_submit")
        self.sleep(5)
        
        current_url = self.get_current_url()
        print(f"Redirected to: {current_url}")
        
        try:
            self.assert_url_contains("/verify-mobile")
            print(f"✅ TEST CASE {test_num} PASSED: Login with created account successful!")
            print("✓ Redirected to /verify-mobile")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Login with created account failed")
            take_screenshot_on_failure(self, "login_with_created_account", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Login with created account failed - {e}")

    def test_final_logout(self):
        """Test: FINAL LOGOUT"""
        test_num = get_next_test_number()
        print("\n" + "="*70)
        print(f"🧪 TEST CASE {test_num}: FINAL LOGOUT")
        print("="*70)
        
        self.logout()
        self.sleep(3)
        
        try:
            self.assert_url_contains("/auth/login")
            print(f"✅ TEST CASE {test_num} PASSED: Final logout successful!")
        except Exception as e:
            print(f"\n❌ TEST CASE {test_num} FAILED: Final logout failed")
            take_screenshot_on_failure(self, "final_logout", test_num)
            pytest.fail(f"TEST CASE {test_num} FAILED - Final logout failed - {e}")
