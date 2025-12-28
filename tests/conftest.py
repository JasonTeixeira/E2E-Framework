"""
Pytest Configuration and Fixtures
Provides reusable fixtures for test setup and teardown
"""

import pytest
from datetime import datetime
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver
from framework.core.driver_factory import DriverFactory
from framework.config.config_manager import config
from framework.utils.screenshot_helper import ScreenshotHelper
from loguru import logger


# ============= Session-Level Fixtures =============

@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """Configure logging for test session."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logger.add(
        log_file,
        rotation="100 MB",
        retention="30 days",
        level=config.log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}"
    )
    
    logger.info("=" * 80)
    logger.info("TEST SESSION STARTED")
    logger.info(f"Environment: {config.env}")
    logger.info(f"Browser: {config.browser_type}")
    logger.info(f"Base URL: {config.base_url}")
    logger.info("=" * 80)
    
    yield
    
    logger.info("=" * 80)
    logger.info("TEST SESSION COMPLETED")
    logger.info("=" * 80)


@pytest.fixture(scope="session")
def test_config():
    """Provide configuration object to tests."""
    return config


# ============= Function-Level Fixtures =============

@pytest.fixture(scope="function")
def driver(request):
    """
    Create WebDriver instance for each test.
    Handles setup and teardown automatically.
    """
    # Get browser settings from config
    browser = config.browser_type
    headless = config.headless
    
    # Allow override via pytest CLI
    browser = request.config.getoption("--browser", browser)
    
    logger.info(f"Initializing {browser} driver for test: {request.node.name}")
    
    # Create driver
    driver_factory = DriverFactory(browser=browser, headless=headless)
    driver_instance = driver_factory.create_driver()
    
    # Store driver in request for screenshot on failure
    request.node._driver = driver_instance
    
    yield driver_instance
    
    # Teardown
    logger.info(f"Tearing down driver for test: {request.node.name}")
    driver_factory.quit_driver()


@pytest.fixture(scope="function")
def screenshot_helper(driver):
    """Provide screenshot helper instance."""
    return ScreenshotHelper(driver)


# ============= Page Object Fixtures =============

@pytest.fixture(scope="function")
def login_page(driver):
    """
    Provide Login Page Object instance.
    Automatically navigates to login page.
    """
    from framework.pages.login_page import LoginPage
    page = LoginPage(driver)
    page.navigate()
    return page


# ============= Pytest Hooks =============

def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment to run tests: dev, staging, prod"
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture test execution result.
    Captures screenshot on test failure.
    """
    outcome = yield
    report = outcome.get_result()
    
    # Only capture on test call phase (not setup/teardown)
    if report.when == "call":
        # Get driver from item if available
        driver = getattr(item, "_driver", None)
        
        if report.failed and driver:
            # Capture screenshot on failure
            screenshot_dir = Path("screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"FAIL_{item.name}_{timestamp}.png"
            screenshot_path = screenshot_dir / screenshot_name
            
            try:
                driver.save_screenshot(str(screenshot_path))
                logger.error(f"Test failed: {item.name}")
                logger.error(f"Screenshot saved: {screenshot_path}")
                
                # Attach to Allure report if available
                try:
                    import allure
                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name=f"failure_{item.name}",
                        attachment_type=allure.attachment_type.PNG
                    )
                except ImportError:
                    pass
                    
            except Exception as e:
                logger.error(f"Failed to capture screenshot: {e}")


def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers", "smoke: Quick smoke tests"
    )
    config.addinivalue_line(
        "markers", "regression: Full regression suite"
    )
    config.addinivalue_line(
        "markers", "critical: Critical path tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection (e.g., skip tests based on markers)."""
    skip_ci = pytest.mark.skip(reason="Skipped in CI environment")
    
    for item in items:
        if "skip_ci" in item.keywords and config.getoption("--ci", False):
            item.add_marker(skip_ci)


@pytest.fixture(scope="function")
def test_data():
    """
    Provide test data for tests.
    Can be extended to load from files, databases, etc.
    """
    return {
        "valid_user": {
            "username": "standard_user",
            "password": "secret_sauce"
        },
        "locked_user": {
            "username": "locked_out_user",
            "password": "secret_sauce"
        },
        "invalid_user": {
            "username": "invalid_user",
            "password": "wrong_password"
        }
    }


@pytest.fixture(autouse=True)
def log_test_name(request):
    """Log test name at start and end."""
    logger.info(f"{'=' * 60}")
    logger.info(f"Starting test: {request.node.name}")
    logger.info(f"{'=' * 60}")
    
    yield
    
    logger.info(f"{'=' * 60}")
    logger.info(f"Finished test: {request.node.name}")
    logger.info(f"{'=' * 60}")


# ============= Performance Monitoring =============

@pytest.fixture(scope="function")
def performance_monitor(driver):
    """Monitor page performance metrics."""
    class PerformanceMonitor:
        def get_page_load_time(self):
            """Get page load time in seconds."""
            navigation_start = driver.execute_script(
                "return window.performance.timing.navigationStart"
            )
            load_complete = driver.execute_script(
                "return window.performance.timing.loadEventEnd"
            )
            return (load_complete - navigation_start) / 1000
            
        def get_dom_ready_time(self):
            """Get DOM ready time in seconds."""
            navigation_start = driver.execute_script(
                "return window.performance.timing.navigationStart"
            )
            dom_ready = driver.execute_script(
                "return window.performance.timing.domContentLoadedEventEnd"
            )
            return (dom_ready - navigation_start) / 1000
            
    return PerformanceMonitor()
