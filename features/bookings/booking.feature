@bookings
Feature: Bookings

    @acceptance
    Scenario: Get all bookings
        As a user
        I want to be able to retrieve all bookings
        So that I can view the details of all bookings

        When I call to "booking" endpoint using "get" method and without body
        Then I receive the response and validate using "get_all_bookings" json

    @booking_id
    @acceptance
    Scenario: Get a booking
        As a user
        I want to be able to retrieve a booking
        So that I can view the details of a booking

        When I call to "booking" endpoint using "get" method and without body
        Then I receive the response and validate using "get_booking" json

    @room_id
    Scenario: Create a booking
        As a user
        I want to be able to create a booking
        So that I can book a room

        When I call to "booking" endpoint using "post" method and with body
        Then I receive the response and validate using "create_booking" json

    @booking_id
    Scenario: Update a booking
        As a user
        I want to be able to update a booking
        So that I can change the details of a booking

        When I call to "booking" endpoint using "put" method and with body
        Then I receive the response and validate using "update_booking" json

    @booking_id
    Scenario: Delete a booking
        As a user
        I want to be able to delete a booking
        So that I can cancel a booking

        When I call to "booking" endpoint using "delete" method and without body
        Then I receive the response and validate using "delete_booking" json
