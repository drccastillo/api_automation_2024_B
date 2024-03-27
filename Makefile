install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

log:
	python -m unittest unittests/test_logger.py

test:
	python -m pytest -v booker_api/bookings/test_bookings.py

format:
	python -m black **/*.py

lint:
	pylint unittests/test_logger.py

all: install lint test