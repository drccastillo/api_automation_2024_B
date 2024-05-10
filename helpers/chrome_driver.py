"""
Module to control the Chrome driver
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging

# Logger configuration
import logging
from utils.logger import get_logger
LOGGER = get_logger(__name__, logging.DEBUG)

# Chrome options
chrome_options = Options()

# Configure Selenium Grid remote server
grid_url = "http://localhost:4444/wd/hub"

# Class for Chrome driver controller
class ChromeDriver:
    """
    Class to control the Chrome driver
    """
    def __init__(self, configuration):
        """
        Initialize method for ChromeDriver
        :param configuration: Browser configuration
        """
        LOGGER.info("Creating Remote Chrome Driver with", configuration)
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"--window-size={configuration['browser']['resolution']}")
        self.driver = webdriver.Remote(
            command_executor=grid_url,
            options=chrome_options
        )
