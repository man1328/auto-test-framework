"""
LoginPage Page Object — Example Web Project
Demonstrates web POM using Selenium + BasePage.
"""
from selenium.webdriver.common.by import By
import allure

from core.page_object import BasePage


class _Locators:
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message, [data-testid='error']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title, [data-testid='dashboard']")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot password?")


class LoginPage(BasePage):
    """
    Login Page — covers login form interactions.
    URL: /login (relative to BASE_URL in config)
    """

    PAGE_URL = "/login"

    @allure.step("Enter email: {email}")
    def enter_email(self, email: str):
        self.type_text(_Locators.EMAIL_INPUT, email)

    @allure.step("Enter password")
    def enter_password(self, password: str):
        self.type_text(_Locators.PASSWORD_INPUT, password)

    @allure.step("Click Login button")
    def click_login(self):
        self.click(_Locators.LOGIN_BUTTON)

    @allure.step("Login with email='{email}'")
    def login(self, email: str, password: str):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def is_error_displayed(self) -> bool:
        return self.is_visible(_Locators.ERROR_MESSAGE, timeout=5)

    def get_error_text(self) -> str:
        return self.get_text(_Locators.ERROR_MESSAGE)

    def is_dashboard_displayed(self) -> bool:
        return self.is_visible(_Locators.DASHBOARD_HEADER, timeout=10)

    @allure.step("Click 'Forgot Password?' link")
    def click_forgot_password(self):
        self.click(_Locators.FORGOT_PASSWORD_LINK)
