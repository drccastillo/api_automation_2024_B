import logging
from config.config import BASE_URL
from config.config import CREDENTIALS
from utils.logger import get_logger
from helpers.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


class Auth:
    """
    Class for Auth
    """

    def __init__(self, rest_client=None):
        """
        Setup class for Auth
        """
        self.url_auth = f"{BASE_URL}/auth/"
        if rest_client is None:
            self.rest_client = RestClient()
        else:
            self.rest_client = rest_client

    def extract_token(self, response):
        """
        Extract token from response
        """
        return response["cookies"]["token"]

    def create_token(self):
        """
        Create token
        """
        url_auth_login = f"{self.url_auth}login"
        response = self.rest_client.request(
            method_name="post", url=url_auth_login, body=CREDENTIALS
        )
        return response

    def validate_token(self, token):
        """
        Validate token
        """
        url_auth_validate = f"{self.url_auth}validate"
        body_token = {"token": token}
        response = self.rest_client.request(
            method_name="post", url=url_auth_validate, body=body_token
        )
        return response

    def destroy_token(self, token):
        """
        Destroy token
        """
        url_auth_logout = f"{self.url_auth}logout"
        body_token = {"token": token}
        response = self.rest_client.request(
            method_name="post", url=url_auth_logout, body=body_token
        )
        return response