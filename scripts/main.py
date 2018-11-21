import logging
import yaml
from sys import stdout
from bf import BF
from MailJet import MailJet
from datetime import datetime

# Load configuration file
with open('../config.yml', 'r') as f:
    config = yaml.load(f)

# Store config values as variables
log_dir = config['logging']['log_dir']
log_level = logging.getLevelName(config['logging']['log_level'])
log_format = '%(levelname)s %(asctime)s %(module)s - %(message)s'
log_name = "log_%s.txt" % datetime.now().strftime("%Y-%m-%d--%H-%M-%S")

# Configure and start logger
logging.basicConfig(
    filename=log_dir + log_name,
    level=log_level,
    format=log_format,
    filemode='w+'
)
logger = logging.getLogger()
stream = logging.StreamHandler(stdout)
logger.addHandler(stream)

# Start program
logger.info('Program started')
try:
    data = BF(
        login=True,
        detail=True,
        username=config['bf']['username'],
        password=config['bf']['password']
    )
    MailJet().send_update(data.get_relevant_data())
    print(data.get_relevant_data())
except Exception as e:
    logging.exception(e)
