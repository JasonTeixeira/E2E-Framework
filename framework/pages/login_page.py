"""
Login Page Object - SauceDemo Application
Demonstrates Page Object Model implementation
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from framework.core.base_page import BasePage
from loguru import logger


class LoginPage(BasePage):
    """
    Page Object for SauceDemo Login Page.
    Inherits all methods from BasePage.
    """
    
    # Page URL
    URL = "https://www.saucedemo.com"
    
    # Locators (using tuple format for maintainability)
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    ERROR_BUTTON = (By.CSS_SELECTOR, ".error-button")
    LOGO = (By.CSS_SELECTOR, ".login_logo")
    BOT_LOGO = (By.CSS_SELECTOR, ".bot_column")
    
    # Products page locator (for verification)
    PRODUCTS_TITLE = (By.CSS_SELECTOR, ".title")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    
    def __init__(self, driver: WebDriver):
        """Initialize Login Page."""
        super().__init__(driver)
        logger.info("Initialized LoginPage")
        
    def navigate(self) -> 'LoginPage':
        """
        Navigate to login page.
        
        Returns:
            Self for method chaining
        """
        self.navigate_to(self.URL)
        self.wait_for_page_load()
        return self
        
    def wait_for_page_load(self) -> None:
        """Wait for login page to load completely."""
        self.wait_for_element(self.LOGO, timeout=10)
        self.wait_for_element(self.USERNAME_INPUT, timeout=10)
        logger.info("Login page loaded successfully")
        
    def enter_username(self, username: str) -> 'LoginPage':
        """
        Enter username.
        
        Args:
            username: Username to enter
            
        Returns:
            Self for method chaining
        """
        logger.info(f"Entering username: {username}")
        self.enter_text(self.USERNAME_INPUT, username)
        return self
        
    def enter_password(self, password: str) -> 'LoginPage':
        """
        Enter password.
        
        Args:
            password: Password to enter
            
        Returns:
            Self for method chaining
        """
        logger.info("Entering password")
        self.enter_text(self.PASSWORD_INPUT, password)
        return self
        
    def click_login(self) -> None:
        """Click login button."""
        logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)
        
    def login(self, username: str, password: str) -> None:
        """
        Complete login flow.
        
        Args:
            username: Username
            password: Password
        """
        logger.info(f"Logging in with user: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        
    def is_error_displayed(self) -> bool:
        """
        Check if error message is displayed.
        
        Returns:
            True if error is displayed, False otherwise
        """
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=3)
        
    def get_error_message(self) -> str:
        """
        Get error message text.
        
        Returns:
            Error message text
        """
        if self.is_error_displayed():
            error_text = self.get_text(self.ERROR_MESSAGE)
            logger.info(f"Error message: {error_text}")
            return error_text
        return ""
        
    def clear_error(self) -> 'LoginPage':
        """
        Clear error message by clicking X button.
        
        Returns:
            Self for method chaining
        """
        if self.is_error_displayed():
            logger.info("Clearing error message")
            self.click(self.ERROR_BUTTON)
        return self
        
    def is_login_successful(self) -> bool:
        """
        Verify if login was successful by checking for products page.
        
        Returns:
            True if on products page, False otherwise
        """
        try:
            self.wait_for_element(self.INVENTORY_CONTAINER, timeout=10)
            products_title = self.get_text(self.PRODUCTS_TITLE)
            success = products_title == "Products"
            
            if success:
                logger.info("Login successful - Products page loaded")
            else:
                logger.warning("Login may have failed - unexpected page")
                
            return success
        except Exception as e:
            logger.error(f"Login verification failed: {e}")
            return False
            
    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.driver.current_url
        
    def is_on_inventory_page(self) -> bool:
        """
        Check if currently on inventory page.
        
        Returns:
            True if on inventory page
        """
        return "inventory.html" in self.get_current_url()
        
    # ============= Validation Methods =============
    
    def validate_page_elements(self) -> bool:
        """
        Validate all expected page elements are present.
        
        Returns:
            True if all elements present, False otherwise
        """
        logger.info("Validating login page elements")
        
        elements_to_check = [
            (self.USERNAME_INPUT, "Username field"),
            (self.PASSWORD_INPUT, "Password field"),
            (self.LOGIN_BUTTON, "Login button"),
            (self.LOGO, "Logo"),
        ]
        
        all_present = True
        for locator, name in elements_to_check:
            if not self.is_element_present(locator):
                logger.error(f"Missing element: {name}")
                all_present = False
            else:
                logger.debug(f"✓ {name} present")
                
        return all_present
