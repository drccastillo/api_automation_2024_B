@messages
Feature: Messages

    @acceptance
    @critical
    @allure.label.owner:DC
    @allure.link:https://jira.com/BOOK-001
    @allure.issue:BOOK-001

    Scenario: Get all messages
        As a user
        I want to get all messages
        So that I can see all messages

        When I call to "message" endpoint using "get" method and without body
        Then I receive the response and validate using "get_all_messages" json

    @message_id
    @acceptance
    @critical
    @allure.label.owner:DC
    @allure.link:https://jira.com/BOOK-002
    @allure.issue:BOOK-002
    Scenario: Get message by id
        As a user
        I want to get message by id
        So that I can see message by id

        When I call to "message" endpoint using "get" method and without body
        Then I receive the response and validate using "get_message" json
