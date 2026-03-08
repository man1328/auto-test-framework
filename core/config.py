"""
Automation Test Framework — Core Configuration Loader
Reads settings from .env (local) or environment variables (CI/Jenkins).
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import yaml

# Load .env from project root
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


def _get(key: str, default=None):
    return os.environ.get(key, default)


# ─── Appium / Android ─────────────────────────────────────────────────────────
APPIUM_SERVER_URL: str = _get("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
ANDROID_PLATFORM_VERSION: str = _get("ANDROID_PLATFORM_VERSION", "13")
ANDROID_DEVICE_NAME: str = _get("ANDROID_DEVICE_NAME", "emulator-5554")
ANDROID_APP_PATH: str = _get("ANDROID_APP_PATH", "")      # path to .apk
ANDROID_APP_PACKAGE: str = _get("ANDROID_APP_PACKAGE", "")
ANDROID_APP_ACTIVITY: str = _get("ANDROID_APP_ACTIVITY", "")
ANDROID_AUTOMATION_NAME: str = _get("ANDROID_AUTOMATION_NAME", "UiAutomator2")
IMPLICIT_WAIT: int = int(_get("IMPLICIT_WAIT", 10))
EXPLICIT_WAIT: int = int(_get("EXPLICIT_WAIT", 20))

# ─── Web / Selenium ───────────────────────────────────────────────────────────
BROWSER: str = _get("BROWSER", "chrome")          # chrome | firefox | edge
HEADLESS: bool = _get("HEADLESS", "true").lower() == "true"
BASE_URL: str = _get("BASE_URL", "https://example.com")

# ─── API ──────────────────────────────────────────────────────────────────────
API_BASE_URL: str = _get("API_BASE_URL", "https://jsonplaceholder.typicode.com")
API_TIMEOUT: int = int(_get("API_TIMEOUT", 30))
API_TOKEN: str = _get("API_TOKEN", "")

# ─── Reports ──────────────────────────────────────────────────────────────────
REPORTS_DIR: Path = ROOT_DIR / "reports"
ALLURE_DIR: Path = REPORTS_DIR / "allure-results"
JUNIT_DIR: Path = REPORTS_DIR / "junit"
HTML_DIR: Path = REPORTS_DIR / "html"
LOGS_DIR: Path = ROOT_DIR / "logs"

# Auto-create directories
for _d in [REPORTS_DIR, ALLURE_DIR, JUNIT_DIR, HTML_DIR, LOGS_DIR]:
    _d.mkdir(parents=True, exist_ok=True)


def load_yaml(path: str | Path) -> dict:
    """Load a YAML test-data file."""
    with open(path, "r") as f:
        return yaml.safe_load(f)
