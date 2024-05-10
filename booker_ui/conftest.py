"""
This module contains fixtures for the RESTful Booker API tests.
"""

import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import pytest
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@pytest.fixture(name="_log_test_names")
def _log_test_names_fixture(request):
    """
    Fixture to log the test names.
    :param request: pytest request object
    """
    LOGGER.info("Test '%s' STARTED", request.node.name)

    def fin():
        LOGGER.info("Test '%s' COMPLETED", request.node.name)

    request.addfinalizer(fin)


@pytest.fixture(name="browser")
def browser_fixture():
    """
    Fixture to get the browser
    :return: browser
    """
    chrome_options = Options()
    chrome_options.add_argument("--ignore-ssl-errors=yes")
    chrome_options.add_argument("--ignore-certificate-errors")
    driver = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub", options=chrome_options
    )
    yield driver
    driver.quit()
