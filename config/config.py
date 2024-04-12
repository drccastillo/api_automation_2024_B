"""
This module contains the configuration for the Restful-Booker API.
"""

import os
from dotenv import load_dotenv

# Get the absolute path of the current directory
abs_path = os.path.abspath(__file__ + "../../../")

# Load environment variables from the .env file
load_dotenv()

# Base URL for the Restful-Booker API
BASE_URL = os.getenv("RESTFUL_BOOKER_BASE_URL", "https://restful-booker.herokuapp.com")

# Credentials for authentication
CREDENTIALS = {
    "username": os.getenv("RESTFUL_BOOKER_USERNAME"),
    "password": os.getenv("RESTFUL_BOOKER_PASSWORD"),
}

# Token for authorization
TOKEN = os.getenv("RESTFUL_BOOKER_TOKEN")

# Default headers for requests to the Restful-Booker API
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# Add authorization if a token is provided
if TOKEN:
    DEFAULT_HEADERS["cookie"] = f"token={TOKEN}"
