from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from config.config import CREDENTIALS
from config.config import BASE_URL


from utils.logger import get_logger
import logging
LOGGER = get_logger(__name__, logging.DEBUG)

from helpers.driver_factory import DriverFactory
from helpers.action import Action

#   await DriverFactory.createInstance();
#   await DriverFactory.mybrowser.get("https://www.saucedemo.com/");
#   this.loginPage = await new LoginPage(DriverFactory.mybrowser);

class Login:
    usernameInput = (By.CSS_SELECTOR, '[data-test="username"]')
    passwordInput = (By.CSS_SELECTOR, '[data-test="password"]')
    loginButton = (By.CSS_SELECTOR, '#login-button')
    logoLabel = (By.CSS_SELECTOR, '.login_logo')

    def __init__(self, driver = None):
        if driver is None:
            self.driver_factory = DriverFactory()
        else:
            self.driver_factory = driver
        
        self.url_auth = f"{BASE_URL}/#/admin"
        self.action = Action(self.driver_factory.my_browser)

        if isinstance(self.driver_factory.my_browser, WebDriver):
            LOGGER.info("Waiting for Login Page elements")
            WebDriverWait(self.driver_factory.my_browser, 10).until(EC.presence_of_element_located(self.usernameInput))
            WebDriverWait(self.driver_factory.my_browser, 10).until(EC.presence_of_element_located(self.passwordInput))
            WebDriverWait(self.driver_factory.my_browser, 10).until(EC.presence_of_element_located(self.loginButton))
            WebDriverWait(self.driver_factory.my_browser, 10).until(EC.presence_of_element_located(self.logoLabel))
        else:
            raise TypeError("driver_factory.my_browser must be a WebDriver instance")
    
    async def setCredentials(self, objectCredentials):
        LOGGER.info("Setting Credentials")
        await self.action.clickOn(self.usernameInput)
        await self.action.setText(self.usernameInput, objectCredentials.username)
        await self.action.clickOn(self.passwordInput)
        await self.action.setText(self.passwordInput, objectCredentials.password)

    async def clickLoginButton(self):
        LOGGER.info("Trying to login user")
        await self.action.clickOn(self.loginButton)

    async def auth_user(self):
        LOGGER.info("Login")
        if self.driver_factory.my_browser is None:
            raise ValueError("my_browser is None")
        await self.driver_factory.my_browser.get(self.url_auth)
        await self.setCredentials(CREDENTIALS)
        await self.clickLoginButton()
        return self.driver_factory.my_browser
