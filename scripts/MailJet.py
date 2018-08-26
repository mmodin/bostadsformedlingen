import logging
import yaml
from mailjet_rest import Client
from datetime import datetime
from html_table import html_table

# Initialize logger
logger = logging.getLogger(__name__)


class MailJet:
    """Class for sending Bostadsförmedlingen data via MailJet"""

    def __init__(self):
        # Load config file
        with open('../config.yml', 'r') as f:
            config = yaml.load(f)
        # Store config data
        self.public_key = config['mail']['public_key']
        self.secret_key = config['mail']['secret_key']
        self.recipients = config['mail']['recipients']
        self.recipients = [{'Email': x} for x in config['mail']['recipients']]
        self.sender = config['mail']['sender']

        logger.info('Initializing mail client...')
        # Initialize the email client
        self.mailjet = Client(auth=(self.public_key, self.secret_key))

    def send_update(self, df):
        logger.info('Generating email template...')
        data = {
            'FromEmail': self.sender,
            'FromName': 'Apartment finder',
            'Subject': 'Daily Apartment Update (%s)' % datetime.now(),
            'Html-part': '<h3>Appartments currently listed: </h3><br /> %s <br />' % html_table(df),
            'Recipients': self.recipients
        }
        logger.info('Sending email...')
        result = self.mailjet.send.create(data=data)
        if result.status_code == 200:
            logger.info('Successfully sent email.')
            return result
        else:
            logger.error('Something went wrong while sending email...status code: %s', result.status_code)




