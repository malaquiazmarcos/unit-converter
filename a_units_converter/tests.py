from django.test import TestCase

import json
from logic import *

with open("a_units_converter/data/units.json", "r") as units:
    data_units = json.load(units)

def fullname_units_available(data_units, unit_type):
    """
    All fullnames of one wanted magnitude.
    """
    if not data_units:
        raise ValueError('The data of API is not available.')
    
    try: 
        dict_only_units = {}
        list_fullnames = []

        for units in data_units[unit_type].values():
            list_fullnames.append(units['name'])
        
        dict_only_units[unit_type] = list_fullnames

        return dict_only_units
    except AttributeError as e:
        raise TypeError('Error in the data') from e
        


print(fullname_units_available(data_units, 'data'))
    




            




