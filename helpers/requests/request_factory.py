"""
Module for RequestFactory class
"""
from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from helpers.rest_client import RestClient


class RequestFactory(ABC):
    """
    RequestFactory class for handling requests
    """

    def __init__(self, rest_client=None):
        """
        Setup class for Room
        """
        if rest_client is None:
            self.rest_client = RestClient()
        else:
            self.rest_client = rest_client

    @abstractmethod
    def execute(self):
        """
        Execute the request
        """

    def __str__(self):
        """
        Return a string representation of the RequestFactory instance.
        """
        return f'RequestFactory(rest_client={self.rest_client})'
