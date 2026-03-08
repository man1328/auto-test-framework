# ✍️ Adding Tests — Step-by-Step Guide

Everything you need to know to add new test cases, test projects, and connect a real Android app.

---

## 🚀 Method 1 — CLI Generator (Fastest)

### Create a brand-new project

```bash
cd "/home/manrig-13/PycharmProjects/automation test framework"
source .venv/bin/activate

# Interactive mode — asks you everything:
python cli/create_project.py

# One-liner for an API project:
python cli/create_project.py --name my_shop_api --type api --base-url https://api.myshop.com

# One-liner for an Android project:
python cli/create_project.py --name my_android_app --type android

# One-liner for a Web project:
python cli/create_project.py --name my_web_portal --type web --base-url https://myportal.com
```

This creates a fully structured folder under `projects/my_shop_api/` with:
- A test file with one placeholder test
- A YAML data file
- A `.env.example` with all relevant config vars

### Add a new test to an existing project

```bash
# Interactive mode — asks for method names, titles, descriptions:
python cli/add_test.py

# One-liner:
python cli/add_test.py --project my_shop_api --name ProductsTest --type api
```

The CLI will ask you:
```
Test method 1 name (e.g. test_get_products): test_get_all_products
Allure title for test_get_all_products: GET /products returns list
Docstring: Verify all products are returned with status 200
Severity [blocker/critical/normal/minor/trivial]: critical
Pytest marker [smoke/regression]: smoke

Test method 2 name (or ENTER to stop): [ENTER]
```

Result: a fully structured Python test file ready for you to implement.

---

## ✏️ Method 2 — Write Tests Manually

### API Test Example

Create `projects/my_shop_api/tests/test_products.py`:

```python
import pytest
import allure
from core.base_api_test import BaseAPITest

@allure.suite("API — My Shop")
@allure.feature("Products")
@pytest.mark.api
class TestProducts(BaseAPITest):

    @allure.title("GET /products returns 200 with a list")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_all_products(self):
        resp = self.get("/products")
        self.assert_status(resp, 200)
        assert len(resp.json()) > 0, "Products list should not be empty"

    @allure.title("GET /products/{id} returns specific product")
    @pytest.mark.parametrize("product_id", [1, 2, 3])
    def test_get_product_by_id(self, product_id):
        resp = self.get(f"/products/{product_id}")
        self.assert_status(resp, 200)
        assert resp.json()["id"] == product_id
```

> Run it: `pytest projects/my_shop_api/ -m api -v`

---

### Android Test Example

Create `projects/my_android_app/screens/login_screen.py`:

```python
from appium.webdriver.common.appiumby import AppiumBy
import allure
from core.page_object import BasePage

class _Locators:
    EMAIL_FIELD    = (AppiumBy.ACCESSIBILITY_ID, "email_input")
    PASSWORD_FIELD = (AppiumBy.ACCESSIBILITY_ID, "password_input")
    LOGIN_BUTTON   = (AppiumBy.ACCESSIBILITY_ID, "login_button")
    ERROR_TEXT     = (AppiumBy.XPATH, "//android.widget.TextView[@resource-id='error']")

class LoginScreen(BasePage):

    @allure.step("Login with email='{email}'")
    def login(self, email: str, password: str):
        self.type_text(_Locators.EMAIL_FIELD, email)
        self.type_text(_Locators.PASSWORD_FIELD, password)
        self.click(_Locators.LOGIN_BUTTON)

    def is_error_shown(self) -> bool:
        return self.is_visible(_Locators.ERROR_TEXT)
```

Create `projects/my_android_app/tests/test_login.py`:

```python
import pytest
import allure
from core.base_android_test import BaseAndroidTest
from projects.my_android_app.screens.login_screen import LoginScreen

@allure.suite("Android — My App")
@allure.feature("Login")
@pytest.mark.android
class TestAndroidLogin(BaseAndroidTest):

    @allure.title("Valid login navigates to home screen")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_valid_login(self):
        screen = LoginScreen(self.driver)
        screen.login("user@example.com", "password123")
        assert not screen.is_error_shown(), "Error should not appear on valid login"

    @allure.title("Invalid login shows error message")
    @pytest.mark.parametrize("email,password", [
        ("wrong@example.com", "wrongpass"),
        ("user@example.com", ""),
    ])
    def test_invalid_login(self, email, password):
        screen = LoginScreen(self.driver)
        screen.login(email, password)
        assert screen.is_error_shown(), "Error message should appear for invalid credentials"
```

