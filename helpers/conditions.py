from selenium.webdriver.support import expected_conditions as EC
import logging
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

from helpers.driver_factory import DriverFactory

LOGGER = get_logger(__name__)

class Conditions:
    """
    Class to perform conditions on the browser
    """

    def __init__(self, driver = None):
        if driver is None:
            self.driver_factory = DriverFactory()
        else:
            self.driver_factory = driver


    async def initialize(self):
        if not self.driver_factory.my_browser:
            LOGGER.debug("Browser instance is not initialized. Creating a new instance.")
            await self.driver_factory.create_instance()
        else:
            LOGGER.debug("Browser instance already exists.")

    async def is_located(self, locator):
        """
        Check if element is located in the DOM
        :param locator: Locator of the element
        """
        LOGGER.debug("Checking element is present in DOM: %s", locator.value)
        if self.driver_factory.my_browser:
            await self.driver_factory.my_browser.wait(EC.presence_of_element_located(locator))
        else:
            LOGGER.error("Browser instance is None")

    async def wait_until_visible(self, locator):
        """
        Wait until element is visible
        :param locator: Locator of the element
        """
        LOGGER.debug("Waiting element to be visible: %s", locator.value)
        if self.driver_factory.my_browser:
            await self.driver_factory.my_browser.wait(EC.visibility_of_element_located(locator))
        else:
            LOGGER.error("Browser instance is None")