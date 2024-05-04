@brandings
Feature: Brandings

    @acceptance
    Scenario: Get all brandings
        As a user
        I want to be able to retrieve all brandings
        So that I can view the details of all brandings

        When I call to "branding" endpoint using "get" method and without body
        Then I receive the response and validate using "get_all_brandings" json

    @acceptance
    Scenario: Update branding
        As a user
        I want to be able to update branding
        So that I can change the details of branding

        When I call to "branding" endpoint using "put" method and with body
        Then I receive the response and validate using "update_branding" json
