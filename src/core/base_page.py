from seleniumbase import BaseCase
from configs.settings import Settings

class BasePage(BaseCase):

    def open_url(self, path: str):
        """Open URL with proper BASE_URL handling"""
        try:
            # Always ensure BASE_URL is available
            base_url = getattr(Settings, 'BASE_URL', 'https://dev.v.shipgl.in')
            
            # If path is a full URL, use it directly, otherwise append to base URL
            if path.startswith('http'):
                url = path
            else:
                url = base_url + path
            
            print(f"🌐 Opening URL: {url}")
            self.open(url)
            self.sleep(2)  # Wait for page to load
        except Exception as e:
            print(f"❌ Error opening URL: {e}")
            raise

    def type_text(self, locator, value):
        self.type(locator, value)

    def click_el(self, locator):
        self.click(locator)

    def assert_visible(self, locator):
        self.assert_element_visible(locator)

    def verify_dashboard(self):
        """Verify user is on dashboard"""
        self.sleep(2)  # Wait for redirect
        self.assert_url_contains("/dashboard")

    def verify_login_page(self):
        """Verify user is on login page"""
        self.sleep(2)  # Wait for redirect
        self.assert_url_contains("/auth/login")

    def logout(self):
        """Logout user by navigating to logout URL"""
        self.open_url("/logout")
        self.sleep(3)  # Wait for logout to complete
        try:
            self.verify_login_page()
        except:
            pass

    def verify_mobile_verification_page(self):
        """Verify user is on mobile verification page"""
        self.sleep(2)
        self.assert_url_contains("/verify-mobile")
    
    def get_current_url(self):
        """Get the current page URL"""
        return self.driver.current_url
