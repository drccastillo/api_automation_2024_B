"""
Module to test the Auth API endpoints
"""
from __future__ import annotations

import logging

import allure
import pytest

from entities.auth import Auth
from helpers.rest_client import RestClient
from helpers.validate_response import ValidateResponse
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


@allure.epic("Auth API")
@allure.story("Auth API Endpoints")
class TestAuths:
    """
    Class to test Auth API endpoints
    """

    @classmethod
    def setup_class(cls):
        """
        Setup class for bookings
        """
        cls.rest_client = RestClient()
        cls.auth = Auth()
        cls.validate = ValidateResponse()
        cls.list_tokens = []

    @allure.title("Create a token")
    @allure.tag("Auth", "Create")
    @pytest.mark.acceptance
    def test_create_token(self, _log_test_names):
        """
        Test create token
        """
        LOGGER.info("Test create token")
        response = self.auth.create_token()
        self.validate.validate_response(
            actual_response=response,
            endpoint="auth",
            file_name="create_token",
        )
        self.list_tokens.append(response["cookies"]["token"])
        LOGGER.debug("Cookie token: %s", response["cookies"]["token"])

    @allure.title("Validate a token")
    @allure.tag("Auth", "Validate")
    @pytest.mark.acceptance
    def test_validate_token(self, create_token, _log_test_names):
        """
        Test validate token
        :param create_token: fixture to create a token
        """
        LOGGER.info("Test validate token")
        response = self.auth.validate_token(token=create_token)
        self.validate.validate_response(
            actual_response=response,
            endpoint="auth",
            file_name="validate_token",
        )

    @allure.title("Destroy a token")
    @allure.tag("Auth", "Delete")
    @pytest.mark.acceptance
    def test_destroy_token(self, create_token, _log_test_names):
        """
        Test destroy token
        :param create_token: fixture to create a token
        """
        LOGGER.info("Test destroy token")
        response = self.auth.destroy_token(token=create_token)
        self.validate.validate_response(
            actual_response=response,
            endpoint="auth",
            file_name="destroy_token",
        )

    @allure.title("Check health of the auth service")
    @allure.tag("Auth", "Health")
    @pytest.mark.smoke
    def test_health_check_auth(self, _log_test_names):
        """
        Test get health check endpoint
        """
        LOGGER.info("Test get health check")
        response = self.auth.health_check_auth()
        self.validate.validate_response(
            actual_response=response,
            endpoint="auth",
            file_name="get_health_check",
        )

    @classmethod
    def teardown_class(cls):
        """
        PyTest teardown class
        """
        LOGGER.info("Teardown class")
        LOGGER.info("Cleanup tokens data")
        for token_id in cls.list_tokens:
            response = cls.auth.destroy_token(token=token_id)
            if response["status_code"] == 200:
                LOGGER.debug("Token Id: %s deleted", token_id)
