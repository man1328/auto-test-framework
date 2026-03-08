"""
Global pytest conftest.py
Provides shared fixtures available to ALL test projects.
Project-specific conftest.py files can override these.
"""
import pytest
from core.logger import get_logger

log = get_logger("conftest")


# ─── Screenshot on failure (for web/mobile) ───────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Track test outcome so base classes can check pass/fail in teardown."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ─── Allure environment info ───────────────────────────────────────────────────
def pytest_configure(config):
    """Write Allure environment file so reports show test environment."""
    import os
    from pathlib import Path
    allure_dir = Path("reports/allure-results")
    allure_dir.mkdir(parents=True, exist_ok=True)
    env_file = allure_dir / "environment.properties"
    env_file.write_text(
        f"Browser={os.environ.get('BROWSER', 'chrome')}\n"
        f"BaseURL={os.environ.get('BASE_URL', 'N/A')}\n"
        f"APIBaseURL={os.environ.get('API_BASE_URL', 'N/A')}\n"
        f"AndroidDevice={os.environ.get('ANDROID_DEVICE_NAME', 'N/A')}\n"
        f"AppiumServer={os.environ.get('APPIUM_SERVER_URL', 'N/A')}\n"
        f"PlatformVersion={os.environ.get('ANDROID_PLATFORM_VERSION', 'N/A')}\n"
    )


# ─── Session-scoped API client (optional shortcut) ────────────────────────────
@pytest.fixture(scope="session")
def api_base_url():
    from core import config
    return config.API_BASE_URL


@pytest.fixture(scope="session")
def env():
    """Return the entire config module for convenience."""
    from core import config
    return config
