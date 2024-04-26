export PYTHONPATH := /home/dcc/apps/api_automation_2024_B:/home/dcc/apps/api_automation_2024_B

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test-logger:
	- python -m unittest unittests/test_logger.py

test-restclient:
	- python -m unittest unittests/test_rest_client.py

test-all:
	- python -m pytest -v booker_api/rooms/test_rooms.py booker_api/bookings/test_bookings.py booker_api/brandings/test_brandings.py booker_api/messages/test_messages.py booker_api/reports/test_reports.py

test-auth:
	- python -m pytest -v booker_api/auth/test_auths.py

test-bookings:
	- python -m pytest -v booker_api/bookings/test_bookings.py

test-rooms:
	- python -m pytest -v booker_api/rooms/test_rooms.py

test-brandings:
	- python -m pytest -v booker_api/brandings/test_brandings.py

test-messages:
	- python -m pytest -v booker_api/messages/test_messages.py

test-reports:
	- python -m pytest -v booker_api/reports/test_reports.py

junitxml-all:
	- python -m pytest -v -s --junitxml=reports/junitxml/report_all.xml booker_api/rooms/test_rooms.py booker_api/bookings/test_bookings.py booker_api/brandings/test_brandings.py booker_api/messages/test_messages.py booker_api/reports/test_reports.py

html-all:
	- python -m pytest -v -s --html=reports/html/pytest_html_report_all.html booker_api/rooms/test_rooms.py booker_api/bookings/test_bookings.py booker_api/brandings/test_brandings.py booker_api/messages/test_messages.py booker_api/reports/test_reports.py

excel-all:
	- python -m pytest -v -s --excelreport=reports/excel/report_all.xlsx booker_api/rooms/test_rooms.py booker_api/bookings/test_bookings.py booker_api/brandings/test_brandings.py booker_api/messages/test_messages.py booker_api/reports/test_reports.py

markdown-all:
	- python -m pytest -v -s --md-report --md-report-output reports/markdown/md_report_all.md booker_api/rooms/test_rooms.py booker_api/bookings/test_bookings.py booker_api/brandings/test_brandings.py booker_api/messages/test_messages.py booker_api/reports/test_reports.py

junitxml-auth:
	- python -m pytest -v -s --junitxml=reports/junitxml/report_auth.xml booker_api/auth/test_auths.py

html-auth:
	- python -m pytest -v -s --html=reports/html/pytest_html_report_auth.html booker_api/auth/test_auths.py

excel-auth:
	- python -m pytest -v -s --excelreport=reports/excel/report_auth.xlsx booker_api/auth/test_auths.py

markdown-auth:
	- python -m pytest -v -s --md-report --md-report-output reports/markdown/md_report_auth.md booker_api/auth/test_auths.py

junitxml-bookings:
	- python -m pytest -v -s --junitxml=reports/junitxml/report_bookings.xml booker_api/bookings/test_bookings.py

html-bookings:
	- python -m pytest -v -s --html=reports/html/pytest_html_report_bookings.html booker_api/bookings/test_bookings.py

excel-bookings:
	- python -m pytest -v -s --excelreport=reports/excel/report_bookings.xlsx booker_api/bookings/test_bookings.py

markdown-bookings:
	- python -m pytest -v -s --md-report --md-report-output reports/markdown/md_report_bookings.md booker_api/bookings/test_bookings.py

junitxml-rooms:
	- python -m pytest -v -s --junitxml=reports/junitxml/report_rooms.xml booker_api/rooms/test_rooms.py

html-rooms:
	- python -m pytest -v -s --html=reports/html/pytest_html_report_rooms.html booker_api/rooms/test_rooms.py

excel-rooms:
	- python -m pytest -v -s --excelreport=reports/excel/report_rooms.xlsx booker_api/rooms/test_rooms.py

markdown-rooms:
	- python -m pytest -v -s --md-report --md-report-output reports/markdown/md_report_rooms.md booker_api/rooms/test_rooms.py

junitxml-brandings:
	- python -m pytest -v -s --junitxml=reports/junitxml/report_brandings.xml booker_api/brandings/test_brandings.py

