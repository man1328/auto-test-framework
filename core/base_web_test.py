"""
Automation Test Framework — Base Web Test Class (Selenium)
All Web test classes should extend BaseWebTest.
"""
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# Selenium 4.6+ includes Selenium Manager which auto-downloads the correct
# driver version for your installed browser — no webdriver-manager needed.
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from core.logger import get_logger
from core import config

log = get_logger(__name__)


class BaseWebTest:
    """
    Base class for all Selenium web tests.

    Usage:
        class TestLogin(BaseWebTest):
            def test_login(self):
                self.driver.get("https://example.com/login")
                page = LoginPage(self.driver)
                page.login("user@example.com", "password")
    """

    driver = None

    @pytest.fixture(autouse=True)
    def setup_driver(self, request):
        """Create WebDriver before each test, quit after."""
        # Skip gracefully if BASE_URL is still the default placeholder
        if config.BASE_URL in ("https://example.com", "http://example.com", ""):
            pytest.skip(
                f"BASE_URL is not configured (current: {config.BASE_URL!r}). "
                "Set BASE_URL in your .env to the target web application URL."
            )
        log.info(f"Starting web test: {request.node.name} | browser: {config.BROWSER}")
        self.driver = self._create_driver()
        self.driver.maximize_window()
        yield
        if self.driver:
            if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
                self._attach_screenshot_on_failure(request.node.name)
            self.driver.quit()
            log.info("WebDriver quit.")

    @staticmethod
    def _create_driver():
        browser = config.BROWSER.lower()
        if browser == "chrome":
            opts = ChromeOptions()
            if config.HEADLESS:
                opts.add_argument("--headless=new")
            opts.add_argument("--no-sandbox")
            opts.add_argument("--disable-dev-shm-usage")
            opts.add_argument("--window-size=1920,1080")
            # ChromeService() with no args lets Selenium Manager auto-download
            # the correct ChromeDriver for your installed Chrome version
            return webdriver.Chrome(service=ChromeService(), options=opts)
        elif browser == "firefox":
            opts = FirefoxOptions()
            if config.HEADLESS:
                opts.add_argument("--headless")
            return webdriver.Firefox(service=FirefoxService(), options=opts)
        else:
            raise ValueError(f"Unsupported browser: {browser}. Use 'chrome' or 'firefox'.")

    def _attach_screenshot_on_failure(self, test_name: str):
        try:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=f"FAILURE_{test_name}",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as e:
            log.warning(f"Could not capture failure screenshot: {e}")

    def navigate(self, url: str):
        """Navigate to a URL (relative to BASE_URL or absolute)."""
        target = url if url.startswith("http") else f"{config.BASE_URL.rstrip('/')}/{url.lstrip('/')}"
        log.info(f"Navigating to: {target}")
        self.driver.get(target)
