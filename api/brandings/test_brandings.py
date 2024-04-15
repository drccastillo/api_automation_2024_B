import logging
import pytest
import allure

from helpers.validate_response import ValidateResponse
from helpers.rest_client import RestClient
from utils.logger import get_logger
from entities.branding import Branding


LOGGER = get_logger(__name__, logging.DEBUG)


@allure.epic("Branding API")
@allure.story("Branding API Endpoints")
class TestBrandings:
    @classmethod
    def setup_class(cls):
        """
        Setup class for Brandings
        """
        LOGGER.info ("Setup Class for Brandings")
        cls.rest_client = RestClient()
        cls.branding = Branding()
        cls.validate = ValidateResponse()

    @allure.title("Get all brandings")
    @allure.tag("Branding", "Get")
    @pytest.mark.acceptance
    def test_get_all_brandings(self, log_test_names):
        """
        Test get all brandings endpoint
        """
        LOGGER.info("Test get all brandings")
        response = self.branding.all_branding()
        self.validate.validate_response(actual_response=response, endpoint="branding", file_name="get_all_brandings")


    @allure.title("Check health of branding service")
    @allure.tag("Branding", "Get")
    @pytest.mark.smoke
    def test_get_health_check(self, log_test_names):    
        """
        Test get health check endpoint
        """
        LOGGER.info("Test get health check")
        response = self.branding.health_check_branding()
        self.validate.validate_response(actual_response=response, endpoint="branding", file_name="get_health_check")


    @allure.title("Update branding")
    @allure.tag("Branding", "Update")
    @pytest.mark.acceptance
    def test_update_branding(self, log_test_names):
        """
        Test update branding
        """
        LOGGER.info("Test update branding")
        body_branding = self.branding.generate_data()
        response = self.branding.update_branding(body=body_branding)
        self.validate.validate_response(actual_response=response, endpoint="branding", file_name="update_branding")
