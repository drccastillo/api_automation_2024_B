from __future__ import annotations

import logging

from behave import then
from behave import when

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@when('I call to "{endpoint}" endpoint using "GET" method and without body')
def call_get_endpoint(context, endpoint):
    LOGGER.debug(
        f"STEP: When I call to '{endpoint}' endpoint using 'GET' method and without body",
    )

    endpoint_name = getattr(context, endpoint)
    if hasattr(context, "param_id"):
        method = getattr(endpoint_name, f"specific_{endpoint}")
        endpoint_id = context.param_id
        response = method(endpoint_id)
    else:
        method = getattr(endpoint_name, f"all_{endpoint}s")
        response = method()

    context.response = response
    context.endpoint = endpoint

    LOGGER.debug("Response: ", context.response)
    LOGGER.debug("Enpoint: ", context.endpoint)


@when('I call to "{endpoint}" endpoint using "POST" method and with body')
def call_post_endpoint(context, endpoint):
    LOGGER.debug(
        f"STEP: When I call to '{endpoint}' endpoint using 'POST' method and with body",
    )

    endpoint_name = getattr(context, endpoint)
    method = getattr(endpoint_name, f"create_{endpoint}")

    data_generators = {
        "room": lambda: endpoint_name.generate_data(),
        "booking": lambda: endpoint_name.generate_data(context.room_id),
    }
    body = data_generators.get(endpoint, lambda: None)()
    response = method(body=body)

    context.response = response
    context.endpoint = endpoint
    context.resource_list[endpoint].append(response["json"][f"{endpoint}id"])

    LOGGER.debug("Response: %s", context.response)
    LOGGER.debug("Enpoint: %s", context.endpoint)
    LOGGER.debug("Resource list: %s", context.resource_list[endpoint])


@when('I call to "{endpoint}" endpoint using "PUT" method and with body')
def call_put_endpoint(context, endpoint):
    LOGGER.debug(
        f"STEP: When I call to '{endpoint}' endpoint using 'PUT' method and with body",
    )

    endpoint_name = getattr(context, endpoint)
    method = getattr(endpoint_name, f"update_{endpoint}")
    endpoint_id = context.param_id

    data_generators = {
        "room": lambda: endpoint_name.generate_data(),
        "booking": lambda: endpoint_name.generate_data(context.room_id),
    }

    body = data_generators.get(endpoint, lambda: None)()
    response = method(endpoint_id, body)

    context.response = response
    context.endpoint = endpoint

    LOGGER.debug("Response: ", context.response)
    LOGGER.debug("Enpoint: ", context.endpoint)


@when('I call to "{endpoint}" endpoint using "DELETE" method and without body')
def call_delete_endpoint(context, endpoint):
    LOGGER.debug(
        f"STEP: When I call to '{endpoint}' endpoint using 'DELETE' method and without body",
    )

    endpoint_name = getattr(context, endpoint)
    method = getattr(endpoint_name, f"delete_{endpoint}")
    endpoint_id = getattr(context, f"{endpoint}_id")

    response = method(endpoint_id)

    context.response = response
    context.endpoint = endpoint

    LOGGER.debug("Response: ", context.response)
    LOGGER.debug("Enpoint: ", context.endpoint)


@then('I receive the response and validate using "{json_file}" json')
def receive_response(context, json_file):
    LOGGER.debug(
        f"STEP: Then I receive the response and validate using '{json_file}' json",
    )
    context.validate.validate_response(
        actual_response=context.response,
        endpoint=context.endpoint,
        file_name=json_file,
    )
