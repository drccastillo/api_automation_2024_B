import pytest
import requests
from unittest.mock import patch, MagicMock
from helpers.rest_client import RestClient


@patch("requests.Session")
def test_successful_response(mock_session):
    mock_session.return_value.get.return_value.status_code = 200
    client = RestClient()
    response = client.request("get", "https://example.com")
    assert response["status_code"] == 200


@patch("requests.Session")
def test_http_error(mock_session):
    mock_session.return_value.get.side_effect = requests.exceptions.HTTPError()
    client = RestClient()
    response = client.request("get", "https://example.com")
    assert "error" in response["json"]


@patch("requests.Session")
def test_connection_error(mock_session):
    mock_session.return_value.get.side_effect = requests.exceptions.ConnectionError()
    client = RestClient()
    response = client.request("get", "https://example.com")
    assert "error" in response["json"]


@patch("requests.Session")
def test_timeout_error(mock_session):
    mock_session.return_value.get.side_effect = requests.exceptions.Timeout()
    client = RestClient()
    response = client.request("get", "https://example.com")
    assert "error" in response["json"]


@patch("requests.Session")
def test_general_request_exception(mock_session):
    mock_session.return_value.get.side_effect = requests.exceptions.RequestException()
    client = RestClient()
    response = client.request("get", "https://example.com")
    assert "error" in response["json"]


@patch("requests.Session")
def test_get_json_with_text(mock_session):
    mock_response = MagicMock()
    mock_response.text = '{"key": "value"}'
    client = RestClient()
    json = client.get_json(mock_response)
    assert json == {"key": "value"}


@patch("requests.Session")
def test_get_json_without_text(mock_session):
    mock_response = MagicMock()
    mock_response.text = None
    client = RestClient()
    json = client.get_json(mock_response)
    assert json == {"msg": "No body content"}


@patch("requests.Session")
def test_get_header_with_headers(mock_session):
    mock_response = MagicMock()
    mock_response.headers = {"Content-Type": "application/json"}
    client = RestClient()
    headers = client.get_header(mock_response)
    assert headers == {"Content-Type": "application/json"}


@patch("requests.Session")
def test_get_header_without_headers(mock_session):
    mock_response = MagicMock()
    mock_response.headers = None
    client = RestClient()
    headers = client.get_header(mock_response)
    assert headers == {"msg": "No headers content"}


@patch("requests.Session")
def test_get_cookies_with_cookies(mock_session):
    mock_response = MagicMock()
    mock_response.cookies = requests.cookies.RequestsCookieJar()
    client = RestClient()
    cookies = client.get_cookies(mock_response)
    assert cookies == {}


@patch("requests.Session")
def test_get_cookies_without_cookies(mock_session):
    mock_response = MagicMock()
    mock_response.cookies = None
    client = RestClient()
    cookies = client.get_cookies(mock_response)
    assert cookies == {"msg": "No cookies content"}
