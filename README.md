# Automation Test Framework

A fully automated, extensible testing framework for **Android (Appium)**, **Web (Selenium)**, and **API** testing — with **Allure + Jenkins** CI/CD reporting and a **CLI code generator** that scaffolds complete projects and tests in seconds.

---

## Why this exists

Most test frameworks make you choose: mobile *or* web *or* API. This one runs all three from a single codebase, with a shared Page Object Model, unified configuration, and a CLI that eliminates boilerplate. Built to be the testing layer I wanted when I was running CI for a mobile + web product — so I built it.

---

## Demo

| Layer | Runs in | Report |
|-------|---------|--------|
| **API** | `pytest projects/example_api/ -m api -v` | Works immediately — no device, no browser |
| **Web** | `pytest projects/example_web/ -m web -v` | Selenium 4 + auto-managed drivers |
| **Android** | `pytest projects/example_android/ -m android -v` | Appium 2 + UiAutomator2 |

> **30-second proof:** `allure serve reports/allure-results` after any run opens an interactive report with screenshots, timelines, and flaky-test history.

---

## Stack

| Category | Tools |
|----------|-------|
| **Mobile** | Appium 2, UiAutomator2 |
| **Web** | Selenium 4, WebDriverManager |
| **API** | `requests`, `pytest` |
| **Reporting** | Allure, JUnit XML (Jenkins-ready) |
| **Architecture** | Page Object Model, YAML data-driven tests |
| **Reliability** | `pytest-rerunfailures` (auto-retry), `pytest-xdist` (parallel) |
| **CI/CD** | Declarative `Jenkinsfile` with Allure + JUnit publishing |
| **Code Gen** | Jinja2 templates → `cli/create_project.py`, `cli/add_test.py` |

---

## Quick Start (runs in 2 minutes)

```bash
# 1. Clone & install
git clone <your-fork>
cd auto-test-framework
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure (copy template, fill your values)
cp .env.example .env
# edit .env — at minimum set API_BASE_URL for API tests

# 3. Run the API suite — zero external deps
pytest projects/example_api/ -m api -v

# 4. See the report
allure serve reports/allure-results
```

**That's it.** Web and Android need a browser/device — see [Setup Details](#setup-details) below.

---

## CLI Code Generator (the time-saver)

```bash
# Scaffold a complete project interactively
python cli/create_project.py

# One-liners
python cli/create_project.py --name my_api --type api --base-url https://api.example.com
python cli/create_project.py --name my_app --type android
python cli/create_project.py --name my_portal --type web --base-url https://staging.example.com

# Add a test to an existing project
python cli/add_test.py --project my_api --name PaymentsTest --type api
```

Generated projects include: base test class, POM skeleton, YAML data file, pytest markers, Allure annotations — ready to write assertions.

---

## Project Structure

```
auto-test-framework/
├── cli/
│   ├── create_project.py    # Project scaffolder (interactive + CLI)
│   └── add_test.py          # Test scaffolder (interactive + CLI)
├── core/
│   ├── config.py            # .env-based config with validation
│   ├── logger.py            # Colored file + console logger
│   ├── page_object.py       # Shared POM base (web + mobile)
│   ├── base_android_test.py # Appium base test + capabilities
│   ├── base_web_test.py     # Selenium base test + driver mgmt
│   └── base_api_test.py     # requests wrapper + assertions
├── templates/               # Jinja2 templates for code gen
├── projects/
│   ├── example_api/         # ✅ Runs immediately — no setup
│   ├── example_web/         # Selenium + Chrome (auto-driver)
│   └── example_android/     # Appium + emulator/device
├── reports/                 # Allure + JUnit + HTML output
├── conftest.py              # Global pytest fixtures
├── pytest.ini               # Markers: api, web, android, smoke, regression
├── Jenkinsfile              # Declarative pipeline (Allure + JUnit)
└── .env.example             # Safe-to-commit config template
```

---

## Running Tests

| Command | Purpose |
|---------|---------|
| `pytest projects/example_api/ -m api -v` | API suite (no deps) |
| `pytest projects/example_web/ -m web -v` | Web suite |
| `pytest projects/example_android/ -m android -v` | Android suite |
| `pytest -m smoke -v` | Cross-project smoke tests |
| `pytest -m regression -v` | Full regression |
| `pytest -n 4` | Parallel (4 workers) |
| `pytest --reruns 2` | Auto-retry flaky tests 2× |

### Allure Reports

