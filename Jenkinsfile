#!/usr/bin/env groovy
/**
 * Automation Test Framework — Declarative Jenkins Pipeline
 *
 * Parameters (customize in Jenkins "Build with Parameters"):
 *   MARKER  — pytest marker to run (smoke | regression | android | web | api | all)
 *   PROJECT — specific project to test (empty = all projects)
 *   BRANCH  — git branch to test
 */
pipeline {
    agent any

    parameters {
        choice(
            name: 'MARKER',
            choices: ['smoke', 'api', 'web', 'android', 'regression', 'all'],
            description: 'Which test suite to run'
        )
        string(
            name: 'PROJECT',
            defaultValue: '',
            description: 'Run tests in a specific project (e.g. example_api). Leave blank for all.'
        )
        booleanParam(
            name: 'START_APPIUM',
            defaultValue: false,
            description: 'Start Appium server before running (required for android tests)'
        )
    }

    environment {
        // ── Paths ─────────────────────────────────────────────────────────
        VENV_DIR    = "${WORKSPACE}/.venv"
        REPORTS_DIR = "${WORKSPACE}/reports"
        ALLURE_DIR  = "${REPORTS_DIR}/allure-results"
        JUNIT_DIR   = "${REPORTS_DIR}/junit"
        HTML_DIR    = "${REPORTS_DIR}/html"

        // ── App config (set in Jenkins Credentials or .env) ────────────────
        APPIUM_SERVER_URL       = credentials('APPIUM_SERVER_URL')    // optional
        ANDROID_DEVICE_NAME     = credentials('ANDROID_DEVICE_NAME')  // optional
        API_BASE_URL            = credentials('API_BASE_URL')
        BASE_URL                = credentials('BASE_URL')
        BROWSER                 = 'chrome'
        HEADLESS                = 'true'
    }

    options {
        timestamps()
        timeout(time: 60, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
        ansiColor('xterm')
    }

    stages {

        stage('🔧 Setup') {
            steps {
                echo "=== Setting up virtual environment ==="
                sh '''
                    python3 -m venv ${VENV_DIR}
                    ${VENV_DIR}/bin/pip install --upgrade pip
                    ${VENV_DIR}/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('📱 Start Appium') {
            when {
                expression { params.START_APPIUM == true }
            }
            steps {
                echo "=== Starting Appium server ==="
                sh '''
                    nohup npx appium --log /tmp/appium.log &
                    sleep 5
                    echo "Appium started"
                '''
            }
        }

        stage('🧪 Run Tests') {
            steps {
                script {
                    def marker = params.MARKER == 'all' ? '' : "-m ${params.MARKER}"
                    def testPath = params.PROJECT ? "projects/${params.PROJECT}" : "projects"

                    echo "=== Running tests: ${testPath} ${marker} ==="
                    sh """
                        ${VENV_DIR}/bin/pytest ${testPath} ${marker} \
                            -v \
                            --tb=short \
                            --junitxml=${JUNIT_DIR}/results.xml \
                            --html=${HTML_DIR}/report.html \
                            --self-contained-html \
                            --alluredir=${ALLURE_DIR} \
                            --reruns 1 \
                            --reruns-delay 2 \
                            || true
                    """
                }
            }
        }
    }

    post {
        always {
            echo "=== Publishing Reports ==="

            // JUnit results (built-in Jenkins)
            junit(
                testResults: 'reports/junit/results.xml',
                allowEmptyResults: true
            )

            // Allure Report (requires Allure Jenkins Plugin)
            allure([
                includeProperties: true,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'reports/allure-results']]
            ])

            // Archive HTML report and logs
            archiveArtifacts(
                artifacts: 'reports/html/report.html, logs/*.log',
                allowEmptyArchive: true
            )
        }

        success {
            echo "✅ All tests passed!"
        }

        failure {
            echo "❌ Tests failed. Check the Allure and HTML reports."
            // emailext (optional — configure Jenkins email plugin):
            // emailext subject: "Test FAILED: ${JOB_NAME} #${BUILD_NUMBER}",
            //          body: "Check ${BUILD_URL}",
            //          to: 'your-team@example.com'
        }

        cleanup {
            // Stop Appium if we started it
            sh 'pkill -f "appium" || true'
        }
    }
}
