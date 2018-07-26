import sqlite3
import yaml
import os
import logging
import datetime
from sys import stdout


# Load config file
with open('config.yml', 'r') as f:
    config = yaml.load(f)

# Get some basic config data
log_level = logging.getLevelName(config['logging']['log_level'])
log_format = '%(levelname)s %(asctime)s %(module)s - %(message)s'
log_name = "installation_log_%s.txt" % datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
log_dir = config['logging']['log_dir']
log_abspath = os.path.abspath(log_dir)
log_dir_exists = os.path.exists(log_dir)

# Check existence of log directory and store data before logging
if log_dir_exists:
     log_dir_message = 'Using existing log directory: %s' % log_abspath
else:
    log_dir_message = 'Could not find specified log directory. Creating a directory: %s' % log_abspath
    os.makedirs(log_dir)

# Initialize logger
logging.basicConfig(filename=log_dir + log_name,
                    level=log_level,
                    format=log_format,
                    filemode='w+')
logger = logging.getLogger()
stream = logging.StreamHandler(stdout)
logger.addHandler(stream)

# Setup data directory
data_dir = config['data']['dir']
data_abspath = os.path.abspath(data_dir)
if os.path.exists(data_dir):
    logger.info('Using existing data directory: %s' % data_abspath)
else:
    logger.info('Could not find specified data directory. Creating a directory: %s' % data_abspath)
    os.makedirs(data_dir)


# Setup sqlite
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


if __name__ == '__main__':
    create_connection(os.path.join(data_dir, config['data']['db_name']))

