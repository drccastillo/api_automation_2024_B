"""
Module containing the Branding class for branding operations.
"""
from __future__ import annotations

import logging
import random
import re
import string

from faker import Faker

from config.config import BASE_URL
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Branding:
    """
    Class for Branding
    """

    def __init__(self, rest_client=None):
        """
        Setup class for Branding
        """
        self.fake = Faker()
        self.url_branding = f'{BASE_URL}/branding/'
        if rest_client is None:
            self.rest_client = RestClient()
        else:
            self.rest_client = rest_client

    def generate_phone_number(self):
        """
        Generate a phone number of correct length
        """
        while True:
            phone_number = ''.join(
                random.choice(string.digits) for _ in range(random.randint(11, 15))
            )
            if 11 <= len(phone_number) <= 15:
                return phone_number

    def generate_string(self, pattern, min_length, max_length):
        """
        Generate a string of correct length and pattern
        """
        while True:
            generated_string = self.fake.text(max_nb_chars=max_length)
            regex_pattern = r'[^&.\w\s]' if '.' in pattern else r'[^&\w\s]'
            generated_string = re.sub(regex_pattern, ' ', generated_string)
            generated_string = re.sub(r'\s+', ' ', generated_string).strip()
            if min_length <= len(generated_string) <= max_length and re.match(
                pattern,
                generated_string,
            ):
                return generated_string

    def generate_data(self):
        """
        Generate branding body with fake data
        """
        body_branding = {
            'name': self.generate_string('[A-Za-z& ]*', 3, 100),
            'map': {
                'latitude': float(self.fake.latitude()),
                'longitude': float(self.fake.longitude()),
            },
            'logoUrl': self.fake.image_url(),
            'description': self.generate_string('[a-zA-Z,&. ]*', 3, 500),
            'contact': {
                'name': self.generate_string('[A-Za-z& ]*', 3, 40),
                'address': self.fake.address(),
                'phone': self.generate_phone_number(),
                'email': self.fake.email(),
            },
        }
        LOGGER.info('New Branding %s', body_branding)
        return body_branding

    def all_brandings(self):
        """
        Get all branding endpoint
        """
        url_get_branding = f'{self.url_branding}'
        response = self.rest_client.request(method_name='get', url=url_get_branding)
        return response

    def health_check_branding(self):
        """
        Health check branding endpoint
        """
        url_health_check_branding = f'{self.url_branding}actuator/health'
        response = self.rest_client.request(
            method_name='get',
            url=url_health_check_branding,
        )
        return response

    def update_branding(self, body=None):
        """
        Update branding endpoint
        """
        url_update_branding = f'{self.url_branding}'
        body_branding = body
        if body is None:
            body_branding = self.generate_data()
        response = self.rest_client.request(
            method_name='put',
            url=url_update_branding,
            body=body_branding,
        )
        return response
