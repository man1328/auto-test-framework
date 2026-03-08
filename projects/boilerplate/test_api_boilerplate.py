"""
╔══════════════════════════════════════════════════════════════════════╗
║          API TESTING — BOILERPLATE TEST SUITE                        ║
╠══════════════════════════════════════════════════════════════════════╣
║  HOW TO USE:                                                         ║
║  1. Set API_BASE_URL in your .env file                               ║
║  2. Replace every  ← TODO  comment with your real values             ║
║  3. Run: pytest projects/boilerplate/test_api_boilerplate.py -m api  ║
╚══════════════════════════════════════════════════════════════════════╝
"""
import time
import pytest
import allure
from core.base_api_test import BaseAPITest


# ─── Fill these in for your API ───────────────────────────────────────────────
RESOURCE       = "/users"          # ← TODO: your main resource endpoint e.g. /products /orders
RESOURCE_ID    = 1                 # ← TODO: ID of an existing resource
BAD_ID         = 999999            # ← TODO: ID that definitely does not exist
CREATE_PAYLOAD = {                 # ← TODO: valid body for creating a new resource
    "name":     "Test User",
    "email":    "test@example.com",
    "username": "testuser",
}
UPDATE_PAYLOAD = {                 # ← TODO: valid body for updating a resource
    "name": "Updated Name",
}
AUTH_HEADER    = {}                # ← TODO: e.g. {"Authorization": "Bearer YOUR_TOKEN"}
                                   #          Leave empty {} if no auth required
MAX_RESPONSE_MS = 2000             # ← TODO: acceptable response time in milliseconds


def timed(response):
    """Return response time in milliseconds."""
    return response.elapsed.total_seconds() * 1000


# ══════════════════════════════════════════════════════════════════════════════
#  GROUP 1 — STATUS CODES
# ══════════════════════════════════════════════════════════════════════════════
@allure.suite("API — Boilerplate")
@allure.feature("Status Codes")
@pytest.mark.api
class TestStatusCodes(BaseAPITest):

    @allure.title("GET list of resources → 200 OK")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_01_get_list_returns_200(self):
        """GET the resource collection — should return 200."""
        resp = self.get(RESOURCE, headers=AUTH_HEADER)
        self.assert_status(resp, 200)

    @allure.title("GET single resource by ID → 200 OK")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_02_get_single_returns_200(self):
        """GET one specific resource by ID — should return 200."""
        resp = self.get(f"{RESOURCE}/{RESOURCE_ID}", headers=AUTH_HEADER)
        self.assert_status(resp, 200)

    @allure.title("GET non-existent resource → 404 Not Found")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_03_get_nonexistent_returns_404(self):
        """GET a resource ID that does not exist — should return 404."""
        resp = self.get(f"{RESOURCE}/{BAD_ID}", headers=AUTH_HEADER)
        self.assert_status(resp, 404)

    @allure.title("POST valid data → 201 Created")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_04_post_valid_data_returns_201(self):
        """POST a valid payload — should return 201."""
        resp = self.post(RESOURCE, data=CREATE_PAYLOAD, headers=AUTH_HEADER)
        self.assert_status(resp, 201)

    @allure.title("POST missing required fields → 400 Bad Request")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_05_post_empty_body_returns_400(self):
        """POST an empty body — should be rejected with 400."""
        resp = self.post(RESOURCE, data={}, headers=AUTH_HEADER)
        assert resp.status_code in (400, 422), \
            f"Expected 400 or 422, got {resp.status_code}"

    @allure.title("PUT update resource → 200 OK")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_06_put_update_returns_200(self):
        """PUT an update to an existing resource — should return 200."""
        resp = self.put(f"{RESOURCE}/{RESOURCE_ID}", data=UPDATE_PAYLOAD, headers=AUTH_HEADER)
        self.assert_status(resp, 200)

    @allure.title("DELETE resource → 200 or 204")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_07_delete_resource_succeeds(self):
        """DELETE a resource — should return 200 or 204."""
        # Create one first so we can delete it cleanly
        create_resp = self.post(RESOURCE, data=CREATE_PAYLOAD, headers=AUTH_HEADER)
        new_id = create_resp.json().get("id")
        resp = self.delete(f"{RESOURCE}/{new_id}", headers=AUTH_HEADER)
        assert resp.status_code in (200, 204), \
            f"Expected 200 or 204 on DELETE, got {resp.status_code}"

    @allure.title("No auth token → 401 Unauthorized")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.security
    def test_08_no_auth_returns_401(self):
        """Accessing a protected endpoint without token should return 401."""
        if not AUTH_HEADER:
            pytest.skip("This API does not require auth — skipping auth test")
        resp = self.get(RESOURCE, headers={})   # deliberately no auth
        self.assert_status(resp, 401)


