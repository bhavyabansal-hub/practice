from src.core.base_page import BasePage
from src.locators.authentication_locators import LegalConsentLocators

class LegalConsentModal(BasePage):

    def accept_terms(self):
        self.click_el(LegalConsentLocators.ACCEPT_BUTTON)
