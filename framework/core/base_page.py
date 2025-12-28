"""
Base Page - Foundation for Page Object Model
Provides reusable methods for all page objects
"""

from typing import List, Optional, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, 
    StaleElementReferenceException
)
from loguru import logger
import time


class BasePage:
    """
    Base Page Object providing common functionality for all pages.
    Implements robust waiting, error handling, and interaction methods.
    """

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initialize Base Page.
        
        Args:
            driver: WebDriver instance
            timeout: Default explicit wait timeout (seconds)
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        
    # ============= Navigation Methods =============
    
    def navigate_to(self, url: str) -> None:
        """Navigate to specified URL."""
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)
        
    def refresh_page(self) -> None:
        """Refresh current page."""
        logger.info("Refreshing page")
        self.driver.refresh()
        
    def go_back(self) -> None:
        """Navigate back in browser history."""
        logger.info("Navigating back")
        self.driver.back()
        
    def go_forward(self) -> None:
        """Navigate forward in browser history."""
        logger.info("Navigating forward")
        self.driver.forward()
        
    # ============= Wait Methods =============
    
    def wait_for_element(self, locator: Tuple[By, str], 
                         timeout: Optional[int] = None) -> WebElement:
        """
        Wait for element to be present and visible.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Override default timeout
            
        Returns:
            WebElement when found and visible
            
        Raises:
            TimeoutException: If element not found within timeout
        """
        timeout = timeout or self.timeout
        logger.debug(f"Waiting for element: {locator}")
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element not found within {timeout}s: {locator}")
            raise
            
    def wait_for_elements(self, locator: Tuple[By, str],
                          timeout: Optional[int] = None) -> List[WebElement]:
        """Wait for multiple elements to be present."""
        timeout = timeout or self.timeout
        logger.debug(f"Waiting for elements: {locator}")
        
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            logger.error(f"Elements not found within {timeout}s: {locator}")
            raise
            
    def wait_for_element_clickable(self, locator: Tuple[By, str],
                                   timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be clickable."""
        timeout = timeout or self.timeout
        logger.debug(f"Waiting for element to be clickable: {locator}")
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element not clickable within {timeout}s: {locator}")
            raise
            
    def wait_for_element_invisible(self, locator: Tuple[By, str],
                                   timeout: Optional[int] = None) -> bool:
        """Wait for element to become invisible."""
        timeout = timeout or self.timeout
        logger.debug(f"Waiting for element to be invisible: {locator}")
        
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"Element still visible after {timeout}s: {locator}")
            return False
            
    def wait_for_url_contains(self, text: str, 
                             timeout: Optional[int] = None) -> bool:
        """Wait for URL to contain specified text."""
        timeout = timeout or self.timeout
        logger.debug(f"Waiting for URL to contain: {text}")
        
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.url_contains(text)
            )
        except TimeoutException:
            logger.error(f"URL doesn't contain '{text}' after {timeout}s")
            return False
            
    # ============= Element Interaction Methods =============
    
    def click(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """
        Click element with retry logic.
        
        Args:
            locator: Element locator
            timeout: Override default timeout
        """
        element = self.wait_for_element_clickable(locator, timeout)
        logger.info(f"Clicking element: {locator}")
        
        try:
            element.click()
        except Exception as e:
            logger.warning(f"Regular click failed, trying JavaScript click: {e}")
            self.driver.execute_script("arguments[0].click();", element)
            
    def enter_text(self, locator: Tuple[By, str], text: str,
                   clear_first: bool = True, timeout: Optional[int] = None) -> None:
        """
        Enter text into input field.
        
        Args:
            locator: Element locator
            text: Text to enter
            clear_first: Clear field before entering text
            timeout: Override default timeout
        """
        element = self.wait_for_element(locator, timeout)
        logger.info(f"Entering text into: {locator}")
        
        if clear_first:
            element.clear()
            
        element.send_keys(text)
        
    def get_text(self, locator: Tuple[By, str], 
                 timeout: Optional[int] = None) -> str:
        """Get text content of element."""
        element = self.wait_for_element(locator, timeout)
        text = element.text
        logger.debug(f"Got text from {locator}: {text}")
        return text
        
    def get_attribute(self, locator: Tuple[By, str], attribute: str,
                     timeout: Optional[int] = None) -> Optional[str]:
        """Get attribute value of element."""
        element = self.wait_for_element(locator, timeout)
        value = element.get_attribute(attribute)
        logger.debug(f"Got attribute '{attribute}' from {locator}: {value}")
        return value
        
    def is_element_visible(self, locator: Tuple[By, str],
                          timeout: Optional[int] = None) -> bool:
        """Check if element is visible."""
        timeout = timeout or self.timeout
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
            
    def is_element_present(self, locator: Tuple[By, str]) -> bool:
        """Check if element is present in DOM."""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
            
    # ============= Advanced Interaction Methods =============
    
    def hover_over(self, locator: Tuple[By, str], 
                   timeout: Optional[int] = None) -> None:
        """Hover mouse over element."""
        element = self.wait_for_element(locator, timeout)
        logger.info(f"Hovering over: {locator}")
        
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        
    def double_click(self, locator: Tuple[By, str],
                    timeout: Optional[int] = None) -> None:
        """Double click element."""
        element = self.wait_for_element(locator, timeout)
        logger.info(f"Double clicking: {locator}")
        
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        
    def right_click(self, locator: Tuple[By, str],
                   timeout: Optional[int] = None) -> None:
        """Right click (context click) element."""
        element = self.wait_for_element(locator, timeout)
        logger.info(f"Right clicking: {locator}")
        
        actions = ActionChains(self.driver)
        actions.context_click(element).perform()
        
    def drag_and_drop(self, source: Tuple[By, str], target: Tuple[By, str],
                     timeout: Optional[int] = None) -> None:
        """Drag source element and drop on target."""
        source_element = self.wait_for_element(source, timeout)
        target_element = self.wait_for_element(target, timeout)
        logger.info(f"Drag and drop from {source} to {target}")
        
        actions = ActionChains(self.driver)
        actions.drag_and_drop(source_element, target_element).perform()
        
    def scroll_to_element(self, locator: Tuple[By, str],
                         timeout: Optional[int] = None) -> None:
        """Scroll element into view."""
        element = self.wait_for_element(locator, timeout)
        logger.info(f"Scrolling to element: {locator}")
        
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.3)  # Allow scroll animation
        
    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of page."""
        logger.info("Scrolling to bottom of page")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
    def scroll_to_top(self) -> None:
        """Scroll to top of page."""
        logger.info("Scrolling to top of page")
        self.driver.execute_script("window.scrollTo(0, 0);")
        
    # ============= JavaScript Execution =============
    
    def execute_script(self, script: str, *args) -> any:
        """Execute JavaScript in browser."""
        logger.debug(f"Executing JavaScript: {script}")
        return self.driver.execute_script(script, *args)
        
    def highlight_element(self, locator: Tuple[By, str],
                         timeout: Optional[int] = None) -> None:
        """Highlight element (useful for debugging)."""
        element = self.wait_for_element(locator, timeout)
        original_style = element.get_attribute("style")
        
        # Apply highlight
        self.driver.execute_script(
            "arguments[0].setAttribute('style', 'border: 2px solid red; background: yellow;');",
            element
        )
        time.sleep(0.5)
        
        # Restore original style
        self.driver.execute_script(
            f"arguments[0].setAttribute('style', '{original_style}');",
            element
        )
        
    # ============= Utility Methods =============
    
    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.driver.current_url
        
    def get_page_title(self) -> str:
        """Get page title."""
        return self.driver.title
        
    def switch_to_frame(self, locator: Tuple[By, str],
                       timeout: Optional[int] = None) -> None:
        """Switch to iframe."""
        frame = self.wait_for_element(locator, timeout)
        logger.info(f"Switching to frame: {locator}")
        self.driver.switch_to.frame(frame)
        
    def switch_to_default_content(self) -> None:
        """Switch back to default content from iframe."""
        logger.info("Switching to default content")
        self.driver.switch_to.default_content()
        
    def switch_to_window(self, window_handle: str) -> None:
        """Switch to window by handle."""
        logger.info(f"Switching to window: {window_handle}")
        self.driver.switch_to.window(window_handle)
        
    def get_window_handles(self) -> List[str]:
        """Get all window handles."""
        return self.driver.window_handles
        
    def accept_alert(self, timeout: Optional[int] = None) -> None:
        """Accept browser alert."""
        timeout = timeout or self.timeout
        logger.info("Accepting alert")
        
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            logger.warning("No alert present to accept")
            
    def dismiss_alert(self, timeout: Optional[int] = None) -> None:
        """Dismiss browser alert."""
        timeout = timeout or self.timeout
        logger.info("Dismissing alert")
        
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.dismiss()
        except TimeoutException:
            logger.warning("No alert present to dismiss")
            
    def get_alert_text(self, timeout: Optional[int] = None) -> Optional[str]:
        """Get alert text."""
        timeout = timeout or self.timeout
        
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            return alert.text
        except TimeoutException:
            logger.warning("No alert present")
            return None
