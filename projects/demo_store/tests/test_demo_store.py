"""
TestDemoStore — API Test
Project: demo_store
Endpoint base: https://fakestoreapi.com
Run: pytest projects/demo_store/tests/ -m api -v
"""
import pytest
import allure

from core.base_api_test import BaseAPITest


@allure.suite("API — Demo_store")
@allure.feature("DemoStore")
@pytest.mark.api
class TestDemoStore(BaseAPITest):
    """Auto-generated API tests for DemoStore."""


    @allure.title("GET list returns 200")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_get_list(self):
        """Verify the main list endpoint returns HTTP 200."""
        # TODO: implement test logic
        # Example:
        # resp = self.get("/endpoint")
        # self.assert_status(resp, 200)
        raise NotImplementedError("Implement this test")

