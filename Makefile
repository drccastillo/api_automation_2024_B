install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

log:
	python -m unittest unittests/test_logger.py

test-all:
	python -m pytest -v api/rooms/test_rooms.py api/bookings/test_bookings.py api/brandings/test_brandings.py api/messages/test_messages.py api/reports/test_reports.py

test-auth:
	python -m pytest -v api/auth/test_auths.py

test-bookings:
	python -m pytest -v api/bookings/test_bookings.py

test-rooms:
	python -m pytest -v api/rooms/test_rooms.py	

test-brandings:
	python -m pytest -v api/brandings/test_brandings.py

test-messages:
	python -m pytest -v api/messages/test_messages.py

test-reports:
	python -m pytest -v api/reports/test_reports.py

junitxml-all:
	python -m pytest -v -s --junitxml=reports/junitxml/report_all.xml api/rooms/test_rooms.py api/bookings/test_bookings.py api/brandings/test_brandings.py api/messages/test_messages.py api/reports/test_reports.py

html-all: 
	python -m pytest -v -s --html=reports/html/pytest_html_report_all.html api/rooms/test_rooms.py api/bookings/test_bookings.py api/brandings/test_brandings.py api/messages/test_messages.py api/reports/test_reports.py

excel-all: 
	python -m pytest -v -s --excelreport=reports/excel/report_all.xlsx api/rooms/test_rooms.py api/bookings/test_bookings.py api/brandings/test_brandings.py api/messages/test_messages.py api/reports/test_reports.py

markdown-all: 
	python -m pytest -v -s --md-report --md-report-output reports/markdown/md_report_all.md api/rooms/test_rooms.py api/bookings/test_bookings.py api/brandings/test_brandings.py api/messages/test_messages.py api/reports/test_reports.py

junitxml-auth:
	python -m pytest -v -s --junitxml=reports/junitxml/report_auth.xml api/auth/test_auths.py

html-auth: 
	python -m pytest -v -s --html=reports/html/pytest_html_report_auth.html api/auth/test_auths.py

excel-auth: 
	python -m pytest -v -s --excelreport=reports/excel/report_auth.xlsx api/auth/test_auths.py

markdown-auth: 
	python -m pytest -v -s --md-report --md-report-output reports/markdown/md_report_auth.md api/auth/test_auths.py

junitxml-bookings:
	python -m pytest -v -s --junitxml=reports/junitxml/report_bookings.xml api/bookings/test_bookings.py

html-bookings: 
	python -m pytest -v -s --html=reports/html/pytest_html_report_bookings.html api/bookings/test_bookings.py

excel-bookings: 
	python -m pytest -v -s --excelreport=reports/excel/report_bookings.xlsx api/bookings/test_bookings.py

markdown-bookings: 
	python -m pytest -v -s --md-report --md-report-output reports/markdown/md_report_bookings.md api/bookings/test_bookings.py

junitxml-rooms:
	python -m pytest -v -s --junitxml=reports/junitxml/report_rooms.xml api/rooms/test_rooms.py

html-rooms: 
	python -m pytest -v -s --html=reports/html/pytest_html_report_rooms.html api/rooms/test_rooms.py

excel-rooms: 
	python -m pytest -v -s --excelreport=reports/excel/report_rooms.xlsx api/rooms/test_rooms.py

markdown-rooms: 
	python -m pytest -v -s --md-report --md-report-output reports/markdown/md_report_rooms.md api/rooms/test_rooms.py

junitxml-brandings:
	python -m pytest -v -s --junitxml=reports/junitxml/report_brandings.xml api/brandings/test_brandings.py

html-brandings: 
	python -m pytest -v -s --html=reports/html/pytest_html_report_brandings.html api/brandings/test_brandings.py

excel-brandings: 
	python -m pytest -v -s --excelreport=reports/excel/report_brandings.xlsx api/brandings/test_brandings.py

markdown-brandings: 
	python -m pytest -v -s --md-report --md-report-output reports/markdown/md_report_brandings.md api/brandings/test_brandings.py

junitxml-messages:
	python -m pytest -v -s --junitxml=reports/junitxml/report_messages.xml api/messages/test_messages.py

html-messages: 
	python -m pytest -v -s --html=reports/html/pytest_html_report_messages.html api/messages/test_messages.py

excel-messages: 
	python -m pytest -v -s --excelreport=reports/excel/report_messages.xlsx api/messages/test_messages.py

markdown-messages: 
	python -m pytest -v -s --md-report --md-report-output reports/markdown/md_report_messages.md api/messages/test_messages.py

junitxml-reports:
	python -m pytest -v -s --junitxml=reports/junitxml/report_reports.xml api/reports/test_reports.py

html-reports: 
	python -m pytest -v -s --html=reports/html/pytest_html_report_reports.html api/reports/test_reports.py

excel-reports: 
	python -m pytest -v -s --excelreport=reports/excel/report_reports.xlsx api/reports/test_reports.py

markdown-reports: 
	python -m pytest -v -s --md-report --md-report-output reports/markdown/md_report_reports.md api/reports/test_reports.py

allure-auth: allure-clean allure-generate-auth allure-open

allure-bookings: allure-clean allure-generate-bookings allure-open

allure-rooms: allure-clean allure-generate-rooms allure-open

allure-brandings: allure-clean allure-generate-brandings allure-open

allure-messages: allure-clean allure-generate-messages allure-open

allure-reports: allure-clean allure-generate-reports allure-open

allure-all: allure-clean allure-generate-all allure-open

allure-clean:
	rm -rf allure-report allure-results

allure-generate-auth:
	python -m pytest -v -s --alluredir=reports/allure/auth api/auth/test_auths.py

allure-generate-bookings:
	python -m pytest -v -s --alluredir=reports/allure/bookings api/bookings/test_bookings.py

allure-generate-rooms:
	python -m pytest -v -s --alluredir=reports/allure/rooms api/rooms/test_rooms.py

allure-generate-brandings:
	python -m pytest -v -s --alluredir=reports/allure/brandings api/brandings/test_brandings.py

allure-generate-messages:
	python -m pytest -v -s --alluredir=reports/allure/messages api/messages/test_messages.py

allure-generate-reports:
	python -m pytest -v -s --alluredir=reports/allure/reports api/reports/test_reports.py

allure-generate-all:
	python -m pytest -v -s --alluredir=reports/allure/all api/bookings/test_bookings.py api/rooms/test_rooms.py api/brandings/test_brandings.py api/messages/test_messages.py api/reports/test_reports.py

allure-open:
	allure serve reports/allure/

format:
	python -m black **/*.py

lint:
	pylint unittests/test_logger.py

all: install lint test

