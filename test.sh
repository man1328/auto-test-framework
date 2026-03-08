#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  Automation Framework — One-Stop Test Runner
#  Usage (from anywhere):
#    bash "/home/manrig-13/PycharmProjects/automation test framework/test.sh"
#    bash "/home/manrig-13/PycharmProjects/automation test framework/test.sh" api
#    bash "/home/manrig-13/PycharmProjects/automation test framework/test.sh" android
#    bash "/home/manrig-13/PycharmProjects/automation test framework/test.sh" smoke
#    bash "/home/manrig-13/PycharmProjects/automation test framework/test.sh" report
# ─────────────────────────────────────────────────────────────

# Always run from the project root — no matter where you call this from
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"
ALLURE="$HOME/.npm-global/bin/allure"
RESULTS_DIR="$SCRIPT_DIR/reports/allure-results"
HTML_DIR="$SCRIPT_DIR/reports/allure-html"

MARKER="${1:-api}"   # default to 'api' if no arg given
APPIUM="$HOME/.npm-global/bin/appium"

# ── report-only mode ──────────────────────────────────────────
if [[ "$MARKER" == "report" ]]; then
    echo "📊 Generating Allure report..."
    "$ALLURE" generate "$RESULTS_DIR" -o "$HTML_DIR" --clean
    echo ""
    echo "📂 Static report: $HTML_DIR/index.html"
    echo "🌐 Serving live report..."
    "$ALLURE" serve "$RESULTS_DIR"
    exit 0
fi

# ── auto-start Appium for android tests ───────────────────────
APPIUM_PID=""
if [[ "$MARKER" == "android" ]]; then
    if ! nc -z 127.0.0.1 4723 2>/dev/null; then
        echo "📱 Starting Appium server..."
        nohup "$APPIUM" > /tmp/appium_run.log 2>&1 &
        APPIUM_PID=$!
        echo "   Waiting for Appium to be ready..."
        for i in {1..15}; do
            sleep 1
            if nc -z 127.0.0.1 4723 2>/dev/null; then
                echo "   ✅ Appium ready (PID=$APPIUM_PID)"
                break
            fi
        done
    else
        echo "📱 Appium already running on port 4723"
    fi
fi

# ── run tests ─────────────────────────────────────────────────
echo ""
echo "🚀 Running tests  [marker: $MARKER]"
echo "──────────────────────────────────────"
"$VENV_PYTHON" -m pytest projects/ -m "$MARKER" -v \
    --alluredir="$RESULTS_DIR"

echo ""
echo "📊 Generating Allure report..."
"$ALLURE" generate "$RESULTS_DIR" -o "$HTML_DIR" --clean

echo ""
echo "✅ Done!"
echo "   HTML report : $HTML_DIR/index.html"
echo "   JUnit XML   : $SCRIPT_DIR/reports/junit/results.xml"
echo ""
echo "▶  To open live report:"
echo "   $ALLURE serve \"$RESULTS_DIR\""
