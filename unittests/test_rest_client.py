"""
Module to test the rest client helper
"""

from __future__ import annotations

import logging
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

import requests

from helpers.rest_client import RestClient
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


class TestRestClient(unittest.TestCase):
    """
    Test class for RestClient
    """

    @patch("requests.Session")
    def test_rest_client_initialization(self, mock_session):
        """
        Test the initialization of RestClient
        """
        LOGGER.info("Test RestClient initialization")
        mock_session.return_value.headers.update.return_value = None
        client = RestClient()
        assert client.timeout == 155
        assert isinstance(client.session, MagicMock)

    @patch("requests.Session")
    def test_request_successful_response(self, mock_session):
        """
        Test a successful response from request method
        """
        LOGGER.info("Test request successful response")
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_session.return_value.get.return_value = mock_response
        client = RestClient()
        response = client.request("get", "https://example.com")
        assert response["status_code"] == 200
        assert response["json"] == {"key": "value"}

    @patch("requests.Session")
    def test_request_http_error(self, mock_session):
        """
        Test an HTTP error from request method
        """
        LOGGER.info("Test request HTTP error")
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_response.status_code = 500
        mock_response.text = "HTTP Error"
        mock_session.return_value.get.return_value = mock_response
        client = RestClient()
        response = client.request("get", "https://example.com")
        assert response["status_code"] == 500
        assert "msg" in response["json"]

    @patch("requests.Session")
    def test_request_connection_error(self, mock_session):
        """
        Test a connection error from request method
        """
        LOGGER.info("Test request connection error")
        mock_session.return_value.get.side_effect = (
            requests.exceptions.ConnectionError()
        )
        client = RestClient()
        response = client.request("get", "https://example.com")
        assert "msg" in response["json"]

    @patch("requests.Session")
    def test_request_timeout_error(self, mock_session):
        """
        Test a timeout error from request method
        """
        LOGGER.info("Test request timeout error")
        mock_session.return_value.get.side_effect = requests.exceptions.Timeout()
        client = RestClient()
        response = client.request("get", "https://example.com")
        assert "msg" in response["json"]

    @patch("requests.Session")
    def test_request_general_request_exception(self, mock_session):
        """
        Test a general request exception from request method
        """
        LOGGER.info("Test request general request exception")
        mock_session.return_value.get.side_effect = (
            requests.exceptions.RequestException()
        )
        client = RestClient()
        response = client.request("get", "https://example.com")
        assert "msg" in response["json"]


if __name__ == "__main__":
    unittest.main()
