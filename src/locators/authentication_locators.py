class LoginLocators:
    EMAIL = "input[name='email']"
    PASSWORD = "input[name='password']"
    SUBMIT = "#kt_sign_in_submit"
    CREATE_ACCOUNT_LINK = "a[href*='signup']"
    FORGOT_PASSWORD_LINK = "a[href*='forgot']"
    ERROR_MSG = ".error-msg"

class SignupLocators:
    FIRST_NAME = "input[name='firstName']"
    LAST_NAME = "input[name='lastName']"
    MOBILE = "input[name='mobile']"
    EMAIL = "input[name='email']"
    PASSWORD = "input[name='password']"
    CONFIRM_PASSWORD = "input[name='confirmPassword']"
    REFERRAL_CODE = "input[name='referral_code']"
    TERMS_CHECKBOX = "#toc"
    SUBMIT = "#sign_up_submit"
    LOGIN_LINK = "a[href*='login']"
    ERROR_MSG = ".error-msg"

class ForgotPasswordLocators:
    EMAIL = "input[name='email']"
    SUBMIT = "button[type='submit']"
    SUCCESS_MSG = ".success-msg"
    ERROR_MSG = ".error-msg"

class MobileVerificationLocators:
    OTP_INPUT = "input[name='otp']"
    SUBMIT = "button[type='submit']"
    ERROR_MSG = ".error-msg"

class LegalConsentLocators:
    ACCEPT_BUTTON = "button.accept-terms"

class LogoutLocators:
    LOGOUT_BUTTON = "button[data-logout], a[data-logout], button:contains('Logout'), a:contains('Logout'), [role='menuitem']:contains('Logout')"
