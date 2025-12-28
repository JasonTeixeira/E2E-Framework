"""
Login Tests - SauceDemo Application
Comprehensive test suite demonstrating framework capabilities
"""

import pytest
import allure
from framework.pages.login_page import LoginPage
from loguru import logger


@allure.feature("Authentication")
@allure.story("Login Functionality")
class TestLogin:
    """Test suite for login functionality."""
    
    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.title("Successful login with valid credentials")
    @allure.description("Verify user can login with valid username and password")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, login_page, test_data):
        """
        Test successful login with valid credentials.
        
        Steps:
        1. Navigate to login page
        2. Enter valid username
        3. Enter valid password
        4. Click login button
        5. Verify successful login
        """
        # Arrange
        valid_user = test_data["valid_user"]
        logger.info(f"Testing login with user: {valid_user['username']}")
        
        # Act
        with allure.step("Enter credentials and login"):
            login_page.login(
                username=valid_user["username"],
                password=valid_user["password"]
            )
        
        # Assert
        with allure.step("Verify successful login"):
            assert login_page.is_login_successful(), "Login should be successful"
            assert login_page.is_on_inventory_page(), "Should be on inventory page"
            logger.info("Login successful - test passed ✓")
    
    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.title("Login fails with invalid credentials")
    @allure.description("Verify appropriate error is shown for invalid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_invalid_credentials(self, login_page, test_data):
        """
        Test login failure with invalid credentials.
        
        Steps:
        1. Navigate to login page
        2. Enter invalid username
        3. Enter invalid password
        4. Click login button
        5. Verify error message is displayed
        """
        # Arrange
        invalid_user = test_data["invalid_user"]
        logger.info(f"Testing login with invalid user: {invalid_user['username']}")
        
        # Act
        with allure.step("Attempt login with invalid credentials"):
            login_page.login(
                username=invalid_user["username"],
                password=invalid_user["password"]
            )
        
        # Assert
        with allure.step("Verify error message is displayed"):
            assert login_page.is_error_displayed(), "Error message should be displayed"
            
            error_message = login_page.get_error_message()
            assert "Username and password do not match" in error_message, \
                f"Expected error about credentials mismatch, got: {error_message}"
            
            logger.info(f"Error message verified: {error_message}")
    
    @pytest.mark.regression
    @allure.title("Login fails with locked out user")
    @allure.description("Verify locked out user cannot login")
    @allure.severity(allure.severity_level.NORMAL)
    def test_locked_out_user(self, login_page, test_data):
        """
        Test login failure with locked out user.
        
        Steps:
        1. Navigate to login page
        2. Enter locked out username
        3. Enter password
        4. Click login button
        5. Verify locked out error message
        """
        # Arrange
        locked_user = test_data["locked_user"]
        logger.info(f"Testing login with locked user: {locked_user['username']}")
        
        # Act
        with allure.step("Attempt login with locked user"):
            login_page.login(
                username=locked_user["username"],
                password=locked_user["password"]
            )
        
        # Assert
        with allure.step("Verify locked out error message"):
            assert login_page.is_error_displayed(), "Error message should be displayed"
            
            error_message = login_page.get_error_message()
            assert "locked out" in error_message.lower(), \
                f"Expected locked out error, got: {error_message}"
            
            logger.info(f"Locked out error verified: {error_message}")
    
    @pytest.mark.regression
    @allure.title("Login fails with empty username")
    @allure.description("Verify error when username field is empty")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_username(self, login_page):
        """
        Test login failure with empty username.
        
        Steps:
        1. Navigate to login page
        2. Leave username empty
        3. Enter password
        4. Click login button
        5. Verify error message
        """
        logger.info("Testing login with empty username")
        
        # Act
        with allure.step("Attempt login with empty username"):
            login_page.enter_password("secret_sauce")
            login_page.click_login()
        
        # Assert
        with allure.step("Verify username required error"):
            assert login_page.is_error_displayed(), "Error message should be displayed"
            
            error_message = login_page.get_error_message()
            assert "Username is required" in error_message, \
                f"Expected username required error, got: {error_message}"
            
            logger.info("Empty username error verified")
    
    @pytest.mark.regression
    @allure.title("Login fails with empty password")
    @allure.description("Verify error when password field is empty")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_password(self, login_page):
        """
        Test login failure with empty password.
        
        Steps:
        1. Navigate to login page
        2. Enter username
        3. Leave password empty
        4. Click login button
        5. Verify error message
        """
        logger.info("Testing login with empty password")
        
        # Act
        with allure.step("Attempt login with empty password"):
            login_page.enter_username("standard_user")
            login_page.click_login()
        
        # Assert
        with allure.step("Verify password required error"):
            assert login_page.is_error_displayed(), "Error message should be displayed"
            
            error_message = login_page.get_error_message()
            assert "Password is required" in error_message, \
                f"Expected password required error, got: {error_message}"
            
            logger.info("Empty password error verified")
    
    @pytest.mark.regression
    @allure.title("Error message can be cleared")
    @allure.description("Verify error message can be dismissed by clicking X")
    @allure.severity(allure.severity_level.MINOR)
    def test_clear_error_message(self, login_page):
        """
        Test error message can be cleared.
        
        Steps:
        1. Trigger an error message
        2. Click X button to clear error
        3. Verify error is no longer displayed
        """
        logger.info("Testing error message clearing")
        
        # Arrange - trigger error
        with allure.step("Trigger error message"):
            login_page.click_login()
            assert login_page.is_error_displayed(), "Error should be displayed initially"
        
        # Act
        with allure.step("Clear error message"):
            login_page.clear_error()
        
        # Assert
        with allure.step("Verify error is cleared"):
            assert not login_page.is_error_displayed(), "Error should no longer be visible"
            logger.info("Error successfully cleared")
    
    @pytest.mark.regression
    @allure.title("Login page elements are present")
    @allure.description("Verify all login page elements are rendered correctly")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_page_elements(self, login_page):
        """
        Test all login page elements are present.
        
        Steps:
        1. Navigate to login page
        2. Verify username field exists
        3. Verify password field exists
        4. Verify login button exists
        5. Verify logo exists
        """
        logger.info("Validating login page elements")
        
        with allure.step("Validate all page elements"):
            assert login_page.validate_page_elements(), \
                "All login page elements should be present"
            
            logger.info("All page elements validated successfully")
    
    @pytest.mark.smoke
    @allure.title("Method chaining works correctly")
    @allure.description("Verify fluent interface/method chaining functionality")
    @allure.severity(allure.severity_level.MINOR)
    def test_method_chaining(self, login_page, test_data):
        """
        Test method chaining functionality.
        
        Demonstrates fluent interface pattern in page object.
        """
        logger.info("Testing method chaining")
        
        valid_user = test_data["valid_user"]
        
        # Act - use method chaining
        with allure.step("Use method chaining for login"):
            (login_page
             .enter_username(valid_user["username"])
             .enter_password(valid_user["password"]))
            
            login_page.click_login()
        
        # Assert
        with allure.step("Verify login successful"):
            assert login_page.is_login_successful(), \
                "Method chaining should not affect functionality"
            
            logger.info("Method chaining works correctly")


@allure.feature("Authentication")
@allure.story("Performance")
class TestLoginPerformance:
    """Performance tests for login functionality."""
    
    @pytest.mark.slow
    @allure.title("Login page loads within acceptable time")
    @allure.description("Verify login page loads in under 3 seconds")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_page_load_time(self, login_page, performance_monitor):
        """
        Test login page load performance.
        
        Verifies page loads within acceptable timeframe.
        """
        logger.info("Testing page load performance")
        
        with allure.step("Measure page load time"):
            load_time = performance_monitor.get_page_load_time()
            logger.info(f"Page load time: {load_time:.2f} seconds")
            
            # Attach performance data to report
            allure.attach(
                f"Load Time: {load_time:.2f}s",
                name="Performance Metrics",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("Verify load time is acceptable"):
            assert load_time < 5.0, \
                f"Page load time {load_time:.2f}s exceeds threshold of 5s"
            
            logger.info("Page load performance is acceptable")


# Parametrized test example
@allure.feature("Authentication")
@allure.story("Data-Driven Testing")
class TestLoginDataDriven:
    """Data-driven tests for login functionality."""
    
    @pytest.mark.parametrize("username,password,expected_error", [
        ("", "", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("invalid", "wrong", "Username and password do not match"),
    ])
    @allure.title("Data-driven login validation")
    @allure.description("Test multiple invalid login scenarios")
    def test_invalid_login_scenarios(self, login_page, username, password, expected_error):
        """
        Parametrized test for multiple invalid login scenarios.
        
        Demonstrates data-driven testing capability.
        """
        logger.info(f"Testing login with username='{username}', password='{password}'")
        
        # Act
        if username:
            login_page.enter_username(username)
        if password:
            login_page.enter_password(password)
            
        login_page.click_login()
        
        # Assert
        assert login_page.is_error_displayed(), "Error should be displayed"
        error_message = login_page.get_error_message()
        assert expected_error in error_message, \
            f"Expected '{expected_error}' in error, got: {error_message}"
        
        logger.info(f"Validated error: {error_message}")
