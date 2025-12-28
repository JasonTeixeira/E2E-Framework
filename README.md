# 🚀 Enterprise E2E Test Automation Framework

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.16.0-green.svg)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/pytest-7.4.3-yellow.svg)](https://pytest.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **A production-ready, scalable test automation framework built with Selenium, Pytest, and modern best practices**

Enterprise-grade E2E testing framework demonstrating advanced automation patterns, comprehensive reporting, and CI/CD integration. Built to showcase professional QA engineering skills for interviews and production use.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#️-configuration)
- [Running Tests](#-running-tests)
- [Reports & Logging](#-reports--logging)
- [Project Structure](#-project-structure)
- [CI/CD Integration](#-cicd-integration)
- [Best Practices](#-best-practices)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🏗️ **Framework Architecture**
- ✅ **Page Object Model (POM)** - Maintainable and scalable test structure
- ✅ **Factory Pattern** - Centralized WebDriver management
- ✅ **Singleton Configuration** - Unified config management
- ✅ **Fluent Interface** - Method chaining for readable tests
- ✅ **Base Page Class** - 50+ reusable interaction methods

### 🧪 **Testing Capabilities**
- ✅ **Cross-Browser Testing** - Chrome, Firefox, Edge support
- ✅ **Parallel Execution** - Run tests concurrently with pytest-xdist
- ✅ **Retry Mechanism** - Auto-retry flaky tests
- ✅ **Data-Driven Testing** - Parametrized tests with multiple datasets
- ✅ **Screenshot on Failure** - Automatic failure evidence capture
- ✅ **Visual Regression** - Image comparison capabilities

### 📊 **Reporting & Monitoring**
- ✅ **Allure Reports** - Beautiful, interactive test reports
- ✅ **HTML Reports** - Self-contained HTML test results
- ✅ **Structured Logging** - Comprehensive logging with Loguru
- ✅ **Performance Monitoring** - Page load time tracking
- ✅ **Test Metrics** - Execution time, pass/fail rates

### ⚙️ **DevOps Integration**
- ✅ **Docker Support** - Containerized test execution
- ✅ **CI/CD Ready** - GitHub Actions, Jenkins integration
- ✅ **Selenium Grid** - Distributed test execution
- ✅ **Environment Management** - Multiple environment configs
- ✅ **Secret Management** - .env file support

---

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   TEST LAYER                         │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │  E2E Tests  │  │   API Tests  │  │ Unit Tests │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────┐
│                PAGE OBJECT LAYER                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │LoginPage │  │HomePage  │  │CartPage  │  ...     │
│  └──────────┘  └──────────┘  └──────────┘          │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────┐
│                 FRAMEWORK CORE                       │
│  ┌──────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │ BasePage     │  │DriverFactory│  │ ConfigMgr  │ │
│  │ 480+ lines   │  │ 200+ lines  │  │ 350+ lines │ │
│  └──────────────┘  └─────────────┘  └────────────┘ │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────┐
│                UTILITIES LAYER                       │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ Screenshot   │  │ Logger       │  │ Reporters │ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
└─────────────────────────────────────────────────────┘
```

**Design Patterns Implemented:**
- 🎨 **Page Object Model** - Separation of test logic and page structure
- 🏭 **Factory Pattern** - WebDriver creation and management
- 🔒 **Singleton Pattern** - Configuration management
- 🔗 **Fluent Interface** - Chainable method calls
- 📦 **Dependency Injection** - Pytest fixtures

---

## 🔧 Prerequisites

- **Python**: 3.8 or higher
- **pip**: Latest version
- **Browser**: Chrome, Firefox, or Edge installed
- **Git**: For cloning the repository

```bash
# Verify Python version
python --version  # Should be 3.8+

# Verify pip
pip --version
```

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/JasonTeixeira/Qa-Automation-Project.git
cd Qa-Automation-Project
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Install in development mode (optional)
pip install -e .
```

### 4. Verify Installation

```bash
# Check pytest installation
pytest --version

# Check Selenium
python -c "import selenium; print(selenium.__version__)"
```

---

## 🚀 Quick Start

### Run Your First Test

```bash
# Run all tests
pytest

# Run with detailed output
pytest -v

# Run specific test file
pytest tests/e2e/test_login.py

# Run specific test
pytest tests/e2e/test_login.py::TestLogin::test_successful_login
```

### Expected Output

```
================================= test session starts ==================================
platform darwin -- Python 3.11.0, pytest-7.4.3, pluggy-1.3.0
plugins: html-4.1.1, metadata-3.0.0, allure-pytest-2.13.2
collected 10 items

tests/e2e/test_login.py::TestLogin::test_successful_login PASSED             [ 10%]
tests/e2e/test_login.py::TestLogin::test_invalid_credentials PASSED          [ 20%]
tests/e2e/test_login.py::TestLogin::test_locked_out_user PASSED              [ 30%]
...

================================== 10 passed in 45.23s =================================
```

---

## ⚙️ Configuration

### Environment-Specific Configs

Configurations are in `config/` directory:

```yaml
# config/dev_config.yml
browser:
  type: chrome          # chrome, firefox, edge
  headless: false       # true for CI/CD
  timeout: 15

app:
  url: https://www.saucedemo.com
  env: dev

execution:
  parallel: false       # Enable for parallel execution
  workers: 4           # Number of parallel workers
  retry_failed: true
  max_retries: 2
```

### Environment Variables

Create `.env` file in root directory:

```bash
# Browser settings
BROWSER_TYPE=chrome
BROWSER_HEADLESS=false

# Application URL
APP_URL=https://www.saucedemo.com

# Test environment
TEST_ENV=dev

# Credentials (DO NOT commit real credentials!)
TEST_USERNAME=standard_user
TEST_PASSWORD=secret_sauce
```

---

## 🏃 Running Tests

### Basic Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v -s

# Run specific markers
pytest -m smoke         # Smoke tests only
pytest -m regression    # Regression tests
pytest -m critical      # Critical tests

# Run in headless mode
pytest --headless

# Run with specific browser
pytest --browser=firefox
pytest --browser=edge
```

### Parallel Execution

```bash
# Run tests in parallel (auto-detect cores)
pytest -n auto

# Run with specific number of workers
pytest -n 4

# Parallel with verbose output
pytest -n 4 -v
```

### Advanced Options

```bash
# Stop on first failure
pytest -x

# Run only failed tests from last run
pytest --lf

# Run failed tests first, then others
pytest --ff

# Show slowest 10 tests
pytest --durations=10

# Generate coverage report
pytest --cov=framework --cov-report=html
```

---

## 📊 Reports & Logging

### Allure Reports

```bash
# Generate Allure report
pytest --alluredir=allure-results

# Serve Allure report
allure serve allure-results

# Generate static Allure report
allure generate allure-results --clean -o allure-report
```

**Allure Report Features:**
- 📈 Test execution trends
- 📸 Screenshot attachments
- ⏱️ Execution timeline
- 📊 Test categorization
- 🔍 Detailed step-by-step execution

### HTML Reports

```bash
# HTML report (auto-generated)
pytest --html=reports/report.html --self-contained-html
```

### Logs

Logs are automatically generated in `logs/` directory:

```
logs/
├── test_20240127_143022.log    # Session log
└── pytest.log                   # Pytest log
```

**Log Levels:**
- 🔵 DEBUG - Detailed debugging info
- 🟢 INFO - General information
- 🟡 WARNING - Warning messages
- 🔴 ERROR - Error messages
- 🟣 CRITICAL - Critical failures

---

## 📁 Project Structure

```
Qa-Automation-Project/
│
├── framework/                    # Core framework code
│   ├── core/                    # Core components
│   │   ├── driver_factory.py   # WebDriver management (200+ lines)
│   │   └── base_page.py         # Base page class (480+ lines)
│   ├── config/                  # Configuration management
│   │   └── config_manager.py    # Config handler (350+ lines)
│   ├── pages/                   # Page Objects
│   │   └── login_page.py        # Login page (180+ lines)
│   └── utils/                   # Utility functions
│       └── screenshot_helper.py # Screenshot utilities (250+ lines)
│
├── tests/                       # Test suites
│   ├── conftest.py             # Pytest fixtures (250+ lines)
│   ├── e2e/                    # E2E tests
│   │   └── test_login.py       # Login tests (300+ lines)
│   └── api/                    # API tests
│
├── config/                      # Environment configs
│   ├── dev_config.yml          # Development
│   ├── staging_config.yml      # Staging
│   └── prod_config.yml         # Production
│
├── reports/                     # Test reports
│   ├── allure-results/         # Allure raw data
│   ├── allure-report/          # Allure HTML
│   └── report.html             # Pytest HTML
│
├── screenshots/                 # Failure screenshots
├── logs/                       # Execution logs
│
├── .github/                    # CI/CD workflows
│   └── workflows/
│       └── tests.yml           # GitHub Actions
│
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── setup.py                    # Package setup
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

**Total Lines of Code: 2,000+** 🎉

---

## 🔄 CI/CD Integration

### GitHub Actions

Workflow file: `.github/workflows/tests.yml`

```yaml
name: Automated Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --headless -n auto
      - name: Generate Allure Report
        if: always()
        run: allure generate allure-results
```

### Jenkins

```groovy
pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh '. venv/bin/activate && pytest --headless -n auto'
            }
        }
        stage('Report') {
            steps {
                allure includeProperties: false, results: [[path: 'allure-results']]
            }
        }
    }
}
```

---

## 💡 Best Practices

### ✅ Code Quality
- **Type Hints**: All functions have type annotations
- **Docstrings**: Comprehensive documentation for all methods
- **Linting**: Use Black, Pylint for code formatting
- **100+ Lines Per Module**: Demonstrates depth of knowledge

### ✅ Test Organization
- **Markers**: Use @pytest.mark for test categorization
- **Fixtures**: Leverage pytest fixtures for setup/teardown
- **Parametrize**: Data-driven tests with @pytest.mark.parametrize
- **Allure Decorations**: Rich reporting with @allure decorators

### ✅ Maintenance
- **Explicit Waits**: Always use WebDriverWait, never sleep()
- **Error Handling**: Try-except blocks with proper logging
- **Screenshot on Failure**: Automatic failure evidence
- **Retry Logic**: Built-in test retry for flaky tests

### ✅ Performance
- **Parallel Execution**: Run tests concurrently
- **Headless Mode**: Faster execution in CI/CD
- **Smart Selectors**: Efficient locator strategies
- **Page Load Monitoring**: Track performance metrics

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Jason Teixeira**
- GitHub: [@JasonTeixeira](https://github.com/JasonTeixeira)
- Email: sage@sageideas.org
- Portfolio: [Your Portfolio URL]

---

## 🌟 Acknowledgments

- Built with modern Python best practices
- Follows industry-standard design patterns
- Production-ready architecture
- Interview-ready demonstration project

---

## 📈 Project Stats

- **Total Lines of Code**: 2,000+
- **Framework Components**: 8 core modules
- **Test Cases**: 10+ comprehensive tests
- **Page Objects**: Fully implemented POM
- **Code Coverage**: Comprehensive
- **Documentation**: Extensive inline docs

---

## 🎯 Skills Demonstrated

| Skill | Implementation |
|-------|----------------|
| **Python** | Advanced OOP, type hints, decorators |
| **Selenium** | WebDriver management, waits, interactions |
| **Pytest** | Fixtures, markers, parametrization, hooks |
| **Design Patterns** | Factory, Singleton, Page Object, Fluent Interface |
| **Architecture** | Scalable, maintainable, production-ready |
| **CI/CD** | GitHub Actions, Jenkins integration |
| **Reporting** | Allure, HTML, logging |
| **DevOps** | Docker, Selenium Grid, parallel execution |

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

**[Report Bug](https://github.com/JasonTeixeira/Qa-Automation-Project/issues)** · **[Request Feature](https://github.com/JasonTeixeira/Qa-Automation-Project/issues)**

Made with ❤️ by Jason Teixeira

</div>
