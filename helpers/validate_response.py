import json
import logging

from utils.logger import get_logger
from config.config import abs_path

LOGGER = get_logger(__name__, logging.DEBUG)


class ValidateResponse:
    def validate_response(self, actual_response=None, endpoint=None, file_name=None):
        """
        :param actual_response: response from the API
        :param endpoint: endpoint of the API
        """
        if actual_response is not None:
            # read from json file
            expected_response = self.read_input_data_json(
                f"{abs_path}/api/input_data/{endpoint}/{file_name}.json"
            )

            # compare actual and expected response
            # validate status_code
            self.validate_value(
                expected_response["status_code"],
                actual_response["status_code"],
                "status_code",
            )
            # validate headers
            self.validate_value(
                expected_response["headers"], actual_response["headers"], "headers"
            )
            # validate body
            self.validate_value(
                expected_response["response"]["body"], actual_response["json"], "body"
            )

    def validate_value(self, expected_value, actual_value, key_compare):
        """
        :param expected_value: expected value
        :param actual_value: actual value
        :param key_compare: key to compare
        """
        error_message = f"Expected value: {expected_value} but got: {actual_value}"
        LOGGER.debug("Expected value '%s': '%s'", key_compare, expected_value)
        LOGGER.debug("Actual value '%s': '%s'", key_compare, actual_value)
        if key_compare == "body":
            assert self.compare_json_keys(expected_value, actual_value), error_message
        elif key_compare == "headers":
            for header, expected_header_value in expected_value.items():
                if header == "Set-Cookie":
                    assert (
                        "Set-Cookie" in actual_value
                        and "token" in actual_value["Set-Cookie"]
                    ), error_message
                else:
                    assert (
                        header in actual_value
                        and expected_header_value == actual_value[header]
                    ), error_message
        else:
            assert expected_value == actual_value, error_message

    @staticmethod
    def read_input_data_json(file_name):
        LOGGER.debug("Reading input data from file: %s", file_name)
        with open(file_name, "r") as json_file:
            data = json.load(json_file)
        LOGGER.debug("Input data json: %s", data)
        json_file.close()
        return data

    @staticmethod
    def compare_json_keys(json1, json2):
        results = []

        if isinstance(json1, dict) and isinstance(json2, dict):
            for key in json1.keys():
                if key in json2.keys():
                    LOGGER.debug("Key '%s' found in json2", key)
                    results.append(
                        ValidateResponse.compare_json_keys(json1[key], json2[key])
                    )
                else:
                    LOGGER.debug("Key '%s' not found in json2", key)
                    results.append(False)
        elif isinstance(json1, list) and isinstance(json2, list):
            for item1, item2 in zip(json1, json2):
                results.append(ValidateResponse.compare_json_keys(item1, item2))
        else:
            results.append(True)

        return False not in results


if __name__ == "__main__":
    val = ValidateResponse()
    val.validate_response()
