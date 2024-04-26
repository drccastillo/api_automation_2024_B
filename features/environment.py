"""
Module to setup and teardown test environment
"""
from __future__ import annotations

import logging

from entities.booking import Booking
from entities.branding import Branding
from entities.message import Message
from entities.report import Report
from entities.room import Room
from helpers.rest_client import RestClient
from helpers.validate_response import ValidateResponse
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


def before_all(context):
    """
    Setup test environment
    :param context: context instance
    """
    LOGGER.info('BEFORE ALL: Setup test environment')
    context.rest_client = RestClient()
    context.validate = ValidateResponse()
    context.room = Room()
    context.booking = Booking()
    context.report = Report()
    context.message = Message()
    context.branding = Branding()

    context.resource_list = {
        'room': [],
        'booking': [],
        'message': [],
    }


def before_feature(_context, feature):
    """
    Setup feature
    :param context: context instance
    :param feature: Feature instance
    """
    LOGGER.info('BEFORE FEATURE: %s', feature.name)
    LOGGER.info('Feature tags: %s', feature.tags)


def before_scenario(context, scenario):
    """
    Setup scenario
    :param context: context instance
    :param scenario: Scenario instance
    """
    LOGGER.info('BEFORE SCENARIO: %s', scenario.name)
    LOGGER.debug('Scenario tags: %s', scenario.tags)

    if 'room_id' in scenario.effective_tags:
        room = context.room.create_room()
        context.room_id = room['json']['roomid']
        context.resource_list['room'].append(context.room_id)
        context.param_id = context.room_id

        LOGGER.debug('Room ID created in before scenario : %s', context.room_id)

    elif 'booking_id' in scenario.effective_tags:
        room = context.room.create_room()
        context.room_id = room['json']['roomid']
        booking = context.booking.create_booking(room_id=context.room_id)
        context.booking_id = booking['json']['bookingid']
        context.param_id = context.booking_id

        context.resource_list['room'].append(context.room_id)
        context.resource_list['booking'].append(context.booking_id)
        LOGGER.debug('Room ID created in before scenario : %s', context.room_id)
        LOGGER.debug('Booking ID created in before scenario : %s', context.booking_id)

    elif 'message_id' in scenario.effective_tags:
        message = context.message.create_message()
        context.message_id = message['json']['messageid']
        context.resource_list['message'].append(context.message_id)
        context.param_id = context.message_id

        LOGGER.debug('Message ID created in before scenario : %s', context.message_id)


def after_scenario(_context, scenario):
    """
    Teardown scenario
    :param context: context instance
    :param scenario: Scenario instance
    """
    LOGGER.info('AFTER SCENARIO: %s', scenario.name)


def after_feature(context, feature):
    """
    Teardown feature
    :param context:
    :param feature: Feature instance
    """
    LOGGER.info('AFTER FEATURE: %s', feature.name)
    delete_resources(context)


def after_all(_context):
    """
    Teardown test environment
    :param context:
    """
    LOGGER.info('AFTER ALL: Tear down test environment')


def delete_resources(context):
    """
    Method to delete resources created during the test
    :param context: context instance
    """
    LOGGER.debug('Delete Resources...')
    for resource in context.resource_list:
        for resource_id in context.resource_list[resource]:
            method = getattr(getattr(context, resource), f'delete_{resource}')
            response = method(resource_id)
            if response['status_code'] == 202:
                LOGGER.debug('Deleting %s with id: %s', resource, resource_id)
