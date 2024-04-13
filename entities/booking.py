import logging
from faker import Faker
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


    def generate_booking_dates(self):
        """
        Generate booking dates with fake data.

        Returns:
            dict: The booking dates.
        """
        checkin_date = self.fake.date_between(start_date="-20y", end_date="-1m")
        checkout_date = self.fake.date_between_dates(
            date_start=checkin_date + timedelta(days=1),
            date_end=checkin_date + timedelta(days=self.fake.random_int(min=2, max=10)),
        )

        return {
            "checkin": checkin_date.strftime("%Y-%m-%d"),
            "checkout": checkout_date.strftime("%Y-%m-%d"),
        }

    def generate_good_data(self, room_id):
        """
        Generate good booking body with fake data.

        Args:
            room_id (int): The ID of the room for the booking.

        Returns:
            dict: The booking body.
        """
        return {
            "firstname": self.fake.first_name(),
            "lastname": self.fake.last_name(),
            "totalprice": self.fake.random_int(min=1, max=999),
            "depositpaid": self.fake.boolean(),
            "bookingdates": self.generate_booking_dates(),
            "additionalneeds": self.fake.sentence(),
            "roomid": room_id,
        }

    def generate_bad_data(self, room_id, bad_scenario):
        """
        Generate booking body with fake data based on the bad scenario.

        Args:
            room_id (int): The ID of the room for the booking.
            bad_scenario (str): The scenario for which to generate the booking body. 
                                Should be one of the following: "no_firstname", "no_lastname", 
                                "no_roomid", "no_checkin", "no_checkout", "no_bookingdates".

        Returns:
            dict: The booking body.
        """
        data = self.generate_good_data(room_id)

        bad_scenario_map = {
            "no_firstname": "firstname",
            "no_lastname": "lastname",
            "no_roomid": "roomid",
            "no_checkin": "bookingdates.checkin",
            "no_checkout": "bookingdates.checkout",
            "no_bookingdates": "bookingdates",
        }
        if bad_scenario not in bad_scenario_map:
            raise ValueError(f"Invalid bad scenario: {bad_scenario}")

        if "." in bad_scenario_map[bad_scenario]:
            key, subkey = bad_scenario_map[bad_scenario].split(".")
            if key in data and subkey in data[key]:
                del data[key][subkey]
        else:
            data[bad_scenario_map[bad_scenario]] = None

        return data

    def generate_data(self, room_id, scenario="good"):
        """
        Generate booking body with fake data based on the scenario.

        Args:
            room_id (int): The ID of the room for the booking.
            scenario (str): The scenario for which to generate the booking body. 
                            Should be either "good" or one of the following bad scenarios: 
                            "no_firstname", "no_lastname", "no_roomid", "no_checkin", 
                            "no_checkout", "no_bookingdates". Defaults to "good".

        Returns:
            dict: The booking body.
        """
        scenario_map = {
            "good": self.generate_good_data,
            "no_firstname": lambda room_id: self.generate_bad_data(room_id, "no_firstname"),
            "no_lastname": lambda room_id: self.generate_bad_data(room_id, "no_lastname"),
            "no_roomid": lambda room_id: self.generate_bad_data(room_id, "no_roomid"),
            "no_checkin": lambda room_id: self.generate_bad_data(room_id, "no_checkin"),
            "no_checkout": lambda room_id: self.generate_bad_data(room_id, "no_checkout"),
            "no_bookingdates": lambda room_id: self.generate_bad_data(room_id, "no_bookingdates"),
        }

        if scenario not in scenario_map:
            raise ValueError(f"Invalid scenario: {scenario}")

        data = scenario_map[scenario](room_id)

        LOGGER.info("new bad booking %s", data)
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
