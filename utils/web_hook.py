import argparse
import logging
import pymsteams
import os

from config.config import WEB_HOOK
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

class Webhook:
    def __init__(self, webhook_url):
        self.team_message = pymsteams.connectorcard(webhook_url)

    def read_report(self, report_path):
        if os.path.exists(report_path):
            with open(report_path, "r") as report:
                report_message = report.read()
            return report_message
        else:
            LOGGER.error(f"{report_path} does not exist")
            raise FileNotFoundError(f"{report_path} does not exist")

    def send_message(self, message):
        self.team_message.text(message)
        try:
            self.team_message.send()
        except pymsteams.TeamsWebhookException as e:
            LOGGER.error(f"Failed to send message: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send a report via webhook.')
    parser.add_argument('module', type=str, help='The module to send the report for.')
    args = parser.parse_args()

    webhook = Webhook(WEB_HOOK)
    report_message = webhook.read_report(f"reports/markdown/md_report_{args.module}.md")
    webhook.send_message(report_message)