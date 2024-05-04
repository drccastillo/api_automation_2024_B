"""
Module for the Base class which is used for handling requests.
"""
from __future__ import annotations

import logging
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

class Base:
    def __init__(self, rest_client, url_base):
        """
        Setup class for Base
        :param rest_client: RestClient instance
        :param url_base: Base URL
        """
        self.rest_client = rest_client
        self.url_base = url_base

    def handle_request(self, http_method, url_path='', request_body=None, resource_id=None):
        """
        Handle request endpoint
        :param http_method: HTTP method name
        :param url_path: URL path
        :param request_body: Request body
        :param resource_id: Resource ID
        """
        url = self._build_url(url_path, resource_id)
        response = self.rest_client.request(
            method_name=http_method,
            url=url,
            body=request_body,
        )
        return response
    
    def _build_url(self, url_path='', resource_id=None):
        """
        Build the URL for the request
        :param url_path: URL path
        :param resource_id: Resource ID
        """
        url = f'{self.url_base}{url_path}'
        if resource_id:
            if url.endswith('/'):
                url = f'{url}{resource_id}'
            else:
                url += f'/{resource_id}'
        return url