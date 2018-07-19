import requests
import pandas as pd
import logging
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
    # Add getting list of municipalities in init
    # Add getting statistics in init
    # Add checking for existing data in init
    # Add method for checking new records

    def __init__(self):
        from bf_data import column_names, fields, municipalities, types
        self.url = 'https://bostad.stockholm.se'
        self.column_names = column_names
        self.fields = fields
        self.municipalities = municipalities
        self.types = types

        response = requests.get(self.url + '/Lista/AllaAnnonser')
        if response.status_code == 200:
            data = response.json()
            self.all_listings = pd.DataFrame([flatten(d) for d in data])
            self.swedish_column_names = self.all_listings.columns
            self.all_listings.columns = column_names
            logger.info('Successfully downloaded all listings...')
        else:
            raise Exception('Unable to get all listings with status code: %s' % response.status_code)

        response = requests.get(self.url + '/statistik/statistiktjansten/GetAreas?year=2017&queue=Bostadsk%C3%B6n')
        if response.status_code == 200:
            data = flatten_municipality(response.json())
            self.all_areas = pd.DataFrame(data)
            logger.info('Successfully downloaded all district and municipality data...')
        else:
            raise Exception('Unable to get municipality data with status code: %s' % response.status_code)

    def save_data(self, path):
        self.all_listings.to_csv(path, encoding='utf-8-sig', index=False)

    # Extend below to use correct filters once source has been added
    def get_relevant_data(self):
        df = self.all_listings
        return df[self.fields][
            df.type.isin(self.types)
            & df.municipality.isin(self.municipalities)
        ]
