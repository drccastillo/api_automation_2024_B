"""
Module for GetRequestFactory class
"""
from __future__ import annotations

from request_factory import RequestFactory


class GetRequestFactory(RequestFactory):
    """
    GetRequestFactory class for handling GET requests
    """

    def create_request(self, url):
        """
        Create the request
        :param url: URL for the request
        :return: The response from the request
        """
        response = self.rest_client.request(method_name='get', url=url)
        return response