html-brandings:
	- python -m pytest -v -s --html=reports/html/pytest_html_report_brandings.html booker_api/brandings/test_brandings.py

excel-brandings:
	- python -m pytest -v -s --excelreport=reports/excel/report_brandings.xlsx booker_api/brandings/test_brandings.py

markdown-brandings:
	- python -m pytest -v -s --md-report --md-report-output reports/markdown/md_report_brandings.md booker_api/brandings/test_brandings.py

junitxml-messages:
	- python -m pytest -v -s --junitxml=reports/junitxml/report_messages.xml booker_api/messages/test_messages.py

html-messages:
	- python -m pytest -v -s --html=reports/html/pytest_html_report_messages.html booker_api/messages/test_messages.py

excel-messages:
	- python -m pytest -v -s --excelreport=reports/excel/report_messages.xlsx booker_api/messages/test_messages.py

markdown-messages:
	- python -m pytest -v -s --md-report --md-report-output reports/markdown/md_report_messages.md booker_api/messages/test_messages.py

junitxml-reports:
	- python -m pytest -v -s --junitxml=reports/junitxml/report_reports.xml booker_api/reports/test_reports.py

html-reports:
	- python -m pytest -v -s --html=reports/html/pytest_html_report_reports.html booker_api/reports/test_reports.py

excel-reports:
	- python -m pytest -v -s --excelreport=reports/excel/report_reports.xlsx booker_api/reports/test_reports.py

markdown-reports:
	- python -m pytest -v -s --md-report --md-report-output reports/markdown/md_report_reports.md booker_api/reports/test_reports.py

allure-auth: allure-clean allure-generate-auth

allure-bookings: allure-clean allure-generate-bookings

allure-rooms: allure-clean allure-generate-rooms

allure-brandings: allure-clean allure-generate-brandings

allure-messages: allure-clean allure-generate-messages

allure-reports: allure-clean allure-generate-reports

allure-all: allure-clean allure-generate-all

behave-all: allure-clean
	- python -m behave

behave-rerun:
	- python -m behave -f rerun -o failed_features.feature

allure-clean:
	rm -rf reports/allure/reports/* reports/allure/results/*

allure-generate-auth:
	python -m pytest -v -s --alluredir=reports/allure/results booker_api/auth/test_auths.py

allure-generate-bookings:
	python -m pytest -v -s --alluredir=reports/allure/results booker_api/bookings/test_bookings.py

allure-generate-rooms:
	python -m pytest -v -s --alluredir=reports/allure/results booker_api/rooms/test_rooms.py

allure-generate-brandings:
	python -m pytest -v -s --alluredir=reports/allure/results booker_api/brandings/test_brandings.py

allure-generate-messages:
	python -m pytest -v -s --alluredir=reports/allure/results booker_api/messages/test_messages.py

allure-generate-reports:
	python -m pytest -v -s --alluredir=reports/allure/results booker_api/reports/test_reports.py

allure-generate-all:
	python -m pytest -v -s --alluredir=reports/allure/results booker_api/bookings/test_bookings.py booker_api/rooms/test_rooms.py booker_api/brandings/test_brandings.py booker_api/messages/test_messages.py booker_api/reports/test_reports.py

web-hook-auth: markdown-auth
	python utils/web_hook.py auth

web-hook-bookings: markdown-bookings
	python utils/web_hook.py bookings

web-hook-rooms: markdown-rooms
	python utils/web_hook.py rooms

web-hook-brandings: markdown-brandings
	python utils/web_hook.py brandings

web-hook-messages: markdown-messages
	python utils/web_hook.py messages

web-hook-reports: markdown-reports
	python utils/web_hook.py reports

web-hook-all: markdown-all
	python utils/web_hook.py all

format:
	find . -type f -name '*.py' -not -path '*/\.git/*' -not -path '*/\.gitignore' -not -path '*/\.*' | xargs python -m black --line-length=100

lint:
	- pylint **/*.py

pre-commit:
	- pre-commit run --all-files

all: install lint test
