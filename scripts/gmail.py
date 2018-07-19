import datetime
import smtplib
import yaml
import logging

# Initialize logger
logger = logging.getLogger(__name__)


class Gmail:
    """Class for sending Bostadsförmedlingen data via gmail"""

    def __init__(self):

#Load configuration file
        with open('config.yml', 'r') as f:
            config = yaml.load(f)

        self.email = config['mail']['email']
        pw = config['mail']['password']
