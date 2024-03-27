from dotenv import load_dotenv
from utils.logger import get_logger
import os
import requests
import logging


# Set up logging
LOGGER = get_logger(__name__, logging.DEBUG)

# Load enviromment variables from .env file
load_dotenv()

# Retrive values from enviromment variables
user_booker_api = os.getenv("user")
password_booker_api = os.getenv("password")
url_booker = "https://restful-booker.herokuapp.com"
headers_booker = {}
body_credential_booker = {"username": user_booker_api, "password": password_booker_api}
# Make authentication request to obtain token
auth_response = requests.post(f"{url_booker}/auth", json=body_credential_booker)
auth_response_data = auth_response.json()

if auth_response.status_code == 200:
    obtained_token = auth_response_data.get("token")
    if obtained_token:
        # Set token as environment variable
        os.environ["token"] = obtained_token
    else:
        LOGGER.error("Token not found in authentication response.")
else:
    LOGGER.error(
        "Authentication failed with status code: %s", auth_response.status_code
    )

# Now you can retrieve the token using os.getenv("token")
token_booker_api = os.getenv("token")
if not token_booker_api:
    LOGGER.warning("Token not found in environment variables.")

# Update headers with token
if token_booker_api:
    headers_booker["Cookie"] = f"token={token_booker_api}"
else:
    LOGGER.warning("Token is missing, Authorization header will not be set.")

LOGGER.debug("Token %s", token_booker_api)
