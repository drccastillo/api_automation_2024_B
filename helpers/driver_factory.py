import logging
from threading import Lock
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException, StaleElementReferenceException, ElementNotInteractableException, InvalidSessionIdException
from utils.logger import get_logger

from chrome_driver import ChromeDriver
from firefox_driver import FirefoxDriver
from config.config import CONFIGURATION

LOGGER = get_logger(__name__, logging.DEBUG)

browser_strategies = {
    'chrome': ChromeDriver,
    'firefox': FirefoxDriver,
}

class SingletonMeta(type):
    """
    Singleton metaclass to create a single instance of a class
    """
    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Call method to create a single instance of a class
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class DriverFactory(metaclass=SingletonMeta):
    """
    Factory class to create browser driver instances
    """

    def __init__(self):
        """
        Initialize method for DriverFactory
        """
        self.my_browser = None

    async def create_instance(self):
        """
        Create a browser driver instance
        """
        if not self.my_browser:
            LOGGER.info("Starting new browser")
            browser_name = CONFIGURATION.get('browser', {}).get('name', '').lower()
            if browser_name in browser_strategies:
                try:
                    self.my_browser = await browser_strategies[browser_name](CONFIGURATION)
                    LOGGER.debug("Browser session info:", await self.my_browser.getSession())
                    return self.my_browser
                except (NoSuchElementException, TimeoutException, StaleElementReferenceException, ElementNotInteractableException, InvalidSessionIdException, WebDriverException) as e:
                    LOGGER.error(f"An error occurred while creating the browser instance: {e}")
                except Exception as e:
                    LOGGER.error(f"An unexpected error occurred: {e}")
            else:
                LOGGER.error("Invalid browser name")
        else:
            LOGGER.info("Browser already exists")
            return self.my_browser

    async def close_instance(self):
        """
        Close the browser driver instance
        """
        if self.my_browser:
            LOGGER.info("Closing Browser")
            try:
                await self.my_browser.quit()
            except (InvalidSessionIdException, WebDriverException) as e:
                LOGGER.error(f"An error occurred while closing the browser instance: {e}")
            except Exception as e:
                LOGGER.error(f"An unexpected error occurred: {e}")
            finally:
                self.my_browser = None
                LOGGER.info("Browser closed")
