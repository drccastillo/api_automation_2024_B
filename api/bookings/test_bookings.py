import logging
import pytest
import allure

from helpers.validate_response import ValidateResponse
from helpers.rest_client import RestClient
from utils.logger import get_logger
from entities.booking import Booking


LOGGER = get_logger(__name__, logging.DEBUG)

@allure.epic("Booking API")
@allure.story("Booking API Endpoints")
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
    

    @allure.title("Get all bookings")
    @allure.tag("Booking", "Get")
    @pytest.mark.acceptance
    def test_get_all_bookings(self, log_test_names):
        """
        Test get all bookings endpoint
        """
        LOGGER.info("Test get all bookings")
        response = self.booking.all_bookings()
        self.validate.validate_response(actual_response=response, endpoint="booking", file_name="get_all_bookings")


    @allure.title("{title}")
    @allure.issue("https://jira.com/BOOK-001", name="BOOK-001")
    @allure.testcase("https://jira.com/BOOK-002", name="BOOK-002")
    @allure.tag("Booking", "Get")
    @pytest.mark.parametrize(
        "scenario, file_name, title",
        [
            pytest.param("exist", "get_booking", "Get an existing booking", marks=pytest.mark.acceptance),
            pytest.param("non_exist", "get_booking_not_exist", "Get a non-existing booking", marks=pytest.mark.functional),
        ]
    )   
    def test_get_booking(self, booking_id, scenario, file_name, title, log_test_names):
        """
        Test get booking endpoint
        """
        LOGGER.info(f"Test get booking with scenario: {scenario}")
        response = self.booking.specific_booking(booking_id=booking_id)
        self.validate.validate_response(actual_response=response, endpoint="booking", file_name=file_name)
    

    @allure.title("Get bookings by room")
    @allure.issue("https://jira.com/BOOK-001", name="BOOK-001")
    @allure.testcase("https://jira.com/BOOK-002", name="BOOK-002")
    @allure.tag("Booking", "Get")    
    @pytest.mark.acceptance
    def test_get_bookings_by_room(self, create_booking, log_test_names):
        """
        Test get booking by room endpoint
        """
        LOGGER.info("Test get booking by room")
        response = self.booking.all_bookings_by_room(room_id=create_booking['room_id'])
        self.validate.validate_response(actual_response=response, endpoint="booking", file_name="get_bookings_by_room")
    
    @allure.title("Get bookings summary by room")
    @allure.issue("https://jira.com/BOOK-001", name="BOOK-001")
    @allure.testcase("https://jira.com/BOOK-002", name="BOOK-002")
    @allure.tag("Booking", "Get")  
    @pytest.mark.acceptance
    def test_get_booking_summary(self, create_booking, log_test_names):
        """
        Test get bookings summary by room endpoint
        """
        LOGGER.info("Test get booking summary")
        response = self.booking.booking_summary_by_room(room_id=create_booking['room_id'])
        self.validate.validate_response(actual_response=response, endpoint="booking", file_name="get_booking_summary")
    
    @allure.title("Check health of the booking service")
    @allure.tag("Booking", "Get")
    @pytest.mark.smoke
    def test_get_health_check(self, log_test_names): # noqa: N805
        """
        Test get health check endpoint
        """
        LOGGER.info("Test get health check")
        response = self.booking.health_check_booking()
        self.validate.validate_response(actual_response=response, endpoint="booking", file_name="get_health_check")

    @allure.title("{title}")
    @allure.tag("Booking", "Create")
    @pytest.mark.parametrize(
        "scenario, file_name, title",
        [
            pytest.param("good", "create_booking", "Create a booking", marks=pytest.mark.acceptance),
            pytest.param("no_firstname", "create_booking_bad_body", "Create a booking with missing Firstname", marks=pytest.mark.functional),
            pytest.param("no_lastname", "create_booking_bad_body","Create a booking with missing Lastname", marks=pytest.mark.functional),
            pytest.param("no_roomid", "create_booking_bad_body","Create a booking with missing Room", marks=pytest.mark.functional),
            pytest.param("no_checkin", "create_booking_bad_body","Create a booking with missing Checkin", marks=pytest.mark.functional),
            pytest.param("no_checkout", "create_booking_bad_body","Create a booking with missing Checkout", marks=pytest.mark.functional),
            pytest.param("no_bookingdates","create_booking_bad_body","Create a booking with missing Dates", marks=pytest.mark.functional),
        ],
    )
    def test_create_booking(self, create_room, scenario, file_name, title, log_test_names):
        """
        Test create booking with both good and bad scenarios.
        """
        LOGGER.info(f"Test create booking with scenario: {scenario}")
        body_booking = self.booking.generate_data(room_id=create_room, scenario=scenario)
        response = self.booking.create_booking(body=body_booking)
        self.validate.validate_response(actual_response=response, endpoint="booking", file_name=file_name)
        
        if scenario == "good":
            self.bookings_list.append(response["json"]["bookingid"])


    @allure.title("Update a booking")
    @allure.tag("Booking", "Update")
    @pytest.mark.acceptance
    def test_update_booking(self, create_booking, log_test_names):
        """
        Test update booking endpoint
        """
        LOGGER.info("Test update booking")
        body_update_booking = self.booking.generate_data(room_id=create_booking['room_id'])
        response = self.booking.update_booking(booking_id=create_booking['booking_id'], body=body_update_booking)
        self.validate.validate_response(actual_response=response, endpoint="booking", file_name="update_booking")

    @allure.title("Delete a booking")
    @allure.tag("Booking", "Delete")
    @pytest.mark.acceptance
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
