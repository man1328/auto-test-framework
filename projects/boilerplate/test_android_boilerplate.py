"""
╔══════════════════════════════════════════════════════════════════════╗
║       ANDROID TESTING — BOILERPLATE TEST SUITE                       ║
╠══════════════════════════════════════════════════════════════════════╣
║  HOW TO USE:                                                         ║
║  1. Set ANDROID_APP_PACKAGE + ANDROID_APP_ACTIVITY in .env           ║
║  2. Connect a device (adb devices) or start an emulator              ║
║  3. Replace every  ← TODO  comment with your real locators           ║
║     (Use Appium Inspector to find element IDs/accessibility IDs)     ║
║  4. Run: bash test.sh android                                        ║
╚══════════════════════════════════════════════════════════════════════╝
"""
import time
import pytest
import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from core.base_android_test import BaseAndroidTest


# ─── Fill these in using Appium Inspector ────────────────────────────────────
# Open Appium Inspector → connect to your device → click each element → copy ID

# Login Screen
EMAIL_FIELD        = (AppiumBy.ACCESSIBILITY_ID, "email_input")       # ← TODO
PASSWORD_FIELD     = (AppiumBy.ACCESSIBILITY_ID, "password_input")    # ← TODO
LOGIN_BUTTON       = (AppiumBy.ACCESSIBILITY_ID, "login_button")      # ← TODO
ERROR_MESSAGE      = (AppiumBy.ACCESSIBILITY_ID, "error_text")        # ← TODO
REMEMBER_ME_TOGGLE = (AppiumBy.ACCESSIBILITY_ID, "remember_me")       # ← TODO
LOGOUT_BUTTON      = (AppiumBy.ACCESSIBILITY_ID, "logout_button")     # ← TODO

# Home / Dashboard Screen
HOME_TITLE         = (AppiumBy.ACCESSIBILITY_ID, "home_title")        # ← TODO
NAV_TAB_1          = (AppiumBy.ACCESSIBILITY_ID, "tab_home")          # ← TODO
NAV_TAB_2          = (AppiumBy.ACCESSIBILITY_ID, "tab_profile")       # ← TODO
SCROLL_LIST        = (AppiumBy.ACCESSIBILITY_ID, "main_scroll_list")  # ← TODO

# Form Screen  (Registration/Edit Profile etc.)
FORM_NAME_FIELD    = (AppiumBy.ACCESSIBILITY_ID, "name_input")        # ← TODO
FORM_SUBMIT_BTN    = (AppiumBy.ACCESSIBILITY_ID, "submit_button")     # ← TODO
FORM_SUCCESS_MSG   = (AppiumBy.ACCESSIBILITY_ID, "success_message")   # ← TODO
KEYBOARD_DISMISS   = (AppiumBy.ACCESSIBILITY_ID, "main_content")      # ← TODO (area outside field)

# Notification
NOTIF_PERMISSION   = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button")

# Valid credentials
VALID_EMAIL    = "user@example.com"    # ← TODO
VALID_PASSWORD = "SecurePass123"       # ← TODO


