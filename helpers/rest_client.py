"""
Module to send HTTP requests to the server
"""
from __future__ import annotations

import json
import logging

import requests.utils
from requests.adapters import HTTPAdapter

from config.config import DEFAULT_HEADERS
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class RestClient:
    """
    Class to send HTTP requests to the server
    """

    def __init__(self, headers=None, timeout=3, max_retries=5):
        """
        Setup class for RestClient
        :param headers: Headers for the request
        :param timeout: Timeout for the request
        :param max_retries: Maximum number of retries
        """
        self.session = requests.Session()
        self.session.headers.update(headers if headers is not None else DEFAULT_HEADERS)
        self.timeout = timeout
        self.adapter = HTTPAdapter(max_retries=max_retries)

    def request(self, method_name, url, body=None):
        """
        Send a request to the server
        :param method_name: HTTP method name
        :param url: URL to send the request
        :param body: Request body
        :return: Response dictionary
        Returns a dictionary with the following keys
        - json: Response body
        - status_code: Response status code
        - headers: Response headers
        """
        response = None  # Initialize response
        response_dict = {}
        try:
            self.session.mount(url, self.adapter)

            method_func = getattr(self.session, method_name)
            response = method_func(url=url, json=body, timeout=self.timeout)
            response_dict.update({'json': self.get_json(response)})
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            LOGGER.error('HTTP error occurred: %s', http_err)
            if response is not None:
                if response.text:
                    try:
                        response_dict['json'] = response.json()
                    except json.JSONDecodeError:
                        response_dict['json'] = {'msg': 'No body content'}
                else:
                    response_dict['json'] = {'msg': str(http_err)}
            else:
                response_dict['json'] = {'msg': str(http_err)}
        except requests.exceptions.ConnectionError as conn_err:
            LOGGER.error('Error connecting: %s', conn_err)
            response_dict['json'] = {'msg': str(conn_err)}
        except requests.exceptions.Timeout as timeout_err:
            LOGGER.error('Timeout error: %s', timeout_err)
            response_dict['json'] = {'msg': str(timeout_err)}
        except requests.exceptions.RequestException as err:
            LOGGER.error('Error: %s', err)
            response_dict['json'] = {'msg': str(err)}
        finally:
            if response is not None:
                response_dict.update(
                    {
                        'status_code': response.status_code,
                        'headers': self.get_header(response),
                        'cookies': self.get_cookies(response),
                    },
                )
            else:
                response_dict.update(
                    {
                        'status_code': 'Unknown',
                        'headers': {'msg': 'No response headers'},
                        'json': {'msg': 'No response body content'},
                        'cookies': {'msg': 'No response cookies'},
                    },
                )
            LOGGER.debug('Status Code: %s', response_dict['status_code'])
            LOGGER.debug('Response headers: %s', response_dict['headers'])
            LOGGER.debug('Response Content: %s', response_dict['json'])
            LOGGER.debug('Response Cookies: %s', response_dict['cookies'])

        return response_dict

    @staticmethod
    def get_json(response):
        """
        Get JSON content from the response
        :param response: Response from the server
        :return: JSON content
        """
        if response.text:
            try:
                return response.json()
            except json.JSONDecodeError:
                return {'msg': response.text}
        else:
            return {'msg': 'No body content'}

    @staticmethod
    def get_header(response):
        """
        Get headers from the response
        :param response: Response from the server
        :return: Headers
        """
        try:
            return response.headers
        except AttributeError:
            return {'msg': 'No headers content'}

    @staticmethod
    def get_cookies(response):
        """
        Get cookies from the response
        :param response: Response from the server
        :return: Cookies
        """
        try:
            return requests.utils.dict_from_cookiejar(response.cookies)
        except AttributeError:
            return {'msg': 'No cookies content'}
