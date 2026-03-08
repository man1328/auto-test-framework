"""
Automation Test Framework — Base Android Test Class (Appium)
All Android test classes should extend BaseAndroidTest.
"""
import pytest
import allure
from selenium.common.exceptions import WebDriverException

from core.logger import get_logger
from core import config

try:
    from appium import webdriver as appium_webdriver
    from appium.options.android.uiautomator2.base import UiAutomator2Options
    _APPIUM_AVAILABLE = True
except ImportError:
    _APPIUM_AVAILABLE = False
    appium_webdriver = None
    UiAutomator2Options = None


def _is_appium_running() -> bool:
    """Return True if Appium server is reachable at the configured URL."""
    import socket
    import urllib.parse
    url = config.APPIUM_SERVER_URL
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 4723
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except OSError:
        return False

log = get_logger(__name__)


class BaseAndroidTest:
    """
    Base class for all Appium Android tests.

    Usage:
        class TestLogin(BaseAndroidTest):
            def test_login_success(self):
                screen = LoginScreen(self.driver)
                screen.login("user", "pass")
                assert screen.is_home_visible()
    """

    driver = None

    @pytest.fixture(autouse=True)
    def setup_driver(self, request):
        """Set up Appium driver before each test, quit after."""
        if not _APPIUM_AVAILABLE:
            pytest.skip(
                "Appium client not installed. "
                "Run: pip install Appium-Python-Client"
            )
        if not _is_appium_running():
            pytest.skip(
                f"Appium server not running at {config.APPIUM_SERVER_URL}. "
                "Start it with: npx appium"
            )
        log.info(f"Starting Android test: {request.node.name}")
        options = self._build_options()
        try:
            self.driver = appium_webdriver.Remote(
                config.APPIUM_SERVER_URL, options=options
            )
            log.info(
                f"Driver started — device: {config.ANDROID_DEVICE_NAME}, "
                f"platform: {config.ANDROID_PLATFORM_VERSION}"
            )
        except WebDriverException as e:
            log.error(f"Failed to start Appium driver: {e}")
            pytest.fail(
                f"Cannot connect to Appium at {config.APPIUM_SERVER_URL}. "
                "Make sure Appium is running and a device/emulator is connected."
            )

        yield

        if self.driver:
            if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
                self._attach_screenshot_on_failure(request.node.name)
            self.driver.quit()
            log.info("Driver quit.")

    @staticmethod
    def _build_options() -> UiAutomator2Options:
        """Build Appium capabilities from config."""
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.platform_version = config.ANDROID_PLATFORM_VERSION
        options.device_name = config.ANDROID_DEVICE_NAME
        options.automation_name = config.ANDROID_AUTOMATION_NAME
        options.implicit_wait_timeout = config.IMPLICIT_WAIT * 1000  # ms

        if config.ANDROID_APP_PATH:
            options.app = config.ANDROID_APP_PATH
        elif config.ANDROID_APP_PACKAGE and config.ANDROID_APP_ACTIVITY:
            options.app_package = config.ANDROID_APP_PACKAGE
            options.app_activity = config.ANDROID_APP_ACTIVITY
        else:
            log.warning(
                "No app path or package/activity set. "
                "Set ANDROID_APP_PATH or ANDROID_APP_PACKAGE+ANDROID_APP_ACTIVITY in .env"
            )
        return options

    def _attach_screenshot_on_failure(self, test_name: str):
        try:
            screenshot = self.driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name=f"FAILURE_{test_name}",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as e:
            log.warning(f"Could not capture failure screenshot: {e}")


# ─── Hook to track test outcome ───────────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
