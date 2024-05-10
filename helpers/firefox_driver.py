from config.config import GRID_URL
import logging
from utils.logger import get_logger
from selenium.webdriver import FirefoxOptions, Remote

LOGGER = get_logger(__name__, logging.DEBUG)

class FirefoxDriver:
    """
    Class for the Firefox driver controller
    """
    def __init__(self, configuration):
        """
        Initialization method for FirefoxDriver
        :param configuration: Browser configuration
        """
        firefox_options = FirefoxOptions()

        LOGGER.info("Creating Remote Firefox Driver with configuration: %s", configuration)

        resolution = configuration.get('browser', {}).get('resolution')
        if resolution:
            firefox_options.add_argument(f"--window-size={resolution}")
        else:
            LOGGER.warning("Browser resolution not provided in configuration. Using default resolution.")

        try:
            self.driver = Remote(
                command_executor= f"{GRID_URL}",
                options=firefox_options
            )
        except Exception as e:
            LOGGER.error("An error occurred while creating the Remote Firefox Driver: %s", e)
            raise
