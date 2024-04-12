import logging
from faker import Faker
from httpx import delete
from config.config import BASE_URL
from utils.logger import get_logger
from helpers.rest_client import RestClient
from datetime import timedelta

LOGGER = get_logger(__name__, logging.DEBUG)


class Booking:
    def __init__(self, rest_client=None):
        """
        Setup class for Booking
        """
        self.fake = Faker()
        self.url_bookings = f"{BASE_URL}/booking/"
        if rest_client is None:
            self.rest_client = RestClient()
        else:
            self.rest_client = rest_client

    def generate_data(self, room_id):
        """
        Generate booking body with fake data
        """
        checkin_date = self.fake.date_between(start_date="-20y", end_date="-1m")
        checkout_date = self.fake.date_between_dates(
            date_start=checkin_date + timedelta(days=1),
            date_end=checkin_date + timedelta(days=self.fake.random_int(min=2, max=10)),
        )

        data = {
            "firstname": self.fake.first_name(),
            "lastname": self.fake.last_name(),
            "totalprice": self.fake.random_int(min=1, max=999),
            "depositpaid": self.fake.boolean(),
            "bookingdates": {
                "checkin": checkin_date.strftime("%Y-%m-%d"),
                "checkout": checkout_date.strftime("%Y-%m-%d"),
            },
            "additionalneeds": self.fake.sentence(),
            "roomid": room_id,
        }
        LOGGER.info("new booking %s", data)
        return data

    def all_bookings(self):
        """
        Get all bookings endpoint
        """
        url_get_bookings = f"{self.url_bookings}"
        response = self.rest_client.request(method_name="get", url=url_get_bookings)
        return response

    def all_bookings_by_room(self, room_id):
        """
        Get all bookings by room endpoint
        """
        url_get_bookings_by_room = f"{self.url_bookings}?roomid={room_id}"
        response = self.rest_client.request(
            method_name="get", url=url_get_bookings_by_room
        )
        return response

    def specific_booking(self, booking_id):
        """
        Get specific booking endpoint
        """
        url_get_booking = f"{self.url_bookings}{booking_id}"
        response = self.rest_client.request(method_name="get", url=url_get_booking)
        return response

    def booking_summary_by_room(self, room_id):
        """
        Get booking summary by room endpoint
        """
        url_get_booking_summary_by_room = f"{self.url_bookings}summary?roomid={room_id}"
        response = self.rest_client.request(
            method_name="get", url=url_get_booking_summary_by_room
        )
        return response

    def health_check_booking(self):
        """
        Health check booking endpoint
        """
        url_health_check_booking = f"{self.url_bookings}actuator/health"
        response = self.rest_client.request(
            method_name="get", url=url_health_check_booking
        )
        return response

    def create_booking(self, body=None, room_id=None):
        """
        Create booking endpoint
        """
        url_create_booking = f"{self.url_bookings}"
        body_booking = body
        if body is None:
            body_booking = self.generate_data(room_id=room_id)
        response = self.rest_client.request(
            method_name="post", url=url_create_booking, body=body_booking
        )
        return response

    def update_booking(self, booking_id, body=None, room_id=None):
        """
        Update booking endpoint
        """
        url_update_booking = f"{self.url_bookings}{booking_id}"
        body_booking = body
        if body is None:
            body_booking = self.generate_data(room_id=room_id)
        response = self.rest_client.request(
            method_name="put", url=url_update_booking, body=body_booking
        )
        return response

    def delete_booking(self, booking_id):
        """
        Delete booking endpoint
        """
        url_delete_booking = f"{self.url_bookings}{booking_id}"
        response = self.rest_client.request(
            method_name="delete", url=url_delete_booking
        )
        return response
