import datetime
import smtplib
import yaml
import logging

# Initialize logger
logger = logging.getLogger(__name__)


class Gmail:
    """Class for sending Bostadsförmedlingen data via gmail"""

    def __init__(self):
        # Load configuration file
        with open('config.yml', 'r') as f:
            config = yaml.load(f)
        # Store basic data
        self.email = config['mail']['email']
        pw = config['mail']['password']
        logger.info('Attempting to authenticate to smtp client...')
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.server.ehlo()
        self.server.login(self.email, pw)
        logger.info('Authentication successful')

    def send_new(self, data):
        title = ''

