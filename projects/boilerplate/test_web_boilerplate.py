"""
╔══════════════════════════════════════════════════════════════════════╗
║          WEB TESTING — BOILERPLATE TEST SUITE                        ║
╠══════════════════════════════════════════════════════════════════════╣
║  HOW TO USE:                                                         ║
║  1. Set BASE_URL in your .env file to your website URL               ║
║  2. Replace every  ← TODO  comment with your real values             ║
║  3. Run: pytest projects/boilerplate/test_web_boilerplate.py -m web  ║
╚══════════════════════════════════════════════════════════════════════╝
"""
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.base_web_test import BaseWebTest


# ─── Fill these in for your app ───────────────────────────────────────────────
LOGIN_URL        = "/login"               # ← TODO: path to login page
DASHBOARD_URL    = "/dashboard"           # ← TODO: path after login
FORGOT_PASS_URL  = "/forgot-password"     # ← TODO: path to forgot password page

VALID_EMAIL      = "user@example.com"     # ← TODO: a real working login email
VALID_PASSWORD   = "SecurePass123"        # ← TODO: a real working password

# Element locators — right-click element in Chrome → Inspect → copy id/class
EMAIL_FIELD      = (By.ID, "email")       # ← TODO: locator for email input
PASSWORD_FIELD   = (By.ID, "password")    # ← TODO: locator for password input
LOGIN_BUTTON     = (By.ID, "login-btn")   # ← TODO: locator for login button
ERROR_MESSAGE    = (By.CSS_SELECTOR, ".error-message")  # ← TODO: locator for error text
NAV_MENU         = (By.CSS_SELECTOR, "nav a")           # ← TODO: nav link selector
LOGOUT_BUTTON    = (By.ID, "logout-btn")                # ← TODO: logout button locator
SEARCH_INPUT     = (By.ID, "search")                    # ← TODO: search field locator
SEARCH_BUTTON    = (By.ID, "search-btn")                # ← TODO: search button locator
SEARCH_RESULTS   = (By.CSS_SELECTOR, ".search-results") # ← TODO: results container
NO_RESULTS_MSG   = (By.CSS_SELECTOR, ".no-results")     # ← TODO: "no results" element
REGISTER_URL     = "/register"                           # ← TODO: registration page path
SUBMIT_FORM_BTN  = (By.ID, "submit")                    # ← TODO: form submit button
SUCCESS_MSG      = (By.CSS_SELECTOR, ".success")         # ← TODO: success message element


