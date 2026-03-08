# 🐳 Docker Deployment Guide

**Yes — this framework is fully containerizable.** Packaging it in Docker means:
- ✅ No manual installs on any new machine (Java, Chrome, Appium, etc. are baked in)
- ✅ Same results on any OS (Windows, Mac, Linux)
- ✅ Runs in Jenkins CI with zero host configuration
- ⚠️ Android testing requires the Appium server to run on the HOST (not inside Docker) because Docker cannot directly access USB devices

---

## ⚡ Quick Start (Docker)

### Prerequisites
Only **Docker Desktop** needs to be installed on the new machine.
Download from: https://www.docker.com/products/docker-desktop

```bash
# 1. Clone or copy the project
cd "/home/manrig-13/PycharmProjects/automation test framework"

# 2. Build the image (one-time, takes ~5-10 min first time)
docker compose build

# 3. Run API tests
docker compose run --rm framework api

# 4. View the live Allure report (stays running, auto-refreshes)
docker compose up allure
# → Open: http://localhost:5050
```

---

## 🧪 Running Different Test Suites

```bash
# API tests (works out of the box)
docker compose run --rm framework api

# Smoke suite
docker compose run --rm framework smoke

# Regression suite
docker compose run --rm framework regression

# With custom API URL
API_BASE_URL=https://api.myapp.com docker compose run --rm framework api

# Web tests (set BASE_URL first)
BASE_URL=https://myapp.com docker compose run --rm framework web
```

---

## 📊 Report Services

### Live Allure Report Server
```bash
docker compose up allure         # Start (always running, auto-refreshes)
docker compose stop allure       # Stop
```
Open: **http://localhost:5050**
- Auto-refreshes every 5 seconds when new test results come in
- Run tests in another terminal → report updates live

### Static Report (generated after each run)
```bash
# After running tests, reports are on your HOST at:
ls reports/allure-html/          # Allure static HTML
ls reports/html/report.html      # Simple HTML report
ls reports/junit/results.xml     # Jenkins JUnit XML
```

---

## 📱 Android Tests with Docker

Android tests use **USB devices connected to your HOST machine**. The container talks to Appium running on the host.

### Setup:

**On the HOST machine (not inside Docker):**
```bash
# 1. Start Appium on the host
npx appium

# 2. Connect your Android device or start emulator
adb devices   # Verify device is visible

# 3. Run Android tests (they connect to host Appium via network)
ANDROID_DEVICE_NAME=your-device-serial \
ANDROID_APP_PACKAGE=com.example.app \
ANDROID_APP_ACTIVITY=.MainActivity \
docker compose run --rm framework android
```

The container uses `host.docker.internal:4723` to reach Appium on the host.

---

## 🔧 Jenkins with Docker

Start Jenkins as a container:
```bash
docker compose --profile jenkins up jenkins
# → Open: http://localhost:8080
```

### Configure Jenkins to run Docker tests:
1. Install **Docker Pipeline** plugin in Jenkins
2. In your pipeline, reference the image:
```groovy
pipeline {
    agent {
        docker {
            image 'automation-framework:latest'
            args '--shm-size=2gb'
        }
    }
    stages {
        stage('Test') {
            steps {
                sh 'python -m pytest projects/ -m smoke -v'
            }
        }
    }
}
```

---

## 📦 Transferring to a New Machine

### Option A — Docker Hub (public/private registry)
```bash
# On the original machine — push image:
docker tag automation-framework:latest yourusername/automation-framework:latest
docker push yourusername/automation-framework:latest

# On the new machine — pull and run:
docker pull yourusername/automation-framework:latest
docker run yourusername/automation-framework:latest api
```

### Option B — Export as a .tar file (no internet needed)
```bash
# On original machine — save image:
docker save automation-framework:latest | gzip > automation-framework.tar.gz

# Transfer the file to the new machine (USB, SCP, etc.)

# On new machine — load and run:
docker load < automation-framework.tar.gz
docker run -v ./reports:/framework/reports automation-framework:latest api
```

### Option C — Just copy the project folder (simplest)
Copy the whole project folder to the new machine and run:
```bash
docker compose build && docker compose run --rm framework api
```
Docker builds the image fresh on the new machine. Takes ~10 min first time but works on any OS.

---

## 🏗️ What's Inside the Docker Image

| Layer | Size (approx) | What |
|---|---|---|
| Python 3.12 slim | ~50MB | Base runtime |
| System libs | ~200MB | Chrome dependencies |
| Google Chrome | ~300MB | Headless browser |
| Java 17 JRE | ~200MB | Allure CLI runtime |
| Appium + drivers | ~150MB | Mobile automation |
| Python packages | ~200MB | Test libraries |
| **Total** | **~1.1GB** | Complete environment |

---

## 💡 Tips

- **Reports are always on your host.** The `reports/` folder is mounted as a volume — your test results survive container restarts.
- **Edit tests without rebuilding.** The `projects/` folder is also mounted — add new test files on your host and they're immediately available inside the container.
- **Environment variables** can be set in a `.env` file in the project root and Docker Compose picks them up automatically.
- **First build is slow** (~5-10 min) because Chrome is downloaded. Subsequent runs are instant — Docker caches the layers.
