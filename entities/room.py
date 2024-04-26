"""
Module containing the Room class which is used for room-related operations.
"""

from __future__ import annotations

import logging

from faker import Faker

from config.config import BASE_URL
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Room:
    """
    Class for Room
    """

    def __init__(self, rest_client=None):
        """
        Setup class for Room
        """
        self.fake = Faker()
        self.url_rooms = f"{BASE_URL}/room/"
        if rest_client is None:
            self.rest_client = RestClient()
        else:
            self.rest_client = rest_client

    def generate_data(self):
        """
        Generate room body with fake data
        """
        data = {
            "roomName": self.fake.name(),
            "type": self.fake.random_element(
                elements=("Single", "Double", "Twin", "Family", "Suite"),
            ),
            "accessible": self.fake.boolean(),
            "image": self.fake.image_url(),
            "description": self.fake.text(),
            "roomPrice": self.fake.random_int(min=1, max=999),
            "features": [
                self.fake.word() for _ in range(self.fake.random_int(min=1, max=5))
            ],
        }
        return data

    def all_rooms(self):
        """
        Get all rooms endpoint
        """
        url_get_rooms = f"{self.url_rooms}"
        response = self.rest_client.request(method_name="get", url=url_get_rooms)
        return response

    def specific_room(self, room_id):
        """
        Get specific room endpoint
        """
        url_get_room = f"{self.url_rooms}{room_id}"
        response = self.rest_client.request(method_name="get", url=url_get_room)
        return response

    def health_check_room(self):
        """
        Health check room endpoint
        """
        url_health_check_room = f"{self.url_rooms}actuator/health"
        response = self.rest_client.request(
            method_name="get",
            url=url_health_check_room,
        )
        return response

    def create_room(self, body=None):
        """
        Create room endpoint
        """
        url_create_room = f"{self.url_rooms}"
        body_room = body
        if body is None:
            body_room = self.generate_data()
        response = self.rest_client.request(
            method_name="post",
            url=url_create_room,
            body=body_room,
        )
        return response

    def update_room(self, room_id, body=None):
        """
        Update room endpoint
        """
        url_update_room = f"{self.url_rooms}{room_id}"
        body_room = body
        if body is None:
            body_room = self.generate_data()
        response = self.rest_client.request(
            method_name="put",
            url=url_update_room,
            body=body_room,
        )
        return response

    def delete_room(self, room_id):
        """
        Delete room endpoint
        """
        url_delete_room = f"{self.url_rooms}{room_id}"
        response = self.rest_client.request(method_name="delete", url=url_delete_room)
        return response
