import logging
from config.config import BASE_URL
from helpers.validate_response import ValidateResponse
from helpers.rest_client import RestClient
from entities.room import Room
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

class TestRooms:
    @classmethod
    def setup_class(cls):
        """
        Setup class for Rooms
        """
        LOGGER.info ("Setup Class for Rooms")
        cls.rest_client = RestClient()
        cls.validate = ValidateResponse()
        cls.room = Room()
        cls.room_list = []


    def test_get_all_rooms(self, log_test_names):
        """
        Test get all rooms endpoint
        """
        LOGGER.info("Test get all rooms")
        response = self.room.all_rooms()
        self.validate.validate_response(actual_response=response, endpoint="room", file_name="get_all_rooms")

    def test_get_room(self, create_room, log_test_names):
        """
        Test get room endpoint
        """
        LOGGER.info("Test get room")
        response = self.room.specific_room(room_id=create_room)
        self.validate.validate_response(actual_response=response, endpoint="room", file_name="get_room")
    
    def test_get_health_check(self, log_test_names): # noqa: N805   
        """
        Test get health check endpoint
        """
        LOGGER.info("Test get health check")
        response = self.room.health_check_room()
        self.validate.validate_response(actual_response=response, endpoint="room", file_name="get_health_check")
    
    def test_create_room(self, log_test_names):
        """
        Test create room
        """
        LOGGER.info("Test create room")
        body_room = self.room.generate_data()
        response = self.room.create_room(body=body_room)
        self.validate.validate_response(actual_response=response, endpoint="room", file_name="create_room")
        self.room_list.append(response["json"]["roomid"])

    def test_update_room(self, create_room, log_test_names):
        """
        Test update room
        """
        LOGGER.info("Test update room")
        body_room = self.room.generate_data()
        response = self.room.update_room(room_id=create_room, body=body_room)
        self.validate.validate_response(actual_response=response, endpoint="room", file_name="update_room")
    
    def test_delete_room(self, create_room, log_test_names):
        """
        Test delete room
        """
        LOGGER.info("Test delete room")
        response = self.room.delete_room(room_id=create_room)
        self.validate.validate_response(actual_response=response, endpoint="room", file_name="delete_room")


    @classmethod
    def teardown_class(cls):
        """
        Teardown class for Rooms
        """
        LOGGER.info ("Cleanup rooms")
        for id_room in cls.room_list:
            response = cls.room.delete_room(room_id=id_room)
            if response["status_code"] == 202:
                LOGGER.info("Room %s deleted", id_room)            
