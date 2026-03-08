"""
Example API Tests — JSONPlaceholder REST API
Run: pytest projects/example_api/tests/ -m api -v

No device or browser required — works out of the box!
API base URL: https://jsonplaceholder.typicode.com
"""
import pytest
import allure

from core.base_api_test import BaseAPITest
from core import config
from pathlib import Path
import yaml


def load_test_data():
    """Load parametrized test data from YAML file."""
    data_file = Path(__file__).parent.parent / "test_data" / "users.yml"
    return yaml.safe_load(data_file.read_text())["new_users"]


@allure.suite("API — JSONPlaceholder")
@allure.feature("Users Endpoint")
@pytest.mark.api
class TestUsersAPI(BaseAPITest):
    """Tests for /users endpoint of JSONPlaceholder API."""

    @allure.title("GET /users returns 200 with a list of users")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_get_all_users(self):
        """Verify the users endpoint returns a non-empty list."""
        resp = self.get("/users")
        self.assert_status(resp, 200)
        users = resp.json()
        assert isinstance(users, list), "Response should be a list"
        assert len(users) > 0, "Users list should not be empty"

    @allure.title("GET /users/{id} returns specific user")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("user_id,expected_name", [
        (1, "Leanne Graham"),
        (2, "Ervin Howell"),
        (3, "Clementine Bauch"),
    ])
    def test_get_user_by_id(self, user_id, expected_name):
        """Verify fetching a user by ID returns correct data."""
        resp = self.get(f"/users/{user_id}")
        self.assert_status(resp, 200)
        body = resp.json()
        assert body["id"] == user_id
        assert body["name"] == expected_name, (
            f"Expected name '{expected_name}', got '{body['name']}'"
        )

    @allure.title("POST /users creates a new user")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("user_data", load_test_data())
    def test_create_user(self, user_data):
        """Verify that creating a user returns 201 with the new user data."""
        resp = self.post("/users", data=user_data)
        self.assert_status(resp, 201)
        body = resp.json()
        assert body["name"] == user_data["name"]
        assert body["email"] == user_data["email"]
        assert "id" in body, "Response should include the new user's id"

    @allure.title("PUT /users/{id} updates a user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user(self):
        """Verify that updating a user returns the modified data."""
        updated = {"name": "Updated Name", "email": "updated@example.com", "username": "updateduser"}
        resp = self.put("/users/1", data=updated)
        self.assert_status(resp, 200)
        self.assert_json_key(resp, "name", "Updated Name")

    @allure.title("DELETE /users/{id} returns 200")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user(self):
        """Verify that deleting a user returns 200."""
        resp = self.delete("/users/1")
        self.assert_status(resp, 200)

    @allure.title("GET /users/{id} for non-existent user returns 404")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_get_nonexistent_user(self):
        """Verify 404 for a user that doesn't exist."""
        resp = self.get("/users/99999")
        self.assert_status(resp, 404)


@allure.suite("API — JSONPlaceholder")
@allure.feature("Posts Endpoint")
@pytest.mark.api
class TestPostsAPI(BaseAPITest):
    """Tests for /posts endpoint."""

    @allure.title("GET /posts returns 100 posts")
    @pytest.mark.smoke
    def test_get_all_posts(self):
        resp = self.get("/posts")
        self.assert_status(resp, 200)
        assert len(resp.json()) == 100

    @allure.title("Filter posts by userId")
    def test_filter_posts_by_user(self):
        resp = self.get("/posts", params={"userId": 1})
        self.assert_status(resp, 200)
        posts = resp.json()
        assert all(p["userId"] == 1 for p in posts), "All posts should belong to userId=1"
