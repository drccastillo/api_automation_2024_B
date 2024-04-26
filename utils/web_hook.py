"""
This module is used to send a report via webhook.
"""
from __future__ import annotations

import argparse
import logging
import os

import pymsteams

from config.config import WEB_HOOK
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Webhook:
    """
    Class to send a report via webhook
    """

    def __init__(self, webhook_url):
        """
        Initialize the Webhook class
        :param webhook_url: webhook URL
        """
        self.team_message = pymsteams.connectorcard(webhook_url)

    def read_report(self, report_path):
        """
        Read the report from the file
        :param report_path: path of the report
        :return: report message
        """
        if os.path.exists(report_path):
            with open(report_path, encoding="utf-8") as report:
                report_content = report.read()
            return report_content
        LOGGER.error("%s does not exist", report_path)
        raise FileNotFoundError(f"{report_path} does not exist")

    def send_message(self, message):
        """
        Send the message via webhook
        :param message: message to send
        """
        self.team_message.text(message)
        try:
            self.team_message.send()
        except pymsteams.TeamsWebhookException as e:
            LOGGER.error("Failed to send message: %s", e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a report via webhook.")
    parser.add_argument("module", type=str, help="The module to send the report for.")
    args = parser.parse_args()

    webhook = Webhook(WEB_HOOK)
    report_message = webhook.read_report(f"reports/markdown/md_report_{args.module}.md")
    webhook.send_message(report_message)
