import datetime
import logging
import yaml
from bf import BF
from gmail import Gmail

# Load configuration file
with open('config.yml', 'r') as f:
    config = yaml.load(f)

# Store config values as variables
log_dir = config['logging']['log_dir']
log_level = logging.getLevelName(config['logging']['log_level'])
log_format = '%(levelname)s %(asctime)s - %(message)s'
log_name = "log_%s.txt" % datetime.now().strftime("%Y-%m-%d--%H-%M-%S")

# Configure and start logger
logging.basicConfig(filename=log_dir + log_name,
                    level=log_level,
                    format=log_format,
                    filemode='w+')
logger = logging.getLogger()

# Start program
logger.info('Program started')

data = BF()
data.get_relevant_data()
data.all_areas








