column_names = [
            'id',
            'fromDate',
            'toDate',
            'numberOf',
            'rooms',
            'isLoggedIn',
            'balcony',
            'fastQueue',
            'externalQueue',
            'address',
            'hasApplied',
            'hasGoodChance',
            'hasInternalQueue',
            'elevator',
            'rent',
            'internalQueue',
            'canApply',
            'queue',
            'queueName',
            'municipality',
            'latitude',
            'longitude',
            'short-term',
            'type',
            'similarStats',
            'Q1',
            'Q3',
            'newlyBuilt',
            'area',
            'senior',
            'district',
            'student',
            'youth',
            'url',
            'floor',
            'normal',
            'sqm'
]

dtypes = {
    'id': 'int64',
    'fromDate': 'O',
    'toDate': 'O',
    'numberOf': 'int64',
    'rooms': 'int64',
    'isLoggedIn': 'bool',
    'balcony': 'bool',
    'fastQueue': 'bool',
    'externalQueue': 'bool',
    'address': 'O',
    'hasApplied': 'bool',
    'hasGoodChance': 'bool',
    'hasInternalQueue': 'bool',
    'elevator': 'bool',
    'rent': 'float64',
    'internalQueue': 'bool',
    'canApply': 'bool',
    'queue': 'O',
    'queueName': 'O',
    'municipality': 'O',
    'latitude': 'float64',
    'longitude': 'float64',
    'short-term': 'bool',
    'type': 'O',
    'similarStats': 'float64',
    'Q1': 'float64',
    'Q3': 'float64',
    'newlyBuilt': 'bool',
    'area': 'O',
    'senior': 'bool',
    'district': 'O',
    'student': 'bool',
    'youth': 'bool',
    'url': 'O',
    'floor': 'float64',
    'normal': 'bool',
    'sqm': 'float64'
}




# Filters (make these come from config file instead?
fields = ['id', 'district', 'municipality', 'sqm', 'rooms', 'type', 'rent',
          'Q3', 'fromDate', 'toDate']
municipalities = ['Stockholm']
districts = ['Nacka Strand', 'Sickla Strand', 'Södermalm', 'Johanneshov', 'Skeppsholmen',
             'Reimersholme', 'Äppelviken', 'Vasastaden', 'Östermalm', 'Kungsholmen',
             'Stadshagen', 'Årsta', 'Långholmen', 'Alvik', 'Aspudden', 'Gröndal',
             'Hammarbyhöjden', 'Gamla Stan', 'Ladugårdsgärdet', 'Kristineberg',
             'Norra Djurgården', 'Liljeholmen', 'Hjorthagen', 'Lilla Essingen',
             'Norrmalm', 'Södra Hammarbyhamnen', 'Fredhäll', 'Marieberg', 'Midsommarkransen'
             ]
types = ['Hyresrätt', 'Korttidskontrakt', 'Bostadssnabben']
