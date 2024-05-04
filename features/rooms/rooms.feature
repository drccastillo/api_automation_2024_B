@rooms
Feature: Rooms

    @acceptance
    @critical
    @allure.label.owner:DC
    @allure.link:https://jira.com/BOOK-001
    @allure.issue:BOOK-001
    Scenario: Get all rooms
        As a user
        I want to be able to retrieve all rooms
        So that I can view the details of all rooms

        When I call to "room" endpoint using "get" method and without body
        Then I receive the response and validate using "get_all_rooms" json

    @room_id
    @acceptance
    @critical
    @allure.label.owner:DC
    @allure.link:https://jira.com/BOOK-002
    @allure.issue:BOOK-002
    Scenario: Get a room
        As a user
        I want to be able to retrieve a room
        So that I can view the details of a room

        When I call to "room" endpoint using "get" method and without body
        Then I receive the response and validate using "get_room" json

    @acceptance
    @critical
    @allure.label.owner:DC
    @allure.link:https://jira.com/BOOK-003
    @allure.issue:BOOK-003
    Scenario: Create a room
        As a user
        I want to be able to create a room
        So that I can add a new room

        When I call to "room" endpoint using "post" method and with body
        Then I receive the response and validate using "create_room" json

    @room_id
    @acceptance
    @critical
    @allure.label.owner:DC
    @allure.link:https://jira.com/BOOK-004
    @allure.issue:BOOK-004
    Scenario: Update a room
        As a user
        I want to be able to update a room
        So that I can modify a room

        When I call to "room" endpoint using "put" method and with body
        Then I receive the response and validate using "update_room" json

    @room_id
    @acceptance
    @critical
    @allure.label.owner:DC
    @allure.link:https://jira.com/BOOK-005
    @allure.issue:BOOK-005
    Scenario: Delete a room
        As a user
        I want to be able to delete a room
        So that I can remove a room

        When I call to "room" endpoint using "delete" method and without body
        Then I receive the response and validate using "delete_room" json
