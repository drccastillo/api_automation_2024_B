"""
Module contains the Report class for handling report-related operations.
"""
from __future__ import annotations

import logging

from config.config import BASE_URL
from helpers.rest_client import RestClient
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


class Report:
    """
    Class for Reports
    """

    def __init__(self, rest_client=None):
        """
        Setup class for Reports
        """
        self.url_reports = f"{BASE_URL}/report/"
        if rest_client is None:
            self.rest_client = RestClient()
        else:
            self.rest_client = rest_client

    def all_reports(self):
        """
        Get all reports endpoint
        """
        url_get_reports = f"{self.url_reports}"
        response = self.rest_client.request(method_name="get", url=url_get_reports)
        return response

    def specific_report(self, room_id):
        """ "
        Get specific report endpoint
        """
        url_get_report = f"{self.url_reports}room/{room_id}"
        response = self.rest_client.request(method_name="get", url=url_get_report)
        return response

    def health_check_report(self):
        """
        Health check report endpoint
        """
        url_health_check_report = f"{self.url_reports}actuator/health"
        response = self.rest_client.request(
            method_name="get",
            url=url_health_check_report,
        )
        return response
