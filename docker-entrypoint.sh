#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
#  Docker Entrypoint — Automation Test Framework
#  Usage inside container:
#    docker run ... framework api
#    docker run ... framework web
#    docker run ... framework android
#    docker run ... framework smoke
#    docker run ... framework report
# ─────────────────────────────────────────────────────────────────
set -e

MARKER="${1:-api}"
RESULTS_DIR="/framework/reports/allure-results"
HTML_DIR="/framework/reports/allure-html"

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║   Automation Test Framework — Docker Runner  ║"
echo "╚══════════════════════════════════════════════╝"
echo "  Marker  : $MARKER"
echo "  Browser : ${BROWSER:-chrome} (headless=${HEADLESS:-true})"
echo "  API URL : ${API_BASE_URL:-not set}"
echo "  Web URL : ${BASE_URL:-not set}"
echo ""

# ── report-only mode ──────────────────────────────────────────────
if [[ "$MARKER" == "report" ]]; then
    echo "📊 Generating Allure static report..."
    allure generate "$RESULTS_DIR" -o "$HTML_DIR" --clean
    echo "✅ Report saved to: $HTML_DIR/index.html"
    echo "   Mount the /framework/reports volume to access it."
    exit 0
fi

# ── run tests ─────────────────────────────────────────────────────
echo "🚀 Running tests [marker: $MARKER]"
echo "──────────────────────────────────────"

MARKER_ARG=""
if [[ "$MARKER" != "all" ]]; then
    MARKER_ARG="-m $MARKER"
fi

python -m pytest projects/ $MARKER_ARG -v \
    --tb=short \
    --alluredir="$RESULTS_DIR" \
    --junitxml=/framework/reports/junit/results.xml \
    --html=/framework/reports/html/report.html \
    --self-contained-html \
    || true   # don't fail the container on test failures

echo ""
echo "📊 Generating Allure report..."
allure generate "$RESULTS_DIR" -o "$HTML_DIR" --clean

echo ""
echo "✅ Done! Reports available in /framework/reports/"
echo "   Mount that directory to access them on the host."
