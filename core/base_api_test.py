"""
Automation Test Framework — Base API Test Class
All API test classes should extend BaseAPITest.
"""
import json
import pytest
import allure
import requests
from requests import Response

from core.logger import get_logger
from core import config

log = get_logger(__name__)


class BaseAPITest:
    """
    Base class for all API/HTTP tests.

    Usage:
        class TestUsers(BaseAPITest):
            def test_get_users(self):
                resp = self.get("/users")
                self.assert_status(resp, 200)
                assert len(resp.json()) > 0
    """

    session: requests.Session = None

    @pytest.fixture(autouse=True)
    def setup_session(self):
        """Create a requests.Session before each test, close after."""
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        if config.API_TOKEN:
            self.session.headers["Authorization"] = f"Bearer {config.API_TOKEN}"
        log.info(f"API session started — base URL: {config.API_BASE_URL}")
        yield
        self.session.close()
        log.info("API session closed.")

    # ─── HTTP Helpers ─────────────────────────────────────────────────────────

    def get(self, endpoint: str, **kwargs) -> Response:
        url = self._url(endpoint)
        log.info(f"GET {url}")
        resp = self.session.get(url, timeout=config.API_TIMEOUT, **kwargs)
        self._log_response(resp)
        return resp

    def post(self, endpoint: str, data: dict = None, **kwargs) -> Response:
        url = self._url(endpoint)
        log.info(f"POST {url} | body: {data}")
        resp = self.session.post(url, json=data, timeout=config.API_TIMEOUT, **kwargs)
        self._log_response(resp)
        return resp

    def put(self, endpoint: str, data: dict = None, **kwargs) -> Response:
        url = self._url(endpoint)
        log.info(f"PUT {url} | body: {data}")
        resp = self.session.put(url, json=data, timeout=config.API_TIMEOUT, **kwargs)
        self._log_response(resp)
        return resp

    def patch(self, endpoint: str, data: dict = None, **kwargs) -> Response:
        url = self._url(endpoint)
        log.info(f"PATCH {url} | body: {data}")
        resp = self.session.patch(url, json=data, timeout=config.API_TIMEOUT, **kwargs)
        self._log_response(resp)
        return resp

    def delete(self, endpoint: str, **kwargs) -> Response:
        url = self._url(endpoint)
        log.info(f"DELETE {url}")
        resp = self.session.delete(url, timeout=config.API_TIMEOUT, **kwargs)
        self._log_response(resp)
        return resp

    # ─── Assertions ───────────────────────────────────────────────────────────

    @allure.step("Assert status code is {expected_status}")
    def assert_status(self, response: Response, expected_status: int):
        assert response.status_code == expected_status, (
            f"Expected HTTP {expected_status}, got {response.status_code}\n"
            f"Response: {response.text[:500]}"
        )

    def assert_json_key(self, response: Response, key: str, expected_value=None):
        """Assert a key exists in the JSON response body (optionally check value)."""
        body = response.json()
        assert key in body, f"Key '{key}' not found in response: {body}"
        if expected_value is not None:
            assert body[key] == expected_value, (
                f"Expected {key}={expected_value!r}, got {body[key]!r}"
            )

    # ─── Internals ────────────────────────────────────────────────────────────

    @staticmethod
    def _url(endpoint: str) -> str:
        base = config.API_BASE_URL.rstrip("/")
        return f"{base}/{endpoint.lstrip('/')}"

    @staticmethod
    def _log_response(resp: Response):
        log.debug(f"  Status: {resp.status_code} | Time: {resp.elapsed.total_seconds():.3f}s")
        try:
            allure.attach(
                json.dumps(resp.json(), indent=2),
                name=f"Response [{resp.status_code}]",
                attachment_type=allure.attachment_type.JSON,
            )
        except Exception:
            allure.attach(resp.text, name=f"Response [{resp.status_code}]",
                          attachment_type=allure.attachment_type.TEXT)
