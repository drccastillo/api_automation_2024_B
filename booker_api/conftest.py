"""
This module contains fixtures for the RESTful Booker API tests.
"""

from __future__ import annotations

import logging
import os
import random

import pytest

from entities.auth import Auth
from entities.booking import Booking
from entities.message import Message
from entities.room import Room
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


@pytest.fixture(name="_log_test_names")
def _log_test_names_fixture(request):
    """
    Fixture to log the test names.
    :param request: pytest request object
    """
    LOGGER.info("Test '%s' STARTED", request.node.name)

    def fin():
        LOGGER.info("Test '%s' COMPLETED", request.node.name)

    request.addfinalizer(fin)


@pytest.fixture(name="create_token")
def create_token_fixture():
    """
    Fixture to retrieve the authentication token.
    :return: token ID
    """
    LOGGER.info("Fixture create token")
    auth = Auth()
    token = None
    response = auth.create_token()
    if response["status_code"] == 200:
        token = response["cookies"]["token"]
    else:
        LOGGER.error("Failed to create token: %s", response["json"])
    yield token
    LOGGER.debug("token_id = %s", token)
    # Cleanup: Attempt to delete the booking if it exists
    if token is not None:
        destroy_token(token, auth)
    else:
        LOGGER.warning("No token created, nothing to delete.")


def validate_token(token, auth):
    """
    self.session.headers.update(headers)
    :param token: token
    :param auth: auth object
    """
    response = auth.validate_token(token=token)
    if response["status_code"] != 200:
        token_id = str(create_token_fixture)
        auth.rest_client.headers["cookie"] = f"token={token_id}"
        os.environ["TOKEN"] = token_id

    LOGGER.debug("The cookie is: %s", auth.rest_client.headers["cookie"])


@pytest.fixture(name="create_room")
def create_room_fixture():
    """
    Fixture to create a room.
    :return: room ID
    """
    LOGGER.info("Fixture create room")
    room_id = None
    room = Room()
    response = room.create_room()
    if response["status_code"] == 201:
        room_id = response["json"]["roomid"]
    yield room_id
    # Cleanup: Attempt to delete the room if it exists
    if room_id is not None:
        delete_room(room_id, room)
    else:
        LOGGER.warning("No room created, nothing to delete.")


@pytest.fixture(name="create_message")
def create_message_fixture():
    """
    Fixture to create a message.
    :return: message ID
    """
    LOGGER.info("Fixture create message")
    message_id = None
    message = Message()
    response = message.create_message()
    if response["status_code"] == 201:
        message_id = response["json"]["messageid"]
    yield message_id
    if message_id is not None:
        delete_message(message_id, message)
    else:
        LOGGER.warning("No message created, nothing to delete.")


@pytest.fixture(name="create_booking")
def create_booking_fixture(create_room):
    """
    Fixture to create a booking.
    :param create_room: fixture to create a room
    :return: booking ID and room ID in a dictionary
    """
    LOGGER.info("Fixture create booking")
    booking = Booking()
    booking_room_id = {}
    booking_room_id["room_id"] = f"{create_room}"
    response = booking.create_booking(room_id=booking_room_id["room_id"])
    if response["status_code"] == 201:
        booking_room_id["booking_id"] = response["json"]["bookingid"]
    yield booking_room_id
    # Cleanup: Attempt to delete the booking if it exists
    if booking_room_id["booking_id"] is not None:
        delete_booking(booking_room_id["booking_id"], booking)
    else:
        LOGGER.warning("No booking created, nothing to delete.")


@pytest.fixture(name="scenario_booking")
def scenario_booking_fixture(scenario, create_booking):
    """
    Fixture to retrieve the booking ID.
    :param scenario: scenario
    :param create_booking: fixture to create a booking
    return: booking ID
    """
    if scenario == "exist":
        return create_booking["booking_id"]

    return random.randint(1000, 9999)


def destroy_token(token, auth):
    """
    Function to delete a token.
    :param token: token
    :param auth: auth object
    """
    LOGGER.info("Function to delete a token")
    auth.destroy_token(token=token)


def delete_booking(booking_id, booking):
    """
    Function to delete a booking.
    :param booking_id: booking ID
    :param booking: booking object
    """
    LOGGER.info("Function to delete a booking")
    booking.delete_booking(booking_id)


def delete_room(room_id, room):
    """
    Function to delete a room.
    :param room_id: room ID
    :param room: room object
    """
    LOGGER.info("Function to delete a room")
    room.delete_room(room_id)


def delete_message(message_id, message):
    """
    Function to delete a message.
    :param message_id: message ID
    :param message: message object
    """
    LOGGER.info("Function to delete a message")
    message.delete_message(message_id)
