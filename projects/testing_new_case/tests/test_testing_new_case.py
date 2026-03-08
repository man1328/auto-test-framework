"""
TestTestingNewCase — Web/Selenium Test
Project: testing_new_case
Page: TestingNewCasePage
Run: pytest projects/testing_new_case/tests/ -m web -v
"""
import pytest
import allure

from core.base_web_test import BaseWebTest
from projects.testing_new_case.pages.testing_new_case_page import TestingNewCasePage


@allure.suite("Web — Testing_new_case")
@allure.feature("TestingNewCase")
@pytest.mark.web
class TestTestingNewCase(BaseWebTest):
    """Auto-generated web tests for TestingNewCase."""


    @allure.title("TestingNewCase page loads")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_page_loads(self):
        """Verify the page loads without errors."""
        self.navigate("/")
        page = TestingNewCasePage(self.driver)
        # TODO: implement test logic
        raise NotImplementedError("Implement this test")

