#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Run tests
python3 -m pytest booker_api/rooms/test_rooms.py booker_api/bookings/test_bookings.py booker_api/brandings/test_brandings.py booker_api/messages/test_messages.py booker_api/reports/test_reports.py -v -s --alluredir reports/allure/results

# Generate Allure report
allure serve --port 9999 reports/allure/results
