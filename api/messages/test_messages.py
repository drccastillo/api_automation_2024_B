import logging
import pytest
import allure

from helpers.validate_response import ValidateResponse
from helpers.rest_client import RestClient
from utils.logger import get_logger
from entities.message import Message

LOGGER = get_logger(__name__, logging.DEBUG)

@allure.epic("Message API")
@allure.story("Message API Endpoints")
class TestMessages:
    @classmethod
    def setup_class(cls):
        """
        Setup class for Messages
        """
        LOGGER.info ("Setup Class for Messages")
        cls.rest_client = RestClient()
        cls.message = Message()
        cls.validate = ValidateResponse()
        cls.message_list = []

    @allure.title("Get all messages")
    @allure.tag("Message", "Get")
    @pytest.mark.acceptance
    def test_get_all_messages(self, log_test_names):
        """
        Test get all messages endpoint
        """
        LOGGER.info("Test get all messages")
        response = self.message.all_messages()
        self.validate.validate_response(actual_response=response, endpoint="message", file_name="get_all_messages")


    @allure.title("Get a message")
    @allure.tag("Message", "Get")
    @pytest.mark.acceptance
    def test_get_message(self, create_message, log_test_names):   
        """
        Test get message endpoint
        """
        LOGGER.info("Test get message")
        response = self.message.specific_message(message_id=create_message)
        self.validate.validate_response(actual_response=response, endpoint="message", file_name="get_message")


    @allure.title("Get unread messages")
    @allure.tag("Message", "Get")
    @pytest.mark.acceptance
    def test_get_unread_messages(self, log_test_names):
        """
        Test get unread messages endpoint
        """
        LOGGER.info("Test get unread messages")
        response = self.message.unread_messages()
        self.validate.validate_response(actual_response=response, endpoint="message", file_name="get_unread_messages")


    @allure.title("Check health of message service")
    @allure.tag("Message", "Get")
    @pytest.mark.smoke
    def test_get_health_check(self, log_test_names):    
        """
        Test get health check endpoint
        """
        LOGGER.info("Test get health check")
        response = self.message.health_check_message()
        self.validate.validate_response(actual_response=response, endpoint="message", file_name="get_health_check")


    @allure.title("Create a message")
    @allure.tag("Message", "Create")
    @pytest.mark.acceptance
    def test_create_message(self, log_test_names):
        """
        Test create message
        """
        LOGGER.info("Test create message")
        body_message = self.message.generate_data()
        response = self.message.create_message(body=body_message)
        self.validate.validate_response(actual_response=response, endpoint="message", file_name="create_message")
        self.message_list.append(response["json"]["messageid"])


    @allure.title("Mark a message as read")
    @allure.tag("Message", "Update")
    @pytest.mark.acceptance
    def test_mark_message_as_read(self, create_message, log_test_names):
        """
        Test mark message as read
        """
        LOGGER.info("Test mark message as read")
        response = self.message.mark_message_as_read(message_id=create_message)
        self.validate.validate_response(actual_response=response, endpoint="message", file_name="mark_message_as_read")


    @allure.title("Delete a message")
    @allure.tag("Message", "Delete")
    @pytest.mark.acceptance
    def test_delete_message(self, create_message, log_test_names):
        """
        Test delete message
        """
        LOGGER.info("Test delete message")
        response = self.message.delete_message(message_id=create_message)
        self.validate.validate_response(actual_response=response, endpoint="message", file_name="delete_message")


    @classmethod
    def teardown_class(cls):
        """
        Teardown class for Messages
        """
        LOGGER.info ("Teardown Class for Messages")
        for message_id in cls.message_list:           
            response = cls.message.delete_message(message_id=message_id)
            if response["status_code"] == 202:
                LOGGER.info("Message %s deleted", message_id)
