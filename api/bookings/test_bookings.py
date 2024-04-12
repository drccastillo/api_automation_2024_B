import logging
import random

from config.config import BASE_URL
from helpers.validate_response import ValidateResponse
from helpers.rest_client import RestClient
from utils.logger import get_logger
from entities.booking import Booking


LOGGER = get_logger(__name__, logging.DEBUG)


class TestBookings:
    @classmethod
    def setup_class(cls):
        """
        Setup class for bookings
        """
        cls.rest_client = RestClient()
        cls.booking = Booking()
        cls.validate = ValidateResponse()
        cls.bookings_list = []

    def test_get_all_bookings(self, log_test_names):
        """
        Test get all bookings endpoint
        """
        LOGGER.info("Test get all bookings")
        response = self.booking.all_bookings()
        self.validate.validate_response(actual_response=response, endpoint="booking", file_name="get_all_bookings")


    def test_get_booking(self, create_booking, log_test_names):
        """
        Test get booking endpoint
        """
        LOGGER.info("Test get booking")
        response = self.booking.specific_booking(booking_id=create_booking["booking_id"])
        self.validate.validate_response(actual_response=response, endpoint="booking", file_name="get_booking")
    
    def test_get_bookings_by_room(self, create_booking, log_test_names):
        """
        Test get booking by room endpoint
        """
        LOGGER.info("Test get booking by room")
        response = self.booking.all_bookings_by_room(room_id=create_booking['room_id'])
        self.validate.validate_response(actual_response=response, endpoint="booking", file_name="get_bookings_by_room")

    def test_get_booking_summary(self, create_booking, log_test_names):
        """
        Test get booking summary endpoint
        """
        LOGGER.info("Test get booking summary")
        response = self.booking.booking_summary_by_room(room_id=create_booking['room_id'])
        self.validate.validate_response(actual_response=response, endpoint="booking", file_name="get_booking_summary")

    def test_get_health_check(self, log_test_names): # noqa: N805
        """
        Test get health check endpoint
        """
        LOGGER.info("Test get health check")
        response = self.booking.health_check_booking()
        self.validate.validate_response(actual_response=response, endpoint="booking", file_name="get_health_check")
    
    def test_create_booking(self, create_room, log_test_names):
        """
        Test create booking
        """
        LOGGER.info("Test create booking")
        body_booking = self.booking.generate_data(room_id=create_room)
        response = self.booking.create_booking(body=body_booking)
        self.validate.validate_response(actual_response=response, endpoint="booking", file_name="create_booking")
        self.bookings_list.append(response["json"]["bookingid"])


    def test_update_booking(self, create_booking, log_test_names):
        """
        Test update booking endpoint
        """
        LOGGER.info("Test update booking")
        body_update_booking = self.booking.generate_data(room_id=create_booking['room_id'])
        response = self.booking.update_booking(booking_id=create_booking['booking_id'], body=body_update_booking)
        self.validate.validate_response(actual_response=response, endpoint="booking", file_name="update_booking")

    def test_delete_booking(self, create_booking, log_test_names):
        """
        Test delete  booking endpoint
        """
        LOGGER.info("Test delete booking")
        response = self.booking.delete_booking(booking_id=create_booking['booking_id'])
        self.validate.validate_response(actual_response=response, endpoint="booking", file_name="delete_booking")

    @classmethod
    def teardown_class(cls):
        """
        PyTest teardown class
        """
        LOGGER.debug("Teardown class")
        LOGGER.debug("Cleanup bookings data")
        for booking_id in cls.bookings_list:
            response = cls.booking.delete_booking(booking_id)
            if response["status_code"] == 202:
                LOGGER.info("booking Id deleted : %s", booking_id)
