"""
Example Web Tests — Login Page
Run: pytest projects/example_web/tests/ -m web -v

Prerequisites:
  - Chrome or Firefox installed
  - Set BASE_URL in .env to target the app under test
  - Set HEADLESS=false in .env to watch the browser
"""
import pytest
import allure
from pathlib import Path
import yaml

from core.base_web_test import BaseWebTest
from projects.example_web.pages.login_page import LoginPage


def load_login_data():
    data_file = Path(__file__).parent.parent / "test_data" / "login_data.yml"
    return yaml.safe_load(data_file.read_text())


@allure.suite("Web — Authentication")
@allure.feature("Login Page")
@pytest.mark.web
class TestLoginPage(BaseWebTest):
    """Tests for the Login page of the example web application."""

    @allure.title("Login page loads successfully")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_login_page_loads(self):
        """Verify that navigating to /login shows the login form."""
        self.navigate("/login")
        page = LoginPage(self.driver)
        assert page.is_visible(("id", "email")), "Email field not found on login page"
        assert page.is_visible(("id", "password")), "Password field not found"

    @allure.title("Valid credentials redirects to dashboard")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_valid_login(self):
        """Verify that a valid user can log in and reaches the dashboard."""
        data = load_login_data()["valid"]
        self.navigate("/login")
        page = LoginPage(self.driver)
        page.login(data["email"], data["password"])
        assert page.is_dashboard_displayed(), (
            "Dashboard did not appear after valid login"
        )

    @allure.title("Invalid credentials shows error message")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("email,password,description", [
        ("wrong@example.com", "wrongpass", "wrong email and password"),
        ("valid@example.com", "wrongpass", "correct email but wrong password"),
        ("", "somepass", "empty email"),
        ("valid@example.com", "", "empty password"),
    ])
    @pytest.mark.regression
    def test_invalid_login(self, email, password, description):
        """Verify that invalid credentials show an appropriate error."""
        self.navigate("/login")
        page = LoginPage(self.driver)
        page.login(email, password)
        assert page.is_error_displayed(), (
            f"Error message not shown for: {description}"
        )

    @allure.title("Forgot password link is clickable")
    @allure.severity(allure.severity_level.MINOR)
    def test_forgot_password_link(self):
        """Verify the 'Forgot password?' link is present and clickable."""
        self.navigate("/login")
        page = LoginPage(self.driver)
        assert page.is_present(("link text", "Forgot password?")), (
            "Forgot password link not found"
        )
