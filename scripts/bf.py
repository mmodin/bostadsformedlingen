import requests
import pandas as pd
import logging
import datetime
import os
from collections import MutableMapping

logger = logging.getLogger(__name__)


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = '{0}{1}{2}'.format(parent_key, sep, k) if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # apply itself to each element of the list - that's it!
            items.append((new_key, list(map(flatten, v))))
        else:
            items.append((new_key, v))
    return dict(items)


def flatten_municipality(area_list):
    tmp = []
    for d in area_list:
        for l in d['Stadsdelar']:
            tmp.append({'municipality': d['Kommun'], 'district': l})

    return tmp


class BF:
    """ Class to get all apartment listings from Stockholms Bostadsförmedling """

    # To do
    # Add getting detailed data in init
    # Parse page
    # Add link to listing in table (url + one of the columns, which?)

    def __init__(self, username, password, login=False):
        from bf_data import column_names, fields, municipalities, types, districts
        self.url = 'https://bostad.stockholm.se'
        self.column_names = column_names
        self.fields = fields
        self.municipalities = municipalities
        self.types = types
        self.districts = districts
        self.data_dir = '../data/latest.pkl'
        self.login = login
        self.session = requests.Session()


        if self.login:
            response = self.session.get(self.url + '/Minasidor/login/')
            logger.info('Getting login cookie...status code: %s' % response.status_code)
            url = 'https://login001.stockholm.se/siteminderagent/forms/login.fcc'
            data = {
                'target': '-SM-https://bostad.stockholm.se/secure/login',
                'smauthreason': '0',
                'smagentname': 'bostad.stockholm.se',
                'USER': username,
                'PASSWORD': password
            }
            response = self.session.post(url, data=data)
            if response.status_code == 200:
                logger.info('Successfully logged in...')
            else:
                logger.error('Failed logging in with status code: %s' % response.status_code)
                raise Exception('Login error')

        response = self.session.get(self.url + '/Lista/AllaAnnonser')
        if response.status_code == 200:
            data = response.json()
            self.all_listings = pd.DataFrame([flatten(d) for d in data])
            self.swedish_column_names = self.all_listings.columns
            self.all_listings.columns = column_names
            logger.info('Successfully downloaded %s listings...' % self.all_listings.shape[0])
        else:
            raise Exception('Unable to get all listings with status code: %s' % response.status_code)

        if os.path.exists(self.data_dir):
            df = pd.read_pickle(self.data_dir)
            old_ids = list(df.id)
            last_modified = datetime\
                .datetime\
                .fromtimestamp(os.path.getmtime(self.data_dir))\
                .strftime('%Y-%m-%d %H:%M:%S')
            logger.info('Found %s historical listings (last modified: %s)' %
                        (len(old_ids), last_modified))
        else:
            logger.info('No existing data file found...assuming that all listings are new')
            old_ids = []
            last_modified = '(NA - first time execution)'

        new_ids = list(self.all_listings.id)
        self.new_listing_ids = [x for x in new_ids if x not in old_ids]
        logger.info('Found %s new records since last execution: %s' %
                    (len(self.new_listing_ids), last_modified))

        self.all_listings.to_pickle(self.data_dir)
        logger.info('Successfully saved the latest data...')

        # make flexible to year?
        response = self.session.get(self.url + '/statistik/statistiktjansten/GetAreas?year=2018&queue=Bostadsk%C3%B6n')
        if response.status_code == 200:
            data = flatten_municipality(response.json())
            self.all_areas = pd.DataFrame(data)
            logger.info('Successfully downloaded all district and municipality data...')
        else:
            raise Exception('Unable to get municipality data with status code: %s' % response.status_code)

    def save_data(self, path):
        self.all_listings.to_csv(path, encoding='utf-8-sig', index=False, float_format='%g')

    # Extend below to use correct filters once source has been added
    def get_relevant_data(self):
        df = self.all_listings
        return df[self.fields][
            df.type.isin(self.types)
            & df.district.isin(self.districts)
            & df.canApply == self.login
        ]

    def get_new_listings(self):
        df = self.get_relevant_data()
        return df[df.id.isin(self.new_listing_ids)]
