"""
HomeScreen Page Object — Example Android Project
Demonstrates how to create screen objects using the POM pattern.
"""
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
import allure

from core.page_object import BasePage


# ─── Locators (separate from logic for easy maintenance) ──────────────────────
class _Locators:
    WELCOME_TEXT = (AppiumBy.ACCESSIBILITY_ID, "welcome_text")
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "login_button")
    MENU_ICON = (AppiumBy.ACCESSIBILITY_ID, "menu_icon")
    SEARCH_BAR = (AppiumBy.XPATH, "//android.widget.EditText[@content-desc='search']")
    FIRST_LIST_ITEM = (AppiumBy.XPATH, "(//android.widget.TextView)[1]")


class HomeScreen(BasePage):
    """
    Represents the Home Screen of the Android app.
    Each method represents a user action or state verification.
    """

    @allure.step("Verify Home Screen is displayed")
    def is_displayed(self) -> bool:
        return self.is_visible(_Locators.WELCOME_TEXT)

    @allure.step("Get welcome message text")
    def get_welcome_text(self) -> str:
        return self.get_text(_Locators.WELCOME_TEXT)

    @allure.step("Tap Login button")
    def tap_login(self):
        self.click(_Locators.LOGIN_BUTTON)

    @allure.step("Open side menu")
    def open_menu(self):
        self.click(_Locators.MENU_ICON)

    @allure.step("Search for '{query}'")
    def search(self, query: str):
        self.type_text(_Locators.SEARCH_BAR, query)

    @allure.step("Get first list item text")
    def get_first_item(self) -> str:
        return self.get_text(_Locators.FIRST_LIST_ITEM)

    @allure.step("Scroll down and take screenshot")
    def scroll_and_screenshot(self):
        self.swipe_up(swipes=2)
        self.take_screenshot("home_scrolled")
