"""
Automation Test Framework — Page Object Model Base Class
All screen/page objects extend this class.
"""
from __future__ import annotations
from typing import List, Tuple
import time
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from core.logger import get_logger
from core import config

log = get_logger(__name__)


class BasePage:
    """
    Base class for all Page Objects.
    Works with both Appium (mobile) and Selenium (web) drivers.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)

    # ─── Element Finders ──────────────────────────────────────────────────────

    def find(self, locator: Tuple[str, str]):
        """Find a single element (explicit wait)."""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            log.error(f"Element not found: {locator}")
            raise

    def find_all(self, locator: Tuple[str, str]) -> List:
        """Find all matching elements."""
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def find_clickable(self, locator: Tuple[str, str]):
        """Wait until element is clickable, then return it."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    # ─── Interactions ─────────────────────────────────────────────────────────

    @allure.step("Click: {locator}")
    def click(self, locator: Tuple[str, str]):
        log.debug(f"Clicking {locator}")
        self.find_clickable(locator).click()

    @allure.step("Type '{text}' into {locator}")
    def type_text(self, locator: Tuple[str, str], text: str, clear: bool = True):
        log.debug(f"Typing '{text}' into {locator}")
        el = self.find(locator)
        if clear:
            el.clear()
        el.send_keys(text)

    def get_text(self, locator: Tuple[str, str]) -> str:
        return self.find(locator).text

    def is_visible(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_present(self, locator: Tuple[str, str]) -> bool:
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    # ─── Mobile-specific helpers ──────────────────────────────────────────────

    def swipe_up(self, swipes: int = 1):
        """Swipe up (scroll down) on mobile."""
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.8)
        end_y = int(size["height"] * 0.2)
        for _ in range(swipes):
            self.driver.swipe(start_x, start_y, start_x, end_y, 600)
            time.sleep(0.3)

    def swipe_down(self, swipes: int = 1):
        """Swipe down (scroll up) on mobile."""
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.2)
        end_y = int(size["height"] * 0.8)
        for _ in range(swipes):
            self.driver.swipe(start_x, start_y, start_x, end_y, 600)
            time.sleep(0.3)

    def scroll_to_text(self, text: str):
        """Android: scroll until text is visible (UiAutomator)."""
        self.driver.find_element(
            By.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView('
            f'new UiSelector().text("{text}"))',
        )

    # ─── Screenshot ───────────────────────────────────────────────────────────

    def take_screenshot(self, name: str = "screenshot"):
        """Attach a screenshot to the Allure report."""
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        log.debug(f"Screenshot taken: {name}")
