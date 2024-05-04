@Reports
Feature:Reports
    @acceptance
    @critical
    @allure.label.owner:DC
    @allure.link:https://jira.com/BOOK-001
    @allure.issue:BOOK-001
    Scenario: Get all reports
        As a user
        I want to be able to get all reports
        So that I can view the details of all reports

        When I call to "report" endpoint using "get" method and without body
        Then I receive the response and validate using "get_all_reports" json

    @room_id
    @acceptance
    @critical
    @allure.label.owner:DC
    @allure.link:https://jira.com/BOOK-002
    @allure.issue:BOOK-002
    Scenario: Get reports by room
        As a user
        I want to be able to get reports by room
        So that I can view the details of reports by room

        When I call to "report" endpoint using "get" method and without body
        Then I receive the response and validate using "get_specific_room_report" json
