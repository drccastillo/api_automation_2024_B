# Python base image
FROM python:3

# Maintainer label
LABEL maintainer="darwin.castillo@jalasoft.com"

# Copy code to /opt/app folder
COPY . /opt/app
WORKDIR /opt/app

# Remove .venv directory if exists
RUN rm -rf .venv

# Update system
RUN apt-get update

# Install Java (always add -y option)
RUN apt-get install -y default-jre
RUN java -version

# Install allure
RUN wget https://github.com/allure-framework/allure2/releases/download/2.29.0/allure_2.29.0-1_all.deb
RUN dpkg -i allure_2.29.0-1_all.deb

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Install virtualenv
RUN python3 -m pip install --user virtualenv

# Create virtualenv for the framework
RUN python3 -m venv .venv

# Activate virtual environment
RUN . .venv/bin/activate

# Install requirements
RUN python3 -m pip install -r requirements.txt

# Run pre-commit hooks
RUN pre-commit run --all-files

# Add script to run tests
RUN chmod +x /opt/app/run_tests.sh

# Define entrypoint command
ENTRYPOINT ["/opt/app/run_tests.sh"]
