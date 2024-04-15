import logging
import pytest
import allure

from helpers.validate_response import ValidateResponse
from helpers.rest_client import RestClient
from utils.logger import get_logger
from entities.report import Report

LOGGER = get_logger(__name__, logging.DEBUG)

@allure.epic("Report API")
@allure.story("Report API Endpoints")
class TestReports:
    @classmethod 
    def setup_class(cls):
        """
        Setup class for Reports
        """
        LOGGER.info("Setup Class for Reports")
        cls.rest_client = RestClient()
        cls.validate = ValidateResponse()
        cls.report = Report()

    
    @allure.title("Get all reports")
    @allure.tag("Report", "Get")
    @pytest.mark.acceptance
    def test_get_all_reports(self, log_test_names):
        """
        Test get all reports endpoint
        """
        LOGGER.info("Test get all reports")
        response = self.report.all_reports()
        self.validate.validate_response(actual_response=response, endpoint="report", file_name="get_all_reports")


    @allure.title("Get a specific room report")
    @allure.tag("Report", "Get")
    @pytest.mark.acceptance
    def test_get_specific_room_report(self, create_booking, log_test_names):
        """
        Test get specific room report endpoint
        """
        LOGGER.info("Test get specific room report")
        response = self.report.specific_report(room_id=create_booking["room_id"])
        self.validate.validate_response(actual_response=response, endpoint="report", file_name="get_specific_room_report")


    @allure.title("Check health of report service")
    @allure.tag("Report", "Get")
    @pytest.mark.acceptance
    def test_get_health_check(self, log_test_names):
        """
        Test get health check endpoint
        """
        LOGGER.info("Test get health check")
        response = self.report.health_check_report()
        self.validate.validate_response(actual_response=response, endpoint="report", file_name="get_health_check")