```bash
# Interactive (auto-opens browser)
allure serve reports/allure-results

# Static HTML for CI artifacts
allure generate reports/allure-results -o reports/allure-html --clean
```

---

## Setup Details

### Android / Appium (only if you run Android tests)

```bash
# One-time: install Appium 2 + driver
npm install -g appium
appium driver install uiautomator2

# Start server (keep running)
npx appium
```

Configure in `.env`:
```ini
APPIUM_SERVER_URL=http://127.0.0.1:4723
ANDROID_DEVICE_NAME=emulator-5554        # or real device serial
ANDROID_PLATFORM_VERSION=13
ANDROID_APP_PATH=/path/to/your-app.apk
```

### Web / Selenium

Zero manual driver setup — WebDriverManager handles it.

```ini
# .env
BASE_URL=https://yourapp.example.com
BROWSER=chrome            # or firefox
HEADLESS=false            # true for CI
```

### API

```ini
# .env
API_BASE_URL=https://jsonplaceholder.typicode.com
API_TOKEN=                # optional Bearer token
```

---

## Jenkins Integration

1. Install Jenkins plugins: **Allure Jenkins Plugin**, **Pipeline**, **AnsiColor**
2. Create Pipeline job → point to this repo's `Jenkinsfile`
3. Add Credentials in Jenkins for: `API_BASE_URL`, `BASE_URL`, `APPIUM_SERVER_URL`
4. Run with Parameters → choose `MARKER` (smoke / api / web / android / regression)

The pipeline:
- Installs deps in isolated workspace
- Runs selected marker suite
- Publishes **Allure** interactive report
- Publishes **JUnit** test results for trend graphs
- Archives HTML report + logs

---

## Writing Tests — Patterns Used Here

### Extend the right base class
```python
# Android
class TestLogin(BaseAndroidTest):
    def test_login(self):
        screen = LoginScreen(self.driver)
        screen.login("user", "pass")
        assert screen.is_home_visible()

# Web
class TestCheckout(BaseWebTest):
    def test_checkout(self):
        self.navigate("/cart")
        page = CartPage(self.driver)
        page.proceed_to_checkout()

# API
class TestOrders(BaseAPITest):
    def test_create_order(self):
        resp = self.post("/orders", json={"item": "book", "qty": 2})
        self.assert_status(resp, 201)
```

### Data-driven via YAML
```python
import yaml
orders = yaml.safe_load(open("test_data/orders.yml"))["orders"]

@pytest.mark.parametrize("order", orders)
def test_create_order(self, order):
    resp = self.post("/orders", json=order)
    self.assert_status(resp, 201)
```

### Allure annotations (what the report shows)
```python
@allure.title("User can log in with valid credentials")
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Authentication")
@pytest.mark.smoke
def test_valid_login(self):
    ...
```

---

## Configuration Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `APPIUM_SERVER_URL` | `http://127.0.0.1:4723` | Appium server |
| `ANDROID_DEVICE_NAME` | `emulator-5554` | Device serial |
| `ANDROID_PLATFORM_VERSION` | `13` | Android version |
| `ANDROID_APP_PATH` | *(required for Android)* | Path to `.apk` |
| `IMPLICIT_WAIT` | `10` | Implicit wait (sec) |
| `EXPLICIT_WAIT` | `20` | Explicit wait (sec) |
| `BROWSER` | `chrome` | `chrome` or `firefox` |
| `HEADLESS` | `true` | Headless mode |
| `BASE_URL` | `https://example.com` | Web base URL |
| `API_BASE_URL` | `https://jsonplaceholder.typicode.com` | API base URL |
| `API_TOKEN` | *(empty)* | Bearer token |

---

## What's Not Here (Known Limits)

- **iOS / XCUITest** — not implemented (Appium 2 supports it; base class would need adding)
- **Visual regression** — no Percy/Applitools hook yet
- **Contract testing** — no Pact / Spring Cloud Contract layer
- **Test management sync** — no direct Jira/Xray/Zephyr push (JUnit XML is the bridge)

---

## My Role

- Designed the multi-layer architecture (shared POM, config, logging)
- Built the CLI code generator (Jinja2 templates → working projects in <30 sec)
- Wired Allure + JUnit + Jenkins pipeline end-to-end
- Implemented auto-retry, parallel execution, and data-driven YAML patterns
- AI-assisted: boilerplate generation, pytest marker syntax, Allure annotation references

---

## License

MIT — use it, fork it, break it, fix it.
