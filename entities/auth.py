"""
This module contains the Auth class which provides methods for handling authentication.
"""
from __future__ import annotations

import logging

from dotenv import dotenv_values

from config.config import abs_path
from config.config import BASE_URL
from config.config import CREDENTIALS
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)
TOKEN = None

class Auth:
    """
    This class provides methods for handling authentication.
    """

    def __init__(self, rest_client=None):
        """
        Setup class for Auth
        param rest_client: The rest client to use. If None, a new rest client is created.
        """
        self.url_auth = f'{BASE_URL}/auth/'
        if rest_client is None:
            self.rest_client = RestClient()
        else:
            self.rest_client = rest_client

    def extract_token(self, response):
        """
        Extract token from response
        param response: The response from the request
        """
        return response['cookies']['token']

    def create_token(self):
        """
        Create token
        """
        url_auth_login = f'{self.url_auth}login'
        response = self.rest_client.request(
            method_name='post',
            url=url_auth_login,
            body=CREDENTIALS,
        )
        env_vars = dotenv_values(f'{abs_path}/.env')
        env_vars['RESTFUL_BOOKER_TOKEN'] = response['cookies']['token']
        with open(f'{abs_path}/.env', 'w', encoding='utf-8') as f:
            for key, value in env_vars.items():
                f.write(f'{key}={value}\n')
        return response

    def validate_token(self, token):
        """
        Validate token
        param token: The token to validate
        """
        url_auth_validate = f'{self.url_auth}validate'
        body_token = {'token': token}
        response = self.rest_client.request(
            method_name='post',
            url=url_auth_validate,
            body=body_token,
        )
        return response

    def destroy_token(self, token):
        """
        Destroy token
        param token: The token to destroy
        """
        url_auth_logout = f'{self.url_auth}logout'
        body_token = {'token': token}
        response = self.rest_client.request(
            method_name='post',
            url=url_auth_logout,
            body=body_token,
        )
        return response

    def health_check_auth(self):
        """
        Health check auth
        """
        url_health_check_auth = f'{self.url_auth}actuator/health'
        response = self.rest_client.request(
            method_name='get',
            url=url_health_check_auth,
        )
        return response
