# Test Automation Framework

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.16.0-green.svg)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/pytest-7.4.3-yellow.svg)](https://pytest.org/)

> A scalable Selenium + Pytest framework for end-to-end web testing

I built this framework to demonstrate how I approach test automation - focusing on maintainability, reliability, and real-world practicality rather than over-engineering.

---

## What's This About?

This is a full-featured test automation framework that handles the challenges you actually face in QA work:

- **Flaky tests?** Built-in retry logic with smart waits
- **Multiple environments?** Configuration management that makes sense
- **Debugging failures?** Automatic screenshots and detailed logging
- **Parallel execution?** Ready to go out of the box
- **Different browsers?** Chrome, Firefox, Edge supported

The goal was to create something that could actually be used on a real project, not just a proof of concept.

---

## Key Features

### Architecture
- **Page Object Model** - Keeps tests clean and maintainable
- **Base Page class** - Reusable methods for common interactions (clicks, waits, typing, etc.)
- **Factory Pattern** - Centralized WebDriver management
- **Smart Configuration** - Environment-specific settings without hardcoding

### Testing Capabilities
- **Cross-browser testing** - Tested on Chrome, Firefox, and Edge
- **Parallel execution** - Run tests concurrently to save time
- **Automatic retries** - Handle intermittent failures gracefully  
- **Data-driven tests** - Parameterized tests for testing multiple scenarios
- **Screenshot capture** - Automatically saves evidence when tests fail

### Reporting & Debugging
- **Allure reports** - Interactive HTML reports with test history
- **Structured logging** - Clear logs that actually help debug issues
- **Performance tracking** - Monitor page load times and test execution

---

## Getting Started

### Prerequisites

You'll need:
- Python 3.8 or higher
- pip (Python package installer)
- Chrome, Firefox, or Edge browser

### Installation

```bash
# Clone the repo
git clone https://github.com/JasonTeixeira/Qa-Automation-Project.git
cd Qa-Automation-Project

# Set up virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Your First Test

```bash
# Run all tests
pytest

# Run with more detail
pytest -v

# Run a specific test file
pytest tests/e2e/test_login.py
```

---

## Configuration

The framework uses YAML config files for different environments. Here's what a config looks like:

```yaml
browser:
  type: chrome
  headless: false
  timeout: 15

app:
  url: https://www.saucedemo.com
  env: dev

execution:
  parallel: false
  workers: 4
  retry_failed: true
```

You can also use environment variables for sensitive data - create a `.env` file:

```bash
BROWSER_TYPE=chrome
APP_URL=https://www.saucedemo.com
TEST_USERNAME=standard_user
TEST_PASSWORD=secret_sauce
```

---

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run in parallel (much faster)
pytest -n auto

# Run specific test categories
pytest -m smoke
pytest -m regression

# Run in headless mode
pytest --headless

# Different browser
pytest --browser=firefox
```

### When Tests Fail

- Screenshots are automatically saved to `screenshots/`
- Check logs in `logs/` for detailed execution info
- Allure reports show step-by-step execution: `allure serve allure-results`

---

## Project Structure

```
Qa-Automation-Project/
├── framework/                   # Core framework code
│   ├── core/                   # WebDriver management, base page
│   ├── config/                 # Configuration handling
│   ├── pages/                  # Page objects
│   └── utils/                  # Helper utilities
│
├── tests/                      # Test suites
│   ├── conftest.py            # Pytest fixtures
│   ├── e2e/                   # End-to-end tests
│   └── api/                   # API tests
│
├── config/                     # Environment configs
│   ├── dev_config.yml
│   ├── staging_config.yml
│   └── prod_config.yml
│
├── reports/                    # Test reports
├── screenshots/                # Failure screenshots
├── logs/                      # Execution logs
└── requirements.txt           # Python dependencies
```

---

## Design Decisions

### Why Page Object Model?

I used POM because it makes tests way more maintainable. When a UI element changes, you update it in one place (the page object) rather than hunting through dozens of test files.

### Why the Factory Pattern?

WebDriver setup can get messy. The factory pattern keeps all that browser initialization logic in one place, making it easier to add new browsers or tweak settings.

### Why Explicit Waits?

Nobody wants flaky tests. I avoid `sleep()` calls and use WebDriverWait throughout, which makes tests more reliable and faster.

---

## CI/CD Integration

The framework works out of the box with GitHub Actions or Jenkins. Here's a simple GitHub Actions workflow:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --headless -n auto
```

---

## What I Learned

Building this taught me a lot about:
- How to structure a framework that others can actually use
- The importance of good logging (debugging is way easier)
- Balancing flexibility with simplicity
- Why explicit waits matter so much for stability

---

## Contributing

If you find issues or have ideas for improvements, feel free to open an issue or pull request. Always happy to discuss better approaches!

---

## Author

**Jason Teixeira**
- GitHub: [@JasonTeixeira](https://github.com/JasonTeixeira)
- Email: sage@sageideas.org

---

## License

MIT License - feel free to use this however you want.
