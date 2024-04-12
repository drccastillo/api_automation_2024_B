import logging
import pytest

from helpers.validate_response import ValidateResponse
from helpers.rest_client import RestClient
from utils.logger import get_logger
from entities.auth import Auth


LOGGER = get_logger(__name__, logging.DEBUG)


class TestAuth:
    @classmethod
    def setup_class(cls):
        """
        Setup class for bookings
        """
        cls.rest_client = RestClient()
        cls.auth = Auth()
        cls.validate = ValidateResponse()
        cls.list_tokens = []


    @pytest.mark.acceptance
    def test_create_token(self, log_test_names):
        """
        Test create token
        """
        LOGGER.info("Test create token")
        response = self.auth.create_token()
        self.validate.validate_response(actual_response=response, endpoint="auth", file_name="create_token")
        self.list_tokens.append(response["cookies"]["token"])
        LOGGER.debug("Cookie token: %s", response["cookies"]["token"])


    @pytest.mark.acceptance
    def test_validate_token(self, create_token, log_test_names):
        """
        Test validate token
        """
        LOGGER.info("Test validate token")
        response = self.auth.validate_token(token=create_token)
        self.validate.validate_response(actual_response=response, endpoint="auth", file_name="validate_token")


    @pytest.mark.acceptance
    def test_destroy_token(self, create_token, log_test_names):
        """
        Test destroy token
        """
        LOGGER.info("Test destroy token")
        response = self.auth.destroy_token(token=create_token)
        self.validate.validate_response(actual_response=response, endpoint="auth", file_name="destroy_token")


    @classmethod
    def teardown_class(cls):
        """
        PyTest teardown class
        """
        LOGGER.info("Teardown class")
        LOGGER.info("Cleanup tokens data")
        for id_token in cls.list_tokens:
            response = cls.auth.destroy_token(token=id_token)
            if response["status_code"] == 200:
                LOGGER.debug("Token Id: %s deleted", id_token)