def wait_for(driver, locator, timeout=10):
    """Wait for element to be visible and return it."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )


def is_visible(driver, locator, timeout=3):
    """Return True if element is visible within timeout."""
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
        return True
    except TimeoutException:
        return False


def do_login(driver):
    """Helper: perform a login flow for tests that need it."""
    wait_for(driver, EMAIL_FIELD).send_keys(VALID_EMAIL)
    driver.find_element(*PASSWORD_FIELD).send_keys(VALID_PASSWORD)
    driver.find_element(*LOGIN_BUTTON).click()
    wait_for(driver, HOME_TITLE, timeout=15)


# ══════════════════════════════════════════════════════════════════════════════
#  GROUP 1 — APP LAUNCH & STABILITY
# ══════════════════════════════════════════════════════════════════════════════
@allure.suite("Android — Boilerplate")
@allure.feature("App Stability")
@pytest.mark.android
class TestAppLaunch(BaseAndroidTest):

    @allure.title("App launches and shows first screen within 5 seconds")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_01_app_launches(self):
        """The app should open and display a screen within 5 seconds."""
        start = time.time()
        # Check for login screen or home screen — whichever comes first
        found = is_visible(self.driver, EMAIL_FIELD) or is_visible(self.driver, HOME_TITLE)
        elapsed = time.time() - start
        assert found, "App did not show a recognizable screen"
        assert elapsed < 5, f"App took {elapsed:.1f}s to load — expected < 5s"

    @allure.title("App survives screen rotation (portrait ↔ landscape)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_02_screen_rotation_no_crash(self):
        """Rotating the screen should not crash the app."""
        from appium.webdriver.common.mobileby import MobileBy
        self.driver.orientation = "LANDSCAPE"
        time.sleep(1)
        self.driver.orientation = "PORTRAIT"
        time.sleep(1)
        # App should still be alive — any element visible = pass
        found = is_visible(self.driver, EMAIL_FIELD) or is_visible(self.driver, HOME_TITLE)
        assert found, "App crashed or lost its screen after rotation"

    @allure.title("App survives background/foreground switch")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_03_background_foreground_no_crash(self):
        """Pressing home and returning should preserve the app state."""
        self.driver.background_app(3)   # put app in background for 3 seconds
        # App auto-comes back — verify it's still on a valid screen
        found = is_visible(self.driver, EMAIL_FIELD) or is_visible(self.driver, HOME_TITLE)
        assert found, "App crashed or didn't resume after backgrounding"

    @allure.title("App handles no network connection gracefully")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_04_no_network_no_crash(self):
        """With no WiFi/data, the app should show an error, not crash."""
        # Disable network
        self.driver.set_network_connection(0)   # 0 = no connection
        time.sleep(2)
        # ← TODO: trigger an action that requires network (e.g. tap refresh)
        # driver.find_element(*REFRESH_BUTTON).click()

        # Check app is still showing something (not crashed/blank)
        page_source = self.driver.page_source
        assert len(page_source) > 100, "App appears to have crashed (empty page source)"

        # Re-enable network for teardown
        self.driver.set_network_connection(6)   # 6 = WiFi + data


# ══════════════════════════════════════════════════════════════════════════════
#  GROUP 2 — LOGIN SCREEN
# ══════════════════════════════════════════════════════════════════════════════
@allure.suite("Android — Boilerplate")
@allure.feature("Login")
@pytest.mark.android
class TestAndroidLogin(BaseAndroidTest):

    @allure.title("Login screen is shown on first launch")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_05_login_screen_appears(self):
        """The login screen should be the first screen shown to a new user."""
        assert is_visible(self.driver, EMAIL_FIELD), "Email field not found on login screen"
        assert is_visible(self.driver, PASSWORD_FIELD), "Password field not found on login screen"
        assert is_visible(self.driver, LOGIN_BUTTON), "Login button not found on login screen"

    @allure.title("Valid credentials → home screen shown")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_06_valid_login_shows_home(self):
        """Logging in with correct credentials should show the home screen."""
        self.driver.find_element(*EMAIL_FIELD).send_keys(VALID_EMAIL)
        self.driver.find_element(*PASSWORD_FIELD).send_keys(VALID_PASSWORD)
        self.driver.find_element(*LOGIN_BUTTON).click()
        assert is_visible(self.driver, HOME_TITLE, timeout=15), \
            "Home screen did not appear after valid login"

    @allure.title("Wrong password shows error message")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_07_wrong_password_shows_error(self):
        """An incorrect password should show an error toast or message."""
        self.driver.find_element(*EMAIL_FIELD).send_keys(VALID_EMAIL)
        self.driver.find_element(*PASSWORD_FIELD).send_keys("totallyWrongPass!")
        self.driver.find_element(*LOGIN_BUTTON).click()
        assert is_visible(self.driver, ERROR_MESSAGE), "Error message should appear for wrong password"

    @allure.title("Empty email and password shows validation error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_08_empty_fields_show_validation(self):
        """Tapping login with no input should show a validation message."""
        self.driver.find_element(*LOGIN_BUTTON).click()
        assert is_visible(self.driver, ERROR_MESSAGE), "Validation error should appear for empty fields"

    @allure.title("Session persists after app restart (Remember Me)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_09_session_persists_after_restart(self):
        """If 'Remember Me' is checked, the user should still be logged in after restarting."""
        if not is_visible(self.driver, REMEMBER_ME_TOGGLE, timeout=2):
            pytest.skip("No 'Remember Me' toggle found — skipping")
        self.driver.find_element(*EMAIL_FIELD).send_keys(VALID_EMAIL)
        self.driver.find_element(*PASSWORD_FIELD).send_keys(VALID_PASSWORD)
        self.driver.find_element(*REMEMBER_ME_TOGGLE).click()   # enable remember me
        self.driver.find_element(*LOGIN_BUTTON).click()
        wait_for(self.driver, HOME_TITLE, timeout=15)
        # Restart app
        self.driver.background_app(-1)   # close
        time.sleep(2)
        self.driver.activate_app(self.driver.current_package)
        time.sleep(3)
        # Should still be on home screen, not login screen
        assert is_visible(self.driver, HOME_TITLE, timeout=5), \
            "User should still be logged in after restart with Remember Me"

    @allure.title("Logout returns to login screen")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_10_logout_returns_to_login(self):
        """Tapping logout should clear the session and show the login screen."""
        do_login(self.driver)
        self.driver.find_element(*LOGOUT_BUTTON).click()
        assert is_visible(self.driver, EMAIL_FIELD, timeout=10), \
            "Login screen should appear after logout"


# ══════════════════════════════════════════════════════════════════════════════
#  GROUP 3 — HOME / DASHBOARD NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
@allure.suite("Android — Boilerplate")
@allure.feature("Navigation")
@pytest.mark.android
class TestAndroidNavigation(BaseAndroidTest):

    @allure.title("Tab 1 opens first section")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_11_nav_tab_1_works(self):
        """Tapping the first nav tab should open its screen."""
        do_login(self.driver)
        self.driver.find_element(*NAV_TAB_1).click()
        # ← TODO: replace HOME_TITLE with the element unique to Tab 1's screen
        assert is_visible(self.driver, HOME_TITLE), "Tab 1 screen not shown"

    @allure.title("Tab 2 opens second section")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_12_nav_tab_2_works(self):
        """Tapping the second nav tab should open its screen."""
        do_login(self.driver)
        self.driver.find_element(*NAV_TAB_2).click()
        time.sleep(1)
        # ← TODO: replace with locator unique to Tab 2's screen
        assert self.driver.page_source is not None, "Tab 2 did not load"

    @allure.title("Back button returns to previous screen")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_13_back_button_works(self):
        """Pressing the Android back button should return to the previous screen."""
        do_login(self.driver)
        self.driver.find_element(*NAV_TAB_2).click()
        time.sleep(1)
        self.driver.back()
        assert is_visible(self.driver, HOME_TITLE, timeout=5), \
            "Back button should return to home screen"

    @allure.title("Back button on home minimizes the app")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_14_back_on_home_minimizes_app(self):
        """Pressing back on the home screen should exit/minimize, not crash."""
        do_login(self.driver)
        self.driver.back()
        time.sleep(1)
        # App should still be alive (not display an error)
        assert self.driver.page_source is not None

    @allure.title("Main list scrolls without crashing")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_15_list_scrolls_smoothly(self):
        """Scrolling through the main content list should not crash the app."""
        do_login(self.driver)
        if not is_visible(self.driver, SCROLL_LIST, timeout=5):
            pytest.skip("No scrollable list found on home screen")
        # Swipe up 3 times to scroll down
        for _ in range(3):
            self.swipe_up()
            time.sleep(0.5)
        assert self.driver.page_source is not None, "App crashed during scroll"


# ══════════════════════════════════════════════════════════════════════════════
#  GROUP 4 — FORMS & KEYBOARD
# ══════════════════════════════════════════════════════════════════════════════
@allure.suite("Android — Boilerplate")
@allure.feature("Forms")
@pytest.mark.android
class TestAndroidForms(BaseAndroidTest):

    @allure.title("Tapping text field opens the keyboard")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_16_tapping_field_opens_keyboard(self):
        """Tapping an input field should open the on-screen keyboard."""
        wait_for(self.driver, EMAIL_FIELD).click()
        assert self.driver.is_keyboard_shown(), "Keyboard should appear after tapping a field"

    @allure.title("Tapping outside field dismisses keyboard")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_17_tapping_outside_dismisses_keyboard(self):
        """Tapping outside an active text field should hide the keyboard."""
        wait_for(self.driver, EMAIL_FIELD).click()
        assert self.driver.is_keyboard_shown(), "Keyboard should open first"
        # Tap outside the field to dismiss
        self.driver.find_element(*KEYBOARD_DISMISS).click()
        time.sleep(0.5)
        assert not self.driver.is_keyboard_shown(), "Keyboard should hide after tapping outside"

    @allure.title("Submitting empty form shows validation errors")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_18_empty_form_shows_errors(self):
        """Submitting a required form with no data should show validation errors."""
        do_login(self.driver)
        if not is_visible(self.driver, FORM_SUBMIT_BTN, timeout=3):
            pytest.skip("No form submit button visible — navigate to form screen first")
        self.driver.find_element(*FORM_SUBMIT_BTN).click()
        assert is_visible(self.driver, ERROR_MESSAGE), "Validation error should appear for empty form"

    @allure.title("Valid form submission shows success message")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_19_valid_form_submission_succeeds(self):
        """Filling in a valid form and submitting should show a success message."""
        do_login(self.driver)
        if not is_visible(self.driver, FORM_NAME_FIELD, timeout=3):
            pytest.skip("Form fields not visible — navigate to the form screen first")
        self.driver.find_element(*FORM_NAME_FIELD).clear()
        self.driver.find_element(*FORM_NAME_FIELD).send_keys("Test User")
        self.driver.find_element(*FORM_SUBMIT_BTN).click()
        assert is_visible(self.driver, FORM_SUCCESS_MSG, timeout=10), \
            "Success message should appear after valid form submission"

    @allure.title("Notification permission dialog can be accepted")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_20_notification_permission_accepted(self):
        """If the app requests notification permission, it can be granted."""
        if not is_visible(self.driver, NOTIF_PERMISSION, timeout=3):
            pytest.skip("No notification permission dialog appeared — skipping")
        self.driver.find_element(*NOTIF_PERMISSION).click()
        time.sleep(0.5)
        # Dialog should be gone
        assert not is_visible(self.driver, NOTIF_PERMISSION, timeout=2), \
            "Permission dialog should close after accepting"
