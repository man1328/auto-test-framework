# ─────────────────────────────────────────────────────────────────
#  Automation Test Framework — Dockerfile
#  Supports: API tests and Web tests (headless Chrome)
#  Android tests require a real device connected to the HOST,
#  which is exposed to the container via ADB over TCP.
# ─────────────────────────────────────────────────────────────────
FROM python:3.12-slim

LABEL maintainer="Automation Framework"
LABEL description="Portable automation testing environment — API, Web (Selenium), and report generation"

# ─── System dependencies ─────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Allure needs Java
    openjdk-17-jre-headless \
    # Chrome & Selenium headless
    wget curl gnupg unzip \
    ca-certificates fonts-liberation \
    libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcairo2 libcups2 libdbus-1-3 \
    libexpat1 libgdk-pixbuf2.0-0 libglib2.0-0 \
    libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 \
    libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 \
    libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 \
    libxrandr2 libxrender1 libxss1 libxtst6 \
    lsb-release xdg-utils \
    # ADB for connecting to Android device on host
    android-sdk-platform-tools \
    # Node.js for Appium (added via nodesource)
    nodejs npm \
    # Network utilities
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# ─── Google Chrome (stable) ──────────────────────────────────────
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | \
    gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] \
    http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# ─── npm global tools (Appium + Allure) ──────────────────────────
ENV NPM_CONFIG_PREFIX=/usr/local
RUN npm install -g appium allure-commandline && \
    appium driver install uiautomator2

# ─── Python dependencies ──────────────────────────────────────────
WORKDIR /framework
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─── Copy project ─────────────────────────────────────────────────
COPY . .

# ─── Create report directories ───────────────────────────────────
RUN mkdir -p reports/allure-results reports/allure-html reports/junit reports/html logs

# ─── Environment defaults (override via docker-compose or -e flags)
ENV BROWSER=chrome \
    HEADLESS=true \
    API_BASE_URL=https://jsonplaceholder.typicode.com \
    BASE_URL=https://example.com \
    APPIUM_SERVER_URL=http://host.docker.internal:4723 \
    ANDROID_DEVICE_NAME=emulator-5554 \
    ANDROID_PLATFORM_VERSION=13

# ─── Entrypoint ───────────────────────────────────────────────────
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["api"]
