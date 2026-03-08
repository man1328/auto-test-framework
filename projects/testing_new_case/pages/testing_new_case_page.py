"""
TestingNewCasePage — Page Object
Page URL: /
"""
from selenium.webdriver.common.by import By

import allure

from core.page_object import BasePage


class _Locators:
    # TODO: add your locators here
    # Examples:
    # ELEMENT_ID   = (By.ID, "element_id")
    # ELEMENT_XPATH = (By.XPATH, "//android.widget.Button[@text='Login']")
    pass


class TestingNewCasePage(BasePage):
    """
    Page object for the TestingNewCase page.
    """

    # TODO: add your page interaction methods
    # Example:
    # @allure.step("Click submit button")
    # def click_submit(self):
    #     self.click(_Locators.SUBMIT_BUTTON)

    def is_displayed(self) -> bool:
        """Override with a check for a key element on this page/screen."""
        raise NotImplementedError("Implement is_displayed() with an element check")