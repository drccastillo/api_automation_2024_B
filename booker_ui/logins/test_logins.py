"""
Test cases for login UI pages
"""

from __future__ import annotations

import logging

import allure
import pytest

from pages.login import Login
from helpers.driver_factory import DriverFactory
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


@allure.epic("Login UI")
@allure.story("Login UI Pages")
class TestLogins:
    """
    Class to test login UI pages
    """
    @classmethod
    def setup_class(cls):
        """
        Setup class for login UI pages
        """
        cls.driver_factory = DriverFactory()
        cls.login = Login()
        #cls.validate = ValidateResponse()
        #cls.list_tokens = []

    @allure.title("Login as admin user")
    @allure.tag("Login")
    @pytest.mark.acceptance
    def test_login(self, _log_test_names):
        """
        Test
        """
        LOGGER.info("Test login")
        response = self.login.auth_user()
        # self.validate.validate_response(
        #     actual_response=response,
        #     endpoint="auth",
        #     file_name="create_token",
        # )
        # self.list_tokens.append(response["cookies"]["token"])
        # LOGGER.debug("Cookie token: %s", response["cookies"]["token"])

    @classmethod
    def teardown_class(cls):
        """
        PyTest teardown class
        """
        # LOGGER.info("Teardown class")
        # LOGGER.info("Cleanup tokens data")
        # for token_id in cls.list_tokens:
        #     response = cls.auth.destroy_token(token=token_id)
        #     if response["status_code"] == 200:
        #         LOGGER.debug("Token Id: %s deleted", token_id)
