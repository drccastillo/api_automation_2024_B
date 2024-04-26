"""
Module containing the Message class with message-related operations.
"""
from __future__ import annotations

import logging

from faker import Faker

from config.config import BASE_URL
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Message:
    """
    Class for Messages
    """

    def __init__(self, rest_client=None):
        """
        Setup class for Messages
        """
        self.fake = Faker()
        self.url_messages = f"{BASE_URL}/message/"
        if rest_client is None:
            self.rest_client = RestClient()
        else:
            self.rest_client = rest_client

    def generate_data(self):
        """
        Generate message body with fake data
        """
        phone_number = self.fake.phone_number()
        while len(phone_number) < 11 or len(phone_number) > 21:
            phone_number = self.fake.phone_number()

        body_message = {
            "name": self.fake.name(),
            "email": self.fake.email(),
            "phone": phone_number,
            "subject": self.fake.sentence(nb_words=6),
            "description": self.fake.text(max_nb_chars=200),
        }
        return body_message

    def all_messages(self):
        """
        Get all messages endpoint
        """
        url_get_messages = f"{self.url_messages}"
        response = self.rest_client.request(method_name="get", url=url_get_messages)
        return response

    def specific_message(self, message_id):
        """
        Get specific message endpoint
        """
        url_get_message = f"{self.url_messages}{message_id}"
        response = self.rest_client.request(method_name="get", url=url_get_message)
        return response

    def unread_messages(self):
        """
        Unread messages endpoint
        """
        url_get_unread_messages = f"{self.url_messages}count"
        response = self.rest_client.request(
            method_name="get",
            url=url_get_unread_messages,
        )
        return response

    def health_check_message(self):
        """
        Health check endpoint
        """
        url_health_check = f"{self.url_messages}actuator/health"
        response = self.rest_client.request(method_name="get", url=url_health_check)
        return response

    def create_message(self, body=None):
        """
        Create message endpoint
        """
        url_create_message = f"{self.url_messages}"
        body_message = body
        if body is None:
            body_message = self.generate_data()
        response = self.rest_client.request(
            method_name="post",
            url=url_create_message,
            body=body_message,
        )
        return response

    def mark_message_as_read(self, message_id):
        """
        Mark message as read endpoint
        """
        url_mark_message_as_read = f"{self.url_messages}{message_id}/read"
        response = self.rest_client.request(
            method_name="put",
            url=url_mark_message_as_read,
        )
        return response

    def delete_message(self, message_id):
        """
        Delete message endpoint
        """
        url_delete_message = f"{self.url_messages}{message_id}"
        response = self.rest_client.request(
            method_name="delete",
            url=url_delete_message,
        )
        return response