> Run it: `bash test.sh android`

---

### Data-Driven Test with YAML

Create `projects/my_shop_api/test_data/products.yml`:
```yaml
new_products:
  - name: "Widget A"
    price: 9.99
    category: "widgets"
  - name: "Gadget B"
    price: 19.99
    category: "gadgets"
```

Use in your test:
```python
from pathlib import Path
import yaml

def load_products():
    f = Path(__file__).parent.parent / "test_data" / "products.yml"
    return yaml.safe_load(f.read_text())["new_products"]

@pytest.mark.parametrize("product", load_products())
def test_create_product(self, product):
    resp = self.post("/products", data=product)
    self.assert_status(resp, 201)
    assert resp.json()["name"] == product["name"]
```

---

## 📱 Setting Up Android Tests End-to-End

### Step 1 — Get your app's package and activity

```bash
# If you have the APK:
aapt dump badging /path/to/your-app.apk | grep -E "package:|launchable-activity"

# If app is already installed on device:
adb shell dumpsys package <partial-package-name> | grep "Activity"
```

### Step 2 — Configure .env

```ini
ANDROID_APP_PACKAGE=com.example.myapp
ANDROID_APP_ACTIVITY=.MainActivity
ANDROID_DEVICE_NAME=emulator-5554      # or real device serial from `adb devices`
ANDROID_PLATFORM_VERSION=13
```

### Step 3 — Find your element locators

Use **Appium Inspector** (free GUI tool):
```bash
# Download from: https://github.com/appium/appium-inspector/releases
# Connect to: http://127.0.0.1:4723
# Then click elements to get their AccessibilityId, XPath, etc.
```

### Step 4 — Run

```bash
bash test.sh android
```

---

## 🏷️ Pytest Markers Reference

Add markers to your tests to control what runs when:

```python
@pytest.mark.smoke       # Critical, fast tests — run first
@pytest.mark.regression  # Full suite
@pytest.mark.android     # Android/Appium tests
@pytest.mark.web         # Selenium web tests
@pytest.mark.api         # API/HTTP tests
@pytest.mark.slow        # Tests > 30 seconds
```

Run by marker:
```bash
pytest -m smoke           # Only smoke tests
pytest -m "api or web"    # API or Web tests
pytest -m "not slow"      # Skip slow tests
```

---

## 📋 Allure Report Annotations

Make your reports beautiful and informative:

```python
import allure

@allure.suite("Android — My App")        # Groups tests in the report
@allure.feature("Login Screen")          # Feature grouping
@allure.story("User can log in")         # User story
@allure.title("Valid login succeeds")    # Test display name
@allure.severity(allure.severity_level.CRITICAL)  # blocker/critical/normal/minor/trivial
@allure.description("Verifies that a user with valid credentials can log in successfully.")
def test_valid_login(self):
    with allure.step("Enter credentials"):
        screen.login("user@example.com", "pass")
    with allure.step("Verify no error shown"):
        assert not screen.is_error_shown()
```

---

## ✅ Checklist Before Running Tests

### API Tests
- [ ] Set `API_BASE_URL` in `.env`
- [ ] Set `API_TOKEN` if the API requires auth
- [ ] Run: `bash test.sh api`

### Android Tests
- [ ] Set `ANDROID_APP_PACKAGE` + `ANDROID_APP_ACTIVITY` in `.env`
- [ ] Connect device or start emulator (`adb devices` to verify)
- [ ] Set `ANDROID_DEVICE_NAME` to your device serial
- [ ] Run: `bash test.sh android` (Appium starts automatically)

### Web Tests
- [ ] Set `BASE_URL` to your target web app in `.env`
- [ ] Set `BROWSER=chrome` or `BROWSER=firefox`
- [ ] Set `HEADLESS=false` to watch the browser, `true` for CI
- [ ] Run: `bash test.sh web`