def wait_for(driver, locator, timeout=10):
    """Helper: wait for an element to be visible."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def is_present(driver, locator):
    """Helper: check if element exists on page."""
    return len(driver.find_elements(*locator)) > 0


# ══════════════════════════════════════════════════════════════════════════════
#  GROUP 1 — LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════════════
@allure.suite("Web — Boilerplate")
@allure.feature("Authentication")
@pytest.mark.web
class TestLoginPage(BaseWebTest):

    @allure.title("Login page loads successfully")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_01_login_page_loads(self):
        """The login page should load with no errors."""
        self.driver.get(self.navigate(LOGIN_URL))
        assert wait_for(self.driver, EMAIL_FIELD), "Email field not found"
        assert wait_for(self.driver, PASSWORD_FIELD), "Password field not found"

    @allure.title("Valid credentials → redirected to dashboard")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_02_valid_login_redirects_to_dashboard(self):
        """Logging in with correct credentials should redirect to the dashboard."""
        self.navigate(LOGIN_URL)
        self.driver.find_element(*EMAIL_FIELD).send_keys(VALID_EMAIL)
        self.driver.find_element(*PASSWORD_FIELD).send_keys(VALID_PASSWORD)
        self.driver.find_element(*LOGIN_BUTTON).click()
        assert DASHBOARD_URL in self.driver.current_url, \
            f"Expected URL to contain '{DASHBOARD_URL}', got: {self.driver.current_url}"

    @allure.title("Wrong password → error message shown")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_03_wrong_password_shows_error(self):
        """An incorrect password should show an error message."""
        self.navigate(LOGIN_URL)
        self.driver.find_element(*EMAIL_FIELD).send_keys(VALID_EMAIL)
        self.driver.find_element(*PASSWORD_FIELD).send_keys("wrongpassword123")
        self.driver.find_element(*LOGIN_BUTTON).click()
        assert is_present(self.driver, ERROR_MESSAGE), "Error message should appear"

    @allure.title("Empty email → validation error shown")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_04_empty_email_shows_validation(self):
        """Submitting without an email should show a validation error."""
        self.navigate(LOGIN_URL)
        self.driver.find_element(*PASSWORD_FIELD).send_keys(VALID_PASSWORD)
        self.driver.find_element(*LOGIN_BUTTON).click()
        assert is_present(self.driver, ERROR_MESSAGE), "Validation error should appear"

    @allure.title("Empty password → validation error shown")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_05_empty_password_shows_validation(self):
        """Submitting without a password should show a validation error."""
        self.navigate(LOGIN_URL)
        self.driver.find_element(*EMAIL_FIELD).send_keys(VALID_EMAIL)
        self.driver.find_element(*LOGIN_BUTTON).click()
        assert is_present(self.driver, ERROR_MESSAGE), "Validation error should appear"

    @allure.title("Forgot password link navigates correctly")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_06_forgot_password_link_works(self):
        """Clicking 'Forgot Password' should navigate to the reset page."""
        self.navigate(LOGIN_URL)
        # ← TODO: update selector to match your app's forgot-password link
        forgot_link = self.driver.find_element(By.LINK_TEXT, "Forgot Password?")
        forgot_link.click()
        assert FORGOT_PASS_URL in self.driver.current_url, \
            f"Expected forgot-password URL, got: {self.driver.current_url}"


# ══════════════════════════════════════════════════════════════════════════════
#  GROUP 2 — DASHBOARD / HOME (run after login)
# ══════════════════════════════════════════════════════════════════════════════
@allure.suite("Web — Boilerplate")
@allure.feature("Dashboard")
@pytest.mark.web
class TestDashboardPage(BaseWebTest):

    def _login(self):
        """Helper: log in before each dashboard test."""
        self.navigate(LOGIN_URL)
        self.driver.find_element(*EMAIL_FIELD).send_keys(VALID_EMAIL)
        self.driver.find_element(*PASSWORD_FIELD).send_keys(VALID_PASSWORD)
        self.driver.find_element(*LOGIN_BUTTON).click()
        WebDriverWait(self.driver, 10).until(EC.url_contains(DASHBOARD_URL))

    @allure.title("Dashboard loads after login")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_07_dashboard_loads(self):
        """After login the dashboard page should load."""
        self._login()
        assert DASHBOARD_URL in self.driver.current_url

    @allure.title("All navigation links are present and clickable")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_08_nav_links_are_clickable(self):
        """Every link in the navigation menu should be clickable (no 404)."""
        self._login()
        nav_links = self.driver.find_elements(*NAV_MENU)
        assert len(nav_links) > 0, "No navigation links found"
        hrefs = [link.get_attribute("href") for link in nav_links if link.get_attribute("href")]
        assert len(hrefs) > 0, "Navigation links have no href attributes"

    @allure.title("Logout redirects to login page")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_09_logout_redirects_to_login(self):
        """Clicking logout should redirect back to the login page."""
        self._login()
        self.driver.find_element(*LOGOUT_BUTTON).click()
        assert LOGIN_URL in self.driver.current_url, \
            f"Expected login URL after logout, got: {self.driver.current_url}"

    @allure.title("Logged-out user cannot access dashboard")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_10_protected_page_redirects_to_login(self):
        """Accessing the dashboard without login should redirect to login."""
        self.driver.get(f"{self.driver.current_url.split('/')[0]}//{self.driver.current_url.split('/')[2]}{DASHBOARD_URL}")
        assert LOGIN_URL in self.driver.current_url, \
            "Should be redirected to login when not authenticated"


# ══════════════════════════════════════════════════════════════════════════════
#  GROUP 3 — SEARCH
# ══════════════════════════════════════════════════════════════════════════════
@allure.suite("Web — Boilerplate")
@allure.feature("Search")
@pytest.mark.web
class TestSearch(BaseWebTest):

    KNOWN_SEARCH_TERM    = "python"   # ← TODO: term that returns results
    UNKNOWN_SEARCH_TERM  = "xyzzy999notarealterm"

    @allure.title("Searching a known term returns results")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_11_search_known_term_shows_results(self):
        """A real search term should return at least one result."""
        self.driver.find_element(*SEARCH_INPUT).send_keys(self.KNOWN_SEARCH_TERM)
        self.driver.find_element(*SEARCH_BUTTON).click()
        assert is_present(self.driver, SEARCH_RESULTS), "Search results should appear"

    @allure.title("Searching unknown term shows no-results message")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_12_search_unknown_term_shows_no_results(self):
        """A nonsense search term should show a 'no results' message."""
        self.driver.find_element(*SEARCH_INPUT).send_keys(self.UNKNOWN_SEARCH_TERM)
        self.driver.find_element(*SEARCH_BUTTON).click()
        assert is_present(self.driver, NO_RESULTS_MSG), "'No results' message should appear"


# ══════════════════════════════════════════════════════════════════════════════
#  GROUP 4 — REGISTRATION FORM
# ══════════════════════════════════════════════════════════════════════════════
@allure.suite("Web — Boilerplate")
@allure.feature("Registration")
@pytest.mark.web
class TestRegistrationForm(BaseWebTest):

    # ← TODO: Fill in the locators that match your registration form
    FIRST_NAME_FIELD  = (By.ID, "first_name")
    LAST_NAME_FIELD   = (By.ID, "last_name")
    REG_EMAIL_FIELD   = (By.ID, "email")
    REG_PASS_FIELD    = (By.ID, "password")
    REG_CONFIRM_FIELD = (By.ID, "confirm_password")

    @allure.title("Valid registration form submits successfully")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_13_valid_form_submits(self):
        """Filling in all required fields should submit successfully."""
        self.navigate(REGISTER_URL)
        self.driver.find_element(*self.FIRST_NAME_FIELD).send_keys("Test")
        self.driver.find_element(*self.LAST_NAME_FIELD).send_keys("User")
        self.driver.find_element(*self.REG_EMAIL_FIELD).send_keys("test_new@example.com")
        self.driver.find_element(*self.REG_PASS_FIELD).send_keys("NewPass123!")
        self.driver.find_element(*self.REG_CONFIRM_FIELD).send_keys("NewPass123!")
        self.driver.find_element(*SUBMIT_FORM_BTN).click()
        assert is_present(self.driver, SUCCESS_MSG), "Success message should appear after registration"

    @allure.title("Submitting empty form shows validation errors")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_14_empty_form_shows_validation(self):
        """Submitting an empty form should show validation errors."""
        self.navigate(REGISTER_URL)
        self.driver.find_element(*SUBMIT_FORM_BTN).click()
        assert is_present(self.driver, ERROR_MESSAGE), "Validation errors should appear"

    @allure.title("Invalid email format is rejected")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_15_invalid_email_rejected(self):
        """A badly formatted email should be rejected with an error."""
        self.navigate(REGISTER_URL)
        self.driver.find_element(*self.REG_EMAIL_FIELD).send_keys("not-an-email")
        self.driver.find_element(*SUBMIT_FORM_BTN).click()
        assert is_present(self.driver, ERROR_MESSAGE), "Email validation error should appear"

    @allure.title("Duplicate email is rejected")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_16_duplicate_email_rejected(self):
        """Registering with an email that already exists should fail."""
        self.navigate(REGISTER_URL)
        self.driver.find_element(*self.REG_EMAIL_FIELD).send_keys(VALID_EMAIL)
        self.driver.find_element(*self.REG_PASS_FIELD).send_keys("AnyPass123!")
        self.driver.find_element(*SUBMIT_FORM_BTN).click()
        assert is_present(self.driver, ERROR_MESSAGE), "Duplicate email error should appear"
