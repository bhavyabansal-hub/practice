import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class DriverFactory:
    @staticmethod
    def create_driver(headless=True):
        chrome_options = Options()

        if headless:
            chrome_options.add_argument("--headless=new")

        # ---------------- BASIC STABILITY ----------------
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # ---------------- 🔥 KILL PASSWORD POPUPS 🔥 ----------------
        chrome_options.add_argument("--disable-features=PasswordLeakDetection")
        chrome_options.add_argument("--disable-save-password-bubble")
        chrome_options.add_argument("--disable-password-manager-reauthentication")

        chrome_options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.default_content_setting_values.notifications": 2,
            }
        )

        # ---------------- 🔥 MOST IMPORTANT PART 🔥 ----------------
        # USE A FRESH TEMP CHROME PROFILE (NO GOOGLE DATA, NO PASSWORDS)
        temp_profile = tempfile.mkdtemp()
        chrome_options.add_argument(f"--user-data-dir={temp_profile}")

        # ---------------- DRIVER ----------------
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        return driver
