"""
This module contains the configuration for the Restful-Booker API.
"""
from __future__ import annotations

import os

from dotenv import load_dotenv

# Get the absolute path of the current directory
abs_path = os.path.abspath(__file__ + '../../../')

# Load environment variables from the .env file
load_dotenv()

# Webhook URL for sending notifications
WEB_HOOK = os.getenv('RESTFUL_BOOKER_WEB_HOOK')

# Base URL for the Restful-Booker API
BASE_URL = os.getenv('RESTFUL_BOOKER_BASE_URL')

# Credentials for authentication
CREDENTIALS = {
    'username': os.getenv('RESTFUL_BOOKER_USERNAME'),
    'password': os.getenv('RESTFUL_BOOKER_PASSWORD'),
}

# Token for authorization
TOKEN = os.getenv('RESTFUL_BOOKER_TOKEN')

# Default headers for requests to the Restful-Booker API
DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

# Add authorization if a token is provided
if TOKEN:
    DEFAULT_HEADERS['Cookie'] = f'token={TOKEN}'


CONFIGURATION = {
    'browser': {
        'name': 'chrome',
        'headless': False,
        'resolution': {
            'width': 800,
            'height': 600,
        },
    },
}
GRID_URL = os.getenv('RESTFUL_BOOKER_GRID_URL')
