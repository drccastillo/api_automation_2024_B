from abc import ABC, abstractmethod
from helpers.rest_client import RestClient

class RequestFactory(ABC):

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
        pass
