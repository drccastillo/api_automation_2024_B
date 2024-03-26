import logging

import pytest
import requests

from config.config import url_booker
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@pytest.fixture()
def create_booking():
    booking_id = None
    rest_client = RestClient()
    LOGGER.info("Fixture create booking")
    body_booking = {
        "firstname" : "Jim from Fixture",
        "lastname" : "Brown from Fixture",
        "totalprice" : 111,
        "depositpaid" : "true",
        "bookingdates" : {
            "checkin" : "2023-01-01",
            "checkout" : "2024-01-01"
        },
        "additionalneeds" : "Breakfast from Fixture"
    }
    url_booker_bookings = f"{url_booker}/booking"
    response = rest_client.request("post", url_booker_bookings, body=body_booking)
    if response.status_code == 200:
        booking_id = response.json()["bookingid"]

    yield booking_id
    LOGGER.debug("Yield fixture delete booking")
    delete_booking(booking_id, rest_client)

def delete_booking(booking_id, rest_client):

    LOGGER.debug("Cleanup booking")
    url_delete_booking = f"{url_booker}/booking/{booking_id}"
    response = rest_client.request("delete", url_delete_booking)
    if response.status_code == 201:
        LOGGER.info("booking Id deleted : %s", booking_id)


@pytest.fixture()
def log_test_names(request):
    LOGGER.info("Test '%s' STARTED", request.node.name)

    def fin():
        LOGGER.info("Test '%s' COMPLETED", request.node.name)

    request.addfinalizer(fin)