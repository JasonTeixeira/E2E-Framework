"""
Driver Factory - Centralized WebDriver Management
Handles browser initialization, configuration, and cleanup
"""

from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from loguru import logger


class DriverFactory:
    """
    Factory class for creating and managing WebDriver instances.
    Supports Chrome, Firefox, Edge, and remote execution.
    """

    def __init__(self, browser: str = "chrome", headless: bool = False, 
                 remote_url: Optional[str] = None):
        """
        Initialize the DriverFactory.
        
        Args:
            browser: Browser type (chrome, firefox, edge)
            headless: Run in headless mode
            remote_url: Selenium Grid/Remote WebDriver URL
        """
        self.browser = browser.lower()
        self.headless = headless
        self.remote_url = remote_url
        self.driver: Optional[webdriver.Remote] = None
        
    def create_driver(self) -> webdriver.Remote:
        """
        Create and configure WebDriver instance.
        
        Returns:
            Configured WebDriver instance
            
        Raises:
            ValueError: If browser type is not supported
        """
        logger.info(f"Creating {self.browser} driver (headless={self.headless})")
        
        if self.remote_url:
            return self._create_remote_driver()
            
        driver_map = {
            "chrome": self._create_chrome_driver,
            "firefox": self._create_firefox_driver,
            "edge": self._create_edge_driver,
        }
        
        if self.browser not in driver_map:
            raise ValueError(
                f"Unsupported browser: {self.browser}. "
                f"Supported browsers: {', '.join(driver_map.keys())}"
            )
            
        self.driver = driver_map[self.browser]()
        self._configure_driver()
        return self.driver
    
    def _create_chrome_driver(self) -> webdriver.Chrome:
        """Create Chrome WebDriver with optimized options."""
        options = ChromeOptions()
        
        # Performance optimizations
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        
        # Privacy & Security
        options.add_argument("--incognito")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        })
        
        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
            
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    def _create_firefox_driver(self) -> webdriver.Firefox:
        """Create Firefox WebDriver with optimized options."""
        options = FirefoxOptions()
        
        # Performance optimizations
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("media.volume_scale", "0.0")
        
        if self.headless:
            options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
    
    def _create_edge_driver(self) -> webdriver.Edge:
        """Create Edge WebDriver with optimized options."""
        options = EdgeOptions()
        
        # Performance optimizations
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        if self.headless:
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")
            
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
    
    def _create_remote_driver(self) -> webdriver.Remote:
        """Create Remote WebDriver for Selenium Grid."""
        logger.info(f"Connecting to remote WebDriver at {self.remote_url}")
        
        options = ChromeOptions() if self.browser == "chrome" else FirefoxOptions()
        
        if self.headless:
            options.add_argument("--headless")
            
        return webdriver.Remote(
            command_executor=self.remote_url,
            options=options
        )
    
    def _configure_driver(self) -> None:
        """Apply common configurations to driver."""
        if not self.driver:
            return
            
        # Timeouts
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(30)
        self.driver.set_script_timeout(30)
        
        # Window management
        if not self.headless:
            self.driver.maximize_window()
            
        logger.info(f"Driver configured successfully: {self.driver.session_id}")
    
    def quit_driver(self) -> None:
        """Safely quit the driver and cleanup resources."""
        if self.driver:
            try:
                logger.info(f"Quitting driver: {self.driver.session_id}")
                self.driver.quit()
            except Exception as e:
                logger.error(f"Error quitting driver: {e}")
            finally:
                self.driver = None
    
    def __enter__(self):
        """Context manager entry."""
        return self.create_driver()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.quit_driver()
