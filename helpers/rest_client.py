import json
import logging
import requests
import requests.utils
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.config import DEFAULT_HEADERS
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class RestClient:
    def __init__(self, headers=DEFAULT_HEADERS, timeout=155, max_retries=135):
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.timeout = timeout

        # Setup retries
        retry_strategy = Retry(
            total=max_retries, status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def request(self, method_name, url, body=None):
        """
        Send a request to the server
        :param method_name: HTTP method name
        :param url: URL to send the request
        :param body: Request body
        :return: Response dictionary
        Returns a dictionary with the following keys
        - json: Response body
        - status_code: Response status code
        - headers: Response headers
        """
        response = None  # Initialize response
        response_dict = {}
        try:
            method_func = getattr(self.session, method_name)
            response = method_func(url=url, json=body, timeout=self.timeout)
            response.raise_for_status()
            response_dict.update({"json": self.get_json(response)})
        except requests.exceptions.HTTPError as http_err:
            LOGGER.error(f"HTTP error occurred: {http_err}")
            if response is not None:
                if response.text:
                    try:
                        response_dict["json"] = response.json()
                    except json.JSONDecodeError:
                        response_dict["json"] = {"msg": "No body content"}
                else:
                    response_dict["json"] = {"error": str(http_err)}
            else:
                response_dict["json"] = {"error": str(http_err)}
        except requests.exceptions.ConnectionError as conn_err:
            LOGGER.error(f"Error connecting: {conn_err}")
            response_dict["json"] = {"error": str(conn_err)}
        except requests.exceptions.Timeout as timeout_err:
            LOGGER.error(f"Timeout error: {timeout_err}")
            response_dict["json"] = {"error": str(timeout_err)}
        except requests.exceptions.RequestException as err:
            LOGGER.error(f"Error: {err}")
            response_dict["json"] = {"error": str(err)}
        finally:
            if response is not None:
                response_dict.update(
                    {
                        "status_code": response.status_code,
                        "headers": self.get_header(response),
                        "cookies": self.get_cookies(response),
                    }
                )
            else:
                response_dict.update(
                    {
                        "status_code": None,
                        "headers": {"msg": "No response headers"},
                        "cookies": {"msg": "No response content"},
                    }
                )
            LOGGER.debug("Status Code: %s", response_dict["status_code"])
            LOGGER.debug("Response headers: %s", response_dict["headers"])
            LOGGER.debug("Response Content: %s", response_dict["json"])
            LOGGER.debug("Response Cookies: %s", response_dict["cookies"])

        return response_dict

    @staticmethod
    def get_json(response):
        if response.text:
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"msg": response.text}
        else:
            return {"msg": "No body content"}

    @staticmethod
    def get_header(response):
        try:
            return response.headers
        except AttributeError:
            return {"msg": "No headers content"}

    @staticmethod
    def get_cookies(response):
        try:
            return requests.utils.dict_from_cookiejar(response.cookies)
        except AttributeError:
            return {"msg": "No cookies content"}
