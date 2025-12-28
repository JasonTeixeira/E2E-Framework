"""
Configuration Manager - Centralized configuration handling
Supports YAML configs, environment variables, and runtime overrides
"""

import os
import yaml
from typing import Any, Dict, Optional
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger


class ConfigManager:
    """
    Centralized configuration management with multiple sources.
    Priority: Runtime > Environment Variables > Config File > Defaults
    """
    
    _instance = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        """Singleton pattern to ensure single config instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize configuration manager."""
        if self._initialized:
            return
            
        self._initialized = True
        self._load_env_variables()
        self._load_config_file()
        self._set_defaults()
        logger.info("Configuration Manager initialized")
        
    def _load_env_variables(self) -> None:
        """Load environment variables from .env file."""
        env_file = Path(__file__).parent.parent.parent / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            logger.info(f"Loaded environment variables from {env_file}")
        else:
            logger.warning("No .env file found")
            
    def _load_config_file(self) -> None:
        """Load configuration from YAML file."""
        # Determine environment
        env = os.getenv("TEST_ENV", "dev")
        config_dir = Path(__file__).parent.parent.parent / "config"
        config_file = config_dir / f"{env}_config.yml"
        
        if not config_file.exists():
            logger.warning(f"Config file not found: {config_file}")
            return
            
        try:
            with open(config_file, 'r') as f:
                self._config = yaml.safe_load(f) or {}
            logger.info(f"Loaded configuration from {config_file}")
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            
    def _set_defaults(self) -> None:
        """Set default values for essential configurations."""
        defaults = {
            "browser": {
                "type": "chrome",
                "headless": False,
                "timeout": 10,
                "page_load_timeout": 30,
            },
            "app": {
                "url": "https://www.saucedemo.com",
                "env": "dev",
            },
            "selenium": {
                "implicit_wait": 10,
                "explicit_wait": 10,
                "page_load_timeout": 30,
            },
            "reporting": {
                "screenshots_on_failure": True,
                "video_recording": False,
                "allure_results_dir": "allure-results",
            },
            "execution": {
                "parallel": False,
                "workers": 4,
                "retry_failed": True,
                "max_retries": 2,
            },
            "logging": {
                "level": "INFO",
                "file": "logs/test_execution.log",
                "console": True,
            },
        }
        
        # Merge defaults with loaded config (loaded config takes priority)
        for section, values in defaults.items():
            if section not in self._config:
                self._config[section] = values
            else:
                for key, value in values.items():
                    if key not in self._config[section]:
                        self._config[section][key] = value
                        
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'browser.type')
            default: Default value if key not found
            
        Returns:
            Configuration value
            
        Example:
            config.get('browser.type')  # Returns 'chrome'
            config.get('app.url')  # Returns app URL
        """
        # Check environment variable first
        env_key = key.upper().replace('.', '_')
        env_value = os.getenv(env_key)
        if env_value is not None:
            return env_value
            
        # Navigate through nested dict
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            logger.debug(f"Config key not found: {key}, returning default: {default}")
            return default
            
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'browser.type')
            value: Value to set
        """
        keys = key.split('.')
        config = self._config
        
        # Navigate to the last level
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        # Set the value
        config[keys[-1]] = value
        logger.debug(f"Set config: {key} = {value}")
        
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section.
        
        Args:
            section: Section name (e.g., 'browser')
            
        Returns:
            Dictionary of section configuration
        """
        return self._config.get(section, {})
        
    def update_section(self, section: str, values: Dict[str, Any]) -> None:
        """
        Update entire section with new values.
        
        Args:
            section: Section name
            values: Dictionary of values to update
        """
        if section not in self._config:
            self._config[section] = {}
            
        self._config[section].update(values)
        logger.debug(f"Updated section: {section}")
        
    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration."""
        return self._config.copy()
        
    # ============= Convenience Methods =============
    
    @property
    def browser_type(self) -> str:
        """Get browser type."""
        return self.get('browser.type', 'chrome')
        
    @property
    def headless(self) -> bool:
        """Get headless mode setting."""
        return self.get('browser.headless', False)
        
    @property
    def base_url(self) -> str:
        """Get base application URL."""
        return self.get('app.url', '')
        
    @property
    def timeout(self) -> int:
        """Get default timeout."""
        return self.get('browser.timeout', 10)
        
    @property
    def env(self) -> str:
        """Get current environment."""
        return self.get('app.env', 'dev')
        
    @property
    def parallel_execution(self) -> bool:
        """Get parallel execution setting."""
        return self.get('execution.parallel', False)
        
    @property
    def workers(self) -> int:
        """Get number of parallel workers."""
        return self.get('execution.workers', 4)
        
    @property
    def screenshots_on_failure(self) -> bool:
        """Get screenshot on failure setting."""
        return self.get('reporting.screenshots_on_failure', True)
        
    @property
    def video_recording(self) -> bool:
        """Get video recording setting."""
        return self.get('reporting.video_recording', False)
        
    @property
    def log_level(self) -> str:
        """Get logging level."""
        return self.get('logging.level', 'INFO')
        
    def print_config(self) -> None:
        """Print current configuration (useful for debugging)."""
        import json
        logger.info("Current Configuration:")
        logger.info(json.dumps(self._config, indent=2))


# Global instance
config = ConfigManager()