# ══════════════════════════════════════════════════════════════════════════════
#  GROUP 2 — PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════
@allure.suite("API — Boilerplate")
@allure.feature("Performance")
@pytest.mark.api
class TestPerformance(BaseAPITest):

    @allure.title(f"GET list responds within {MAX_RESPONSE_MS}ms")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_09_get_list_response_time(self):
        """The list endpoint should respond quickly."""
        resp = self.get(RESOURCE, headers=AUTH_HEADER)
        ms = timed(resp)
        assert ms < MAX_RESPONSE_MS, \
            f"GET {RESOURCE} took {ms:.0f}ms — expected < {MAX_RESPONSE_MS}ms"

    @allure.title(f"POST responds within {MAX_RESPONSE_MS + 1000}ms")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_10_post_response_time(self):
        """POST should respond within an acceptable window."""
        resp = self.post(RESOURCE, data=CREATE_PAYLOAD, headers=AUTH_HEADER)
        ms = timed(resp)
        limit = MAX_RESPONSE_MS + 1000
        assert ms < limit, \
            f"POST took {ms:.0f}ms — expected < {limit}ms"


# ══════════════════════════════════════════════════════════════════════════════
#  GROUP 3 — DATA / SCHEMA VALIDATION
# ══════════════════════════════════════════════════════════════════════════════
@allure.suite("API — Boilerplate")
@allure.feature("Data Validation")
@pytest.mark.api
class TestDataValidation(BaseAPITest):

    # ← TODO: list the fields you expect every item to have
    EXPECTED_FIELDS = ["id", "name", "email"]

    @allure.title("GET list returns a JSON array")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_11_list_returns_array(self):
        """The list endpoint should return a JSON array, not an object."""
        resp = self.get(RESOURCE, headers=AUTH_HEADER)
        self.assert_status(resp, 200)
        data = resp.json()
        assert isinstance(data, list), \
            f"Expected a list, got {type(data).__name__}"

    @allure.title("Single resource contains all expected fields")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_12_resource_has_expected_fields(self):
        """Every required field should be present in the response."""
        resp = self.get(f"{RESOURCE}/{RESOURCE_ID}", headers=AUTH_HEADER)
        self.assert_status(resp, 200)
        data = resp.json()
        for field in self.EXPECTED_FIELDS:
            assert field in data, f"Expected field '{field}' missing from response"

    @allure.title("Resource 'id' field is an integer")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_13_id_field_is_integer(self):
        """The 'id' field type should be an integer."""
        resp = self.get(f"{RESOURCE}/{RESOURCE_ID}", headers=AUTH_HEADER)
        self.assert_status(resp, 200)
        assert isinstance(resp.json().get("id"), int), "ID should be an integer"

    @allure.title("Created resource matches the posted payload")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_14_created_resource_matches_payload(self):
        """The created resource in the response should contain what we sent."""
        resp = self.post(RESOURCE, data=CREATE_PAYLOAD, headers=AUTH_HEADER)
        self.assert_status(resp, 201)
        body = resp.json()
        for key, value in CREATE_PAYLOAD.items():
            assert body.get(key) == value, \
                f"Field '{key}': expected '{value}', got '{body.get(key)}'"

    @allure.title("Updated resource reflects the changes")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_15_updated_resource_reflects_changes(self):
        """After a PUT, the returned data should match what we sent."""
        resp = self.put(f"{RESOURCE}/{RESOURCE_ID}", data=UPDATE_PAYLOAD, headers=AUTH_HEADER)
        self.assert_status(resp, 200)
        body = resp.json()
        for key, value in UPDATE_PAYLOAD.items():
            assert body.get(key) == value, \
                f"Field '{key}' after update: expected '{value}', got '{body.get(key)}'"


# ══════════════════════════════════════════════════════════════════════════════
#  GROUP 4 — AUTH TOKEN VALIDATION
# ══════════════════════════════════════════════════════════════════════════════
@allure.suite("API — Boilerplate")
@allure.feature("Authentication")
@pytest.mark.api
class TestAuthValidation(BaseAPITest):

    @allure.title("Valid token → access granted (200)")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_16_valid_token_grants_access(self):
        """A valid auth token should allow access to the resource."""
        if not AUTH_HEADER:
            pytest.skip("No auth configured — skipping")
        resp = self.get(RESOURCE, headers=AUTH_HEADER)
        self.assert_status(resp, 200)

    @allure.title("Malformed token → 401 Unauthorized")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_17_bad_token_returns_401(self):
        """A garbage token string should be rejected."""
        if not AUTH_HEADER:
            pytest.skip("No auth configured — skipping")
        bad_auth = {"Authorization": "Bearer thisisnotavalidtoken123"}
        resp = self.get(RESOURCE, headers=bad_auth)
        self.assert_status(resp, 401)
