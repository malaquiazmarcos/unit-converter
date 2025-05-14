"""
logic.py

This module contains all functions logic for the API unit converter, 
from the convert to show relevant information.

Functions:
- data_validate: Analyzes exceptions of main data.
- temperature_converter: Special logic for non-linear units to convert.
- units_converter: All lineal units to convert.
- all_data: Returns all data.
- short_description_unit: Returns a short description of unit wanted.
- magnitudes: Returns all magnitudes.
- all_fullname_units_available: Returns all full name units.
- fullname_units_available: Returns full name only unit of user wanted.
"""

def data_validate(units_data):
    """
    Handler exeptions for low repeat code in functions
    """
    if not units_data:
        raise ValueError('The API data is not available or empty')
    
    if not isinstance(units_data, dict):
        raise TypeError('Expected a dictionary for data_units')
    
    return units_data

def temperature_converter(value, unit_type, unit_from, unit_to, units_data):
    units_data = data_validate(units_data)

    if not isinstance(value, (int, float)):
        raise ValueError("Value must be a number")

    if unit_type not in units_data:
        raise KeyError(f'Unit type "{unit_type}" not found in available data')

    if unit_from not in units_data[unit_type] or unit_to not in units_data[unit_type]:
        raise ValueError(f'Unit {unit_from} or {unit_to} not valid in {unit_type}')
    
    try:
        if unit_from == 'F':
            to_kelvin = (value - 32) * (5/9) + 273.15
        elif unit_from == 'C':
            to_kelvin = value + 273.15
        else:
            to_kelvin = value
        if unit_to == 'F':
            result = (to_kelvin - 273.15) * (9/5) + 32
        elif unit_to == 'C':
            result = value - 273.15
        else:
            result = to_kelvin
        
        return result

    except Exception as e:
        raise Exception('Unexpected error in unit convert') from e

def units_converter(value, unit_type, unit_from, unit_to, units_data):
    units_data = data_validate(units_data)

    if not isinstance(value, (int, float)):
        raise ValueError("Value must be a number")

    if unit_type not in units_data:
        raise KeyError(f'Unit type "{unit_type}" not found in available data')

    if unit_from not in units_data[unit_type] or unit_to not in units_data[unit_type]:
        raise ValueError(f'Unit {unit_from} or {unit_to} not valid in {unit_type}')

    try: 
        unit_1 = units_data[unit_type][unit_from]['factor']
        unit_2 = units_data[unit_type][unit_to]['factor']

        to_byte = value * unit_1
        result = to_byte / unit_2

        return result
    
    except ZeroDivisionError: 
        raise ZeroDivisionError('Not possible zero division.')
    except Exception as e:
        raise Exception('Unexpected error in unit convert') from e

def all_data(units_data):
    """
    Show all data.
    """
    return data_validate(units_data)

def units_available(units_data):  # want convert to the units e.g. um => micro
    units_data = data_validate(units_data)
    
    try: 
        dict_only_units = {}
        for magnitude, units in units_data.items():
            dict_only_units[magnitude] = list(units.keys())

        return dict_only_units
    except AttributeError as e:
        raise TypeError('Error in the data') from e

def short_description_unit(units_data, unit_type, unit):
    units_data = data_validate(units_data)

    if not (unit_type and unit): 
        raise ValueError('The data of API is not available.')
    
    try: 
        return {unit: units_data[unit_type][unit]['description']}
    
    except AttributeError as e:
        raise TypeError('Invalid data structure in unit definitions') from e
    
def magnitudes(units_data):
    """
    Show all magnitudes available.
    """
    units_data = data_validate(units_data)

    try: 
        return {'magnitudes': list(units_data.keys())}

    except Exception as e: 
        raise TypeError('Invalid data structure in unit definitions') from e

    
def all_fullname_units_available(units_data):
    units_data = data_validate(units_data)
    try: 
        dict_only_units = {}

        for magnitude, data in units_data.items():
            list_fullnames = []
            for name in data.values():
                list_fullnames.append(name['name'])
            dict_only_units[magnitude] = list_fullnames

        return dict_only_units
    except AttributeError as e:
        raise TypeError('Invalid data structure in unit definitions') from e
    
def fullname_units_available(units_data, unit_type):
    """
    All fullnames of one wanted magnitude.
    """
    """ if not data_units:
        raise ValueError('The API data is not available or empty')
    
    if not isinstance(data_units, dict):
        raise TypeError('Expected a dictionary for data_units') """
    
    units_data = data_validate(units_data)
    
    if unit_type not in units_data:
        raise KeyError(f'Unit type "{unit_type}" not found in available data')
    
    try: 
        list_fullnames = []
        for units in units_data[unit_type].values():
            list_fullnames.append(units['name'])

        return {unit_type: list_fullnames}
    
    except AttributeError as e:
        raise TypeError('Invalid data structure in unit definitions') from e
    




    
