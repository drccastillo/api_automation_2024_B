import logging


from config.config import url_booker
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class TestBookings:
    @classmethod
    def setup_class(cls):
        """
        Setup class for bookings
        """
        cls.rest_client = RestClient()
        cls.url_booker_bookings = f"{url_booker}/booking"
        response = cls.rest_client.request("get", cls.url_booker_bookings)
        cls.booking_id = response["body"][0]["bookingid"]
        LOGGER.debug("Booking ID: %s", cls.booking_id)
        cls.bookings_list = []

    def test_get_all_bookings(self, log_test_names):
        """
        Test get all bookings endpoint
        """
        LOGGER.info("Test get all bookings")
        response = self.rest_client.request("get", self.url_booker_bookings)

        assert response["status_code"] == 200

    def test_get_booking(self, log_test_names):
        """
        Test get booking endpoint
        """
        LOGGER.info("Test get booking")
        url_get_booking = f"{self.url_booker_bookings}/{self.booking_id}"
        response = self.rest_client.request("get", url_get_booking)

        assert response["status_code"] == 200

    def test_create_booking(self, log_test_names):
        """
        Test create booking
        """
        LOGGER.info("Test create booking")
        body_booking = {
            "firstname" : "Jim from Test",
            "lastname" : "Brown from Test",
            "totalprice" : 111,
            "depositpaid" : "true",
            "bookingdates" : {
                "checkin" : "2023-01-01",
                "checkout" : "2024-01-01"
            },
            "additionalneeds" : "Breakfast from test"
        }
        response = self.rest_client.request("post", self.url_booker_bookings, body=body_booking)
        if response["status_code"] == 200:
            self.bookings_list.append(response["body"]["bookingid"])

        assert response["status_code"] == 200
        LOGGER.debug("list booking %s", self.bookings_list)

    def test_delete_booking(self, create_booking_wo_delete, log_test_names):
        """
        Test delete booking
        """
        LOGGER.info("Test delete booking")
        url_delete_booking = f"{self.url_booker_bookings}/{create_booking_wo_delete}"
        LOGGER.info("booking Id to be deleted : %s", create_booking_wo_delete)
        response = self.rest_client.request("delete", url_delete_booking)
        assert response["status_code"] == 201


    def test_update_project(self, create_booking, log_test_names):
        """

        :param create_booking:
        :param log_test_names:
        :return:
        """
        LOGGER.info("Test update booking")
        url_update_booking = f"{self.url_booker_bookings}/{create_booking}"
        body_update_booking = {
            "firstname" : "James Update",
            "lastname" : "Brown Update",
            "totalprice" : 111,
            "depositpaid" : "true",
            "bookingdates" : {
                "checkin" : "2018-01-01",
                "checkout" : "2019-01-01"
            },
            "additionalneeds" : "Breakfast Update"
        }
        # call to endpoint:
        response = self.rest_client.request("put", url_update_booking, body=body_update_booking)

        assert response["status_code"] == 200           

    @classmethod
    def teardown_class(cls):
        """
        PyTest teardown class
        """
        LOGGER.debug("Teardown class")
        LOGGER.debug("Cleanup bookings data")
        for booking_id in cls.bookings_list:
            url_delete_booking = f"{cls.url_booker_bookings}/{booking_id}"
            response = cls.rest_client.request("delete", url_delete_booking)
            if response["status_code"] == 201:
                LOGGER.info("booking Id deleted : %s", booking_id)
