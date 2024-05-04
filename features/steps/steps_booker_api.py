"""
Module to define the steps for the Booker API.
"""
from __future__ import annotations

import logging

from behave import then  # type: ignore # pylint: disable=no-name-in-module
from behave import when  # type: ignore # pylint: disable=no-name-in-module

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@when('I call to "{endpoint}" endpoint using "GET" method and without body')
def call_get_endpoint(context, endpoint):
    """
    Step to call to an endpoint using GET method and without body.
    :param context: Context object.
    :param endpoint: Endpoint to call.
    """
    LOGGER.debug(
        "STEP: When I call to %s endpoint using 'GET' method and without body",
        endpoint,
    )

    endpoint_name = getattr(context, endpoint)
    if context.param_list[endpoint] is not None:
        method = getattr(endpoint_name, f'specific_{endpoint}')
        endpoint_id = context.param_list[endpoint]
        response = method(endpoint_id)
    else:
        method = getattr(endpoint_name, f'all_{endpoint}s')
        response = method()

    context.response = response
    context.endpoint = endpoint

    LOGGER.debug('Response: %s', context.response)
    LOGGER.debug('Enpoint: %s', context.endpoint)


def get_data_by_feature(context, method_name, endpoint):
    """
    Function to get data by feature.
    :param context: Context object.
    :param method_name: Method name.
    :param endpoint: Endpoint to call.
    """
    endpoint_obj = getattr(context, endpoint)
    if method_name == 'GET':
        if hasattr(context, context.param_list[endpoint]):
            method = getattr(endpoint_obj, f'specific_{endpoint}')
            response = method(context.param_list[endpoint])
        else:
            method = getattr(endpoint_obj, f'all_{endpoint}s')
            response = method()
    elif method_name == 'POST':
        method = getattr(endpoint_obj, f'create_{endpoint}')
        if hasattr(context, context.param_list[endpoint]):
            body = endpoint_obj.generate_data(context.param_list[endpoint])
        else:
            body = endpoint_obj.generate_data()
    elif method_name == 'PUT':
        method = getattr(endpoint_obj, f'update_{endpoint}')
        if hasattr(context, 'param_list') and endpoint in context.param_list:
            body = endpoint_obj.generate_data()

        response = method(body=body)
        context.resource_list[endpoint].append(response['json'][f'{endpoint}id'])

    if hasattr(context, 'param_id'):
        method = getattr(endpoint_obj, f'specific_{endpoint}')
        endpoint_id = context.param_id
        response = method(endpoint_id)
    else:
        method = getattr(endpoint_obj, f'all_{endpoint}s')
        response = method()


@when('I call to "{endpoint}" endpoint using "POST" method and with body')
def call_post_endpoint(context, endpoint):
    """
    Step to call to an endpoint using POST method and with body.
    :param context: Context object.
    :param endpoint: Endpoint to call.
    """
    LOGGER.debug(
        "STEP: When I call to %s endpoint using 'POST' method and with body",
        endpoint,
    )

    endpoint_name = getattr(context, endpoint)
    method = getattr(endpoint_name, f'create_{endpoint}')

    body = (
        endpoint_name.generate_data()
        if endpoint == 'room'
        else endpoint_name.generate_data(context.room_id)
    )
    response = method(body=body)

    context.response = response
    context.endpoint = endpoint
    context.resource_list[endpoint].append(response['json'][f'{endpoint}id'])

    LOGGER.debug('Response: %s', context.response)
    LOGGER.debug('Enpoint: %s', context.endpoint)
    LOGGER.debug('Resource list: %s', context.resource_list[endpoint])


@when('I call to "{endpoint}" endpoint using "PUT" method and with body')
def call_put_endpoint(context, endpoint):
    """
    Step to call to an endpoint using PUT method and with body.
    :param context: Context object.
    :param endpoint: Endpoint to call.
    """
    LOGGER.debug(
        "STEP: When I call to %s endpoint using 'PUT' method and with body",
        endpoint,
    )

    endpoint_name = getattr(context, endpoint)
    method = getattr(endpoint_name, f'update_{endpoint}')
    endpoint_id = context.param_list[endpoint]

    body = (
        endpoint_name.generate_data()
        if endpoint != 'booking'
        else endpoint_name.generate_data(context.room_id)
    )
    if endpoint_id is None:
        response = method(body=body)
    else:
        response = method(endpoint_id, body)

    context.response = response
    context.endpoint = endpoint

    LOGGER.debug('Response: %s', context.response)
    LOGGER.debug('Enpoint: %s', context.endpoint)


@when('I call to "{endpoint}" endpoint using "DELETE" method and without body')
def call_delete_endpoint(context, endpoint):
    """
    Step to call to an endpoint using DELETE method and without body.
    :param context: Context object.
    :param endpoint: Endpoint to call.
    """
    LOGGER.debug(
        "STEP: When I call to %s endpoint using 'DELETE' method and without body",
        endpoint,
    )

    endpoint_name = getattr(context, endpoint)
    method = getattr(endpoint_name, f'delete_{endpoint}')
    endpoint_id = getattr(context, f'{endpoint}_id')

    response = method(endpoint_id)

    context.response = response
    context.endpoint = endpoint

    LOGGER.debug('Response: %s', context.response)
    LOGGER.debug('Enpoint: %s', context.endpoint)


@then('I receive the response and validate using "{json_file}" json')
def receive_response(context, json_file):
    """
    Step to validate the response using a json file.
    :param context: Context object.
    :param json_file: Json file to validate.
    """
    LOGGER.debug(
        'STEP: Then I receive the response and validate using %s json',
        json_file,
    )
    context.validate.validate_response(
        actual_response=context.response,
        endpoint=context.endpoint,
        file_name=json_file,
    )
