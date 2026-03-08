"""
Example Android Tests — Home Screen
Run: pytest projects/example_android/tests/ -m android -v

Prerequisites:
  1. Appium 2 running: npx appium
  2. Android device or emulator connected
  3. Set ANDROID_APP_PATH (or ANDROID_APP_PACKAGE + ANDROID_APP_ACTIVITY) in .env
"""
import pytest
import allure

from core.base_android_test import BaseAndroidTest
from projects.example_android.screens.home_screen import HomeScreen


@allure.suite("Android — Home Screen")
@allure.feature("Home Screen")
@pytest.mark.android
class TestHomeScreen(BaseAndroidTest):
    """Tests for the Home Screen of the example Android app."""

    @allure.title("App launches and Home Screen is visible")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_home_screen_displays(self):
        """Verify that the app launches successfully and shows the home screen."""
        screen = HomeScreen(self.driver)
        assert screen.is_displayed(), "Home Screen was not visible after app launch"

    @allure.title("Welcome message contains expected text")
    @allure.severity(allure.severity_level.NORMAL)
    def test_welcome_text(self):
        """Verify the welcome message text."""
        screen = HomeScreen(self.driver)
        text = screen.get_welcome_text()
        assert text, "Welcome text was empty"
        assert len(text) > 0, "Welcome text should not be empty"

    @allure.title("Search bar accepts input")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("query", ["Python", "Automation", "Appium"])
    def test_search_accepts_input(self, query):
        """Verify that the search bar accepts various text inputs."""
        screen = HomeScreen(self.driver)
        screen.search(query)
        # In a real test, verify search results appear
        screen.take_screenshot(f"search_{query}")

    @allure.title("User can scroll the home screen")
    @allure.severity(allure.severity_level.MINOR)
    def test_scroll_home_screen(self):
        """Verify the home screen is scrollable."""
        screen = HomeScreen(self.driver)
        screen.scroll_and_screenshot()
        # Verify app didn't crash — home screen still reachable
        screen.swipe_down()
        assert screen.is_displayed(), "App may have crashed after scrolling"
