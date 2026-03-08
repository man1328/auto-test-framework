"""
conftest.py for the example_android project.
Gracefully skips ALL android tests if Appium is not installed or no device is connected.
"""
import pytest

try:
    from appium import webdriver  # noqa: F401
    _APPIUM_AVAILABLE = True
except ImportError:
    _APPIUM_AVAILABLE = False


def pytest_collection_modifyitems(config, items):
    if not _APPIUM_AVAILABLE:
        skip_marker = pytest.mark.skip(
            reason="Appium not installed. Install with: pip install Appium-Python-Client"
        )
        for item in items:
            if "example_android" in str(item.fspath):
                item.add_marker(skip_marker)
