from helpers.driver_factory import DriverFactory
import logging
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

class Action:
    """
    Class to perform actions on the browser
    """
    def __init__(self, driver=None):
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

    async def openUrl(self, url):
        """
        Open a URL
        :param url: URL to open
        """
        LOGGER.info("Opening URL: %s", url)
        if self.driver_factory.my_browser:
            await self.driver_factory.my_browser.get(url)
        else:
            LOGGER.error("Browser instance is None")

    async def getUrl(self):
        """
        Get the current URL
        """
        LOGGER.info("Getting URL")
        if self.driver_factory.my_browser:
            return await self.driver_factory.my_browser.current_url
        else:
            LOGGER.error("Browser instance is None")
            return None

    async def clickOn(self, locator):
        """
        Click on an element
        :param locator: Locator of the element
        """
        LOGGER.debug("Clicking on: %s", locator[1])
        if self.driver_factory.my_browser:
            element = await self.driver_factory.my_browser.find_element(*locator)
            await element.click()
        else:
            LOGGER.error("Browser instance is None")

    async def setText(self, locator, value):
        """
        Set text in an element
        :param locator: Locator of the element
        :param value: Value to set
        """
        if self.driver_factory.my_browser:
            element = await self.driver_factory.my_browser.find_element(*locator)
            await element.send_keys(value)
        else:
            LOGGER.error("Browser instance is None")