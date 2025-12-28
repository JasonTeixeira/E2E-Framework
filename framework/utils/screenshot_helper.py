"""
Screenshot Helper - Capture and manage test screenshots
Supports failure screenshots, comparison, and annotations
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from loguru import logger


class ScreenshotHelper:
    """Helper class for capturing and managing screenshots."""
    
    def __init__(self, driver: WebDriver, screenshots_dir: str = "screenshots"):
        """
        Initialize Screenshot Helper.
        
        Args:
            driver: WebDriver instance
            screenshots_dir: Directory to save screenshots
        """
        self.driver = driver
        self.screenshots_dir = Path(screenshots_dir)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        
    def capture_screenshot(self, name: str, prefix: str = "") -> str:
        """
        Capture screenshot with timestamp.
        
        Args:
            name: Screenshot name
            prefix: Optional prefix (e.g., 'PASS', 'FAIL')
            
        Returns:
            Path to saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{name}_{timestamp}.png" if prefix else f"{name}_{timestamp}.png"
        filepath = self.screenshots_dir / filename
        
        try:
            self.driver.save_screenshot(str(filepath))
            logger.info(f"Screenshot saved: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return ""
            
    def capture_on_failure(self, test_name: str) -> str:
        """
        Capture screenshot for failed test.
        
        Args:
            test_name: Name of failed test
            
        Returns:
            Path to saved screenshot
        """
        return self.capture_screenshot(test_name, prefix="FAIL")
        
    def capture_element_screenshot(self, element, name: str) -> str:
        """
        Capture screenshot of specific element.
        
        Args:
            element: WebElement to capture
            name: Screenshot name
            
        Returns:
            Path to saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"element_{name}_{timestamp}.png"
        filepath = self.screenshots_dir / filename
        
        try:
            element.screenshot(str(filepath))
            logger.info(f"Element screenshot saved: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to capture element screenshot: {e}")
            return ""
            
    def capture_full_page_screenshot(self, name: str) -> str:
        """
        Capture full page screenshot (including scrollable area).
        
        Args:
            name: Screenshot name
            
        Returns:
            Path to saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"fullpage_{name}_{timestamp}.png"
        filepath = self.screenshots_dir / filename
        
        try:
            # Get page dimensions
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            total_width = self.driver.execute_script("return document.body.scrollWidth")
            
            # Scroll and capture screenshots
            screenshots = []
            for offset in range(0, total_height, viewport_height):
                self.driver.execute_script(f"window.scrollTo(0, {offset})")
                screenshot = self.driver.get_screenshot_as_png()
                screenshots.append(Image.open(io.BytesIO(screenshot)))
                
            # Stitch screenshots together
            full_screenshot = Image.new('RGB', (total_width, total_height))
            y_offset = 0
            for screenshot in screenshots:
                full_screenshot.paste(screenshot, (0, y_offset))
                y_offset += screenshot.height
                
            full_screenshot.save(filepath)
            logger.info(f"Full page screenshot saved: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to capture full page screenshot: {e}")
            return ""
            
    def compare_screenshots(self, baseline: str, current: str, 
                          threshold: float = 0.95) -> tuple[bool, float]:
        """
        Compare two screenshots for visual regression.
        
        Args:
            baseline: Path to baseline screenshot
            current: Path to current screenshot
            threshold: Similarity threshold (0-1)
            
        Returns:
            Tuple of (match, similarity_score)
        """
        try:
            # Load images
            img1 = cv2.imread(baseline)
            img2 = cv2.imread(current)
            
            # Ensure same dimensions
            if img1.shape != img2.shape:
                img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
                
            # Convert to grayscale
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            
            # Compute SSIM
            from skimage.metrics import structural_similarity as ssim
            similarity = ssim(gray1, gray2)
            
            match = similarity >= threshold
            logger.info(f"Screenshot comparison: {similarity:.2%} similarity")
            
            return match, similarity
        except Exception as e:
            logger.error(f"Screenshot comparison failed: {e}")
            return False, 0.0
            
    def annotate_screenshot(self, image_path: str, text: str, 
                          position: tuple = (10, 10)) -> str:
        """
        Add annotation text to screenshot.
        
        Args:
            image_path: Path to screenshot
            text: Annotation text
            position: Text position (x, y)
            
        Returns:
            Path to annotated screenshot
        """
        try:
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)
            
            # Use default font
            font = ImageFont.load_default()
            
            # Add text with background
            bbox = draw.textbbox(position, text, font=font)
            draw.rectangle(bbox, fill='yellow')
            draw.text(position, text, fill='black', font=font)
            
            # Save annotated image
            annotated_path = image_path.replace('.png', '_annotated.png')
            img.save(annotated_path)
            logger.info(f"Annotated screenshot saved: {annotated_path}")
            
            return annotated_path
        except Exception as e:
            logger.error(f"Failed to annotate screenshot: {e}")
            return image_path
            
    def cleanup_old_screenshots(self, days: int = 7) -> None:
        """
        Remove screenshots older than specified days.
        
        Args:
            days: Remove screenshots older than this many days
        """
        cutoff = datetime.now().timestamp() - (days * 86400)
        count = 0
        
        for file in self.screenshots_dir.glob("*.png"):
            if file.stat().st_mtime < cutoff:
                file.unlink()
                count += 1
                
        logger.info(f"Cleaned up {count} old screenshots")


# Fix missing import
import io
