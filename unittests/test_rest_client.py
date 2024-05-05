"""
Module to test the rest client helper
"""
from __future__ import annotations

import logging
import unittest

from helpers.rest_client import RestClient
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


class TestRestClient(unittest.TestCase):
    """
    Test class for RestClient
    """

    def test_singleton(self):
        """
        Test that the RestClient is a singleton
        """
        LOGGER.info('Test RestClient singleton')
        instances = [RestClient() for _ in range(3)]

        # Check if all instances are the same
        for i, instance_i in enumerate(instances):
            for j, instance_j in enumerate(instances[i + 1 :], start=i + 1):
                if instance_i is not instance_j:
                    LOGGER.debug(
                        "The instance %s isn't the same that the instance %s",
                        i,
                        j,
                    )
                    LOGGER.error('Instances are not the same')
                    assert False
                else:
                    LOGGER.debug(
                        'The instance %s is the same that the instance %s',
                        i,
                        j,
                    )

        LOGGER.info('All instances are the same')


if __name__ == '__main__':
    unittest.main()
