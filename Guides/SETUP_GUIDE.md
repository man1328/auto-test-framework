# 📘 Automation Test Framework — Complete Setup Guide

> **What this is:** A full guide explaining how this framework was built, what was installed, and how to reproduce the setup on any machine from scratch.

---

## 🖥️ What Was Installed (Full Stack)

### System-level dependencies

| Tool | Version | How Installed | Why |
|---|---|---|---|
| Python 3.12 | 3.12.3 | Pre-installed | Runtime for all tests |
| Node.js | 22.x | Pre-installed | Required by Appium |
| Java 17 JRE | 17 | `sudo apt install openjdk-17-jre-headless` | Required by Allure CLI |
| Android Debug Bridge (adb) | 34.0.4 | `sudo apt install android-sdk-platform-tools` | Connect to Android devices/emulators |

### npm global packages (installed in `~/.npm-global`)

| Tool | Version | How Installed | Why |
|---|---|---|---|
| Appium 2 | 3.2.0 | `npm install -g appium` | Mobile automation server |
| UiAutomator2 driver | 7.0.0 | `appium driver install uiautomator2` | Android automation engine |
| Allure CLI | 2.37.0 | `npm install -g allure-commandline` | Report viewer/generator |

> **Note:** npm was reconfigured to use `~/.npm-global` as the prefix (no sudo needed).
> Added to `~/.bashrc`: `export PATH="$HOME/.npm-global/bin:$PATH"`

### Python virtual environment (`.venv/`)

All Python packages are isolated in `"/home/manrig-13/PycharmProjects/automation test framework/.venv"`.

| Package | Version | Purpose |
|---|---|---|
| pytest | 9.x | Test runner |
| pytest-html | 4.x | HTML report |
| pytest-xdist | 3.x | Parallel execution |
| pytest-rerunfailures | 16.x | Retry flaky tests |
| allure-pytest | 2.x | Allure report data |
| Appium-Python-Client | 5.2.6 | Python API for Appium |
| selenium | 4.x | Web automation |
| webdriver-manager | 4.x | Auto-downloads ChromeDriver |
| requests | 2.x | HTTP/API testing |
| Jinja2 | 3.x | Code generator templates |
| python-dotenv | 1.x | `.env` config loading |
| PyYAML | 6.x | YAML test data files |
| rich | 13.x | Beautiful CLI output |
| colorlog | 6.x | Colored log output |
| python-lsp-server | 1.14.0 | IDE autocomplete (pylsp) |

---

## 🔁 How to Reproduce This Setup on a Fresh Machine

### Step 1 — System prerequisites

```bash
# Ubuntu/Debian (tested on Ubuntu 24.04)
sudo apt update
sudo apt install -y python3 python3-venv nodejs npm \
    openjdk-17-jre-headless \
    android-sdk-platform-tools
```

### Step 2 — Configure npm prefix (no sudo needed)

```bash
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Step 3 — Install Appium 2 + UiAutomator2 driver + Allure CLI

```bash
npm install -g appium allure-commandline
appium driver install uiautomator2
```

### Step 4 — Clone/copy the project

```bash
# If using git:
git clone <your-repo-url> "/home/user/PycharmProjects/automation test framework"
cd "/home/user/PycharmProjects/automation test framework"
```

### Step 5 — Create virtual environment and install Python deps

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 6 — Configure your environment

```bash
cp .env.example .env
nano .env   # fill in your URLs, device name, app path
```

### Step 7 — Verify everything works

```bash
# Run API example tests (no device needed):
bash test.sh api

# View Allure report:
allure serve reports/allure-results
```

---

## ⚙️ PyCharm IDE Setup

To fix IDE import warnings (red squiggles):

1. Open PyCharm → **File → Settings → Project → Python Interpreter**
2. Click the gear icon → **Add Interpreter → Existing**
3. Set path to: `.venv/bin/python3`
4. Click **OK** — all imports will resolve correctly

---

## 📁 Project Structure Reference

```
automation test framework/
├── .venv/                      # Python virtual environment
├── cli/
│   ├── create_project.py       # Generate new test projects by typing
│   └── add_test.py             # Add tests to existing projects by typing
├── core/
│   ├── config.py               # Loads settings from .env
│   ├── logger.py               # Colored console + file logger
│   ├── page_object.py          # POM base (web + mobile)
│   ├── base_android_test.py    # Appium test base class
│   ├── base_web_test.py        # Selenium test base class
│   └── base_api_test.py        # API test base class
├── templates/                  # Jinja2 code-gen templates
├── projects/
│   ├── example_api/            # ✅ Works immediately, no device
│   ├── example_android/        # Needs Appium server + device
│   └── example_web/            # Needs real BASE_URL in .env
├── reports/
│   ├── allure-results/         # Raw Allure data (auto-generated)
│   ├── allure-html/            # Static HTML Allure report
│   ├── junit/results.xml       # JUnit XML for Jenkins
│   └── html/report.html        # Self-contained HTML report
├── logs/                       # Debug log files (auto-generated)
├── conftest.py                 # Global pytest fixtures
├── pytest.ini                  # Pytest config, markers, report paths
├── requirements.txt            # All Python dependencies
├── test.sh                     # One-stop run script (use this!)
├── Jenkinsfile                 # Jenkins CI/CD pipeline
├── .env.example                # Config template
└── .gitignore
```

---

## 🏃 Running Tests — Quick Reference

```bash
# Always activate the venv first (or use test.sh which handles it)
source .venv/bin/activate

# Run specific suites
bash test.sh api        # API tests only
bash test.sh web        # Web tests (set BASE_URL in .env first)
bash test.sh android    # Android tests (auto-starts Appium)
bash test.sh smoke      # Smoke suite across all projects
bash test.sh regression # Full regression suite
bash test.sh report     # Just regenerate + serve the Allure report

# Or use pytest directly
pytest projects/example_api/ -m api -v
pytest -m smoke -v
pytest -m "api or web" -v
pytest -n 4              # Run 4 tests in parallel
```

---

## 📊 Viewing Reports

```bash
# Live interactive report (opens browser)
allure serve reports/allure-results

# Static HTML report (open in any browser)
allure generate reports/allure-results -o reports/allure-html --clean
# → Open: reports/allure-html/index.html

# Simple HTML report (no Allure needed)
# → Open: reports/html/report.html

# JUnit XML (for Jenkins)
# → File: reports/junit/results.xml
```

---

## 🔧 Configuration Reference (.env)

```ini
# ─── Appium / Android ────────────────────────────────
APPIUM_SERVER_URL=http://127.0.0.1:4723
ANDROID_PLATFORM_VERSION=13
ANDROID_DEVICE_NAME=emulator-5554
ANDROID_APP_PATH=/path/to/your-app.apk
# OR instead of APK path:
ANDROID_APP_PACKAGE=com.example.myapp
ANDROID_APP_ACTIVITY=.MainActivity
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20

# ─── Web / Selenium ──────────────────────────────────
BASE_URL=https://yourapp.example.com
BROWSER=chrome          # chrome | firefox
HEADLESS=false          # true for Jenkins/CI

# ─── API ─────────────────────────────────────────────
API_BASE_URL=https://api.yourapp.com
API_TOKEN=your_bearer_token_here
API_TIMEOUT=30
```
