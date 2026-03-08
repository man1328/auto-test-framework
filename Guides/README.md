# Automation Test Framework 🚀

A fully automated, extensible testing framework for **Android (Appium)**, **Web (Selenium)**, and **API** testing, with **Allure + Jenkins** CI/CD reporting and a **CLI code generator** to create new projects and tests by typing commands.

---

## ✨ Features
- 📱 **Android testing** via Appium 2 + UiAutomator2
- 🌐 **Web testing** via Selenium 4 + WebDriverManager
- 🔌 **API testing** via requests + pytest
- 📊 **Allure Reports** (beautiful visual reports) + JUnit XML for Jenkins
- 🛠️ **CLI generator** — create a full project or add tests by typing one command
- 📐 **Page Object Model** (POM) — clean, maintainable test code
- 📝 **YAML test data** — data-driven tests without touching Python
- 🔁 **Auto-retry flaky tests** via `pytest-rerunfailures`
- ⚡ **Parallel execution** via `pytest-xdist`

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
cd "/home/manrig-13/PycharmProjects/automation test framework"
pip install -r requirements.txt
```

### 2. Configure your environment
```bash
cp .env.example .env
# Edit .env with your device/URL settings
nano .env
```

### 3. Run example tests (no device needed!)
```bash
# API tests — works immediately, no device required
pytest projects/example_api/ -m api -v

# View the Allure report
allure serve reports/allure-results
```

---

## 🛠️ CLI Code Generator

### Create a new project
```bash
# Interactive mode — asks you questions:
python cli/create_project.py

# One-liner API project:
python cli/create_project.py --name my_api --type api --base-url https://api.example.com

# One-liner Android project:
python cli/create_project.py --name my_app --type android

# One-liner Web project:
python cli/create_project.py --name my_portal --type web --base-url https://staging.example.com
```

### Add a test to an existing project
```bash
# Interactive mode (asks test method names, titles, severities):
python cli/add_test.py

# One-liner:
python cli/add_test.py --project my_api --name PaymentsTest --type api
```

---

## 📁 Project Structure
```
automation test framework/
├── cli/
│   ├── create_project.py    # Scaffold new project
│   └── add_test.py          # Add test to existing project
├── core/
│   ├── config.py            # .env-based configuration
│   ├── logger.py            # Colored file + console logger
│   ├── page_object.py       # POM base class (web + mobile)
│   ├── base_android_test.py # Appium base test
│   ├── base_web_test.py     # Selenium base test
│   └── base_api_test.py     # API requests base test
├── templates/               # Jinja2 code-gen templates
├── projects/
│   ├── example_android/     # Example Appium project
│   ├── example_api/         # Example API project ✅ runs immediately
│   └── example_web/         # Example Selenium project
├── reports/                 # Generated HTML/Allure/JUnit reports
├── conftest.py              # Global pytest fixtures
├── pytest.ini               # Pytest config + markers
├── Jenkinsfile              # Declarative Jenkins pipeline
└── .env.example             # Configuration template
```

---

## 🧪 Running Tests

| Command | What runs |
|---|---|
| `pytest projects/example_api/ -m api -v` | All API tests |
| `pytest projects/example_web/ -m web -v` | All Web tests |
| `pytest projects/example_android/ -m android -v` | All Android tests |
| `pytest -m smoke -v` | Smoke suite (all projects) |
| `pytest -m regression -v` | Full regression suite |
| `pytest -n 4` | Parallel (4 workers) |
| `pytest --reruns 2` | Retry flaky tests 2x |

### View Allure Reports
```bash
# Serve interactive report
allure serve reports/allure-results

# Generate static HTML
allure generate reports/allure-results -o reports/allure-html --clean
```

---

## 📱 Android / Appium Setup

### Prerequisites
```bash
# Install Appium 2
npm install -g appium

# Install UiAutomator2 driver
appium driver install uiautomator2

# Start Appium server
npx appium
```

### Configure your device in `.env`
```ini
APPIUM_SERVER_URL=http://127.0.0.1:4723
ANDROID_DEVICE_NAME=emulator-5554     # or your real device serial
ANDROID_PLATFORM_VERSION=13
ANDROID_APP_PATH=/path/to/your-app.apk
```

### Run Android tests
```bash
pytest projects/example_android/ -m android -v
```

---

## 🌐 Web / Selenium Setup

Chrome is auto-downloaded by WebDriverManager — no manual driver setup needed!

```ini
# .env
BASE_URL=https://yourapp.example.com
BROWSER=chrome        # or firefox
HEADLESS=false        # true for CI
```

```bash
pytest projects/example_web/ -m web -v
```

---

## 🔌 Jenkins Setup

1. **Install Jenkins plugins**: Allure Jenkins Plugin, Pipeline, AnsiColor
2. **Create Pipeline job** → point to this repo's `Jenkinsfile`
3. **Set Credentials** in Jenkins for: `API_BASE_URL`, `BASE_URL`, `APPIUM_SERVER_URL`
4. **Run with Parameters**: choose `MARKER` (smoke/api/web/android/regression)

The pipeline will:
- Install dependencies
- Run selected tests
- Publish **Allure** interactive report
- Publish **JUnit** test results
- Archive HTML report and logs

---

## 📐 Writing Tests — Best Practices

### Extending Base Classes
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
        resp = self.post("/orders", data={"item": "book", "qty": 2})
        self.assert_status(resp, 201)
```

### Data-driven with YAML
```python
import yaml
data = yaml.safe_load(open("test_data/orders.yml"))

@pytest.mark.parametrize("order", data["orders"])
def test_create_order(self, order):
    resp = self.post("/orders", data=order)
    self.assert_status(resp, 201)
```

### Allure Annotations
```python
@allure.title("User can log in with valid credentials")
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Authentication")
@pytest.mark.smoke
def test_valid_login(self):
    ...
```

---

## 🔧 Configuration Reference

| Variable | Default | Description |
|---|---|---|
| `APPIUM_SERVER_URL` | `http://127.0.0.1:4723` | Appium server address |
| `ANDROID_DEVICE_NAME` | `emulator-5554` | Device serial |
| `ANDROID_PLATFORM_VERSION` | `13` | Android version |
| `ANDROID_APP_PATH` | _(empty)_ | Path to .apk |
| `IMPLICIT_WAIT` | `10` | Implicit wait (seconds) |
| `EXPLICIT_WAIT` | `20` | Explicit wait (seconds) |
| `BROWSER` | `chrome` | `chrome` or `firefox` |
| `HEADLESS` | `true` | Headless browser mode |
| `BASE_URL` | `https://example.com` | Web base URL |
| `API_BASE_URL` | `https://jsonplaceholder.typicode.com` | API base URL |
| `API_TOKEN` | _(empty)_ | Bearer token |
