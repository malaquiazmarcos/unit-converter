
def temperature_converter(value, unit_type, unit_from, unit_to, units_data):

    if unit_from not in units_data[unit_type] or unit_to not in units_data[unit_type]:
        return f'Unit {unit_from} or {unit_to} is not valid in {unit_type}.'
    
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
        print(f'ERROR: {e}')

def units_converter(value, unit_type, unit_from, unit_to, units_data):
    if unit_from not in units_data[unit_type] or unit_to not in units_data[unit_type]:
        return f'Unit {unit_from} or {unit_to} is not valid in {unit_type}.'

    try: 
        unit_1 = units_data[unit_type][unit_from]['factor']
        unit_2 = units_data[unit_type][unit_to]['factor']

        to_byte = value * unit_1

        try:
            result = to_byte / unit_2
        except ZeroDivisionError: 
            print('Not possible, zero division')

        return result

    except Exception as e:
        print(f'ERROR: {e}')

def all_data(data_units):
    """
    Show all data.
    """
    if not data_units:
        raise ValueError('The data of API is not available.')
    
    try: 
        all_data_1 = data_units

        return all_data_1
    except AttributeError as e:
        raise TypeError('Error in the data') from e

def units_available(data_units):
    if not data_units:
        raise ValueError('The data of API is not available.')
    
    try: 
        dict_only_units = {}
        for magnitude, units in data_units.items():
            dict_only_units[magnitude] = list(units.keys())

        return dict_only_units
    except AttributeError as e:
        raise TypeError('Error in the data') from e

def short_description_unit(data_units, unit_type, unit):
    if not (data_units and unit_type and unit): 
        raise ValueError('The data of API is not available.')
    try: 
        return {unit: data_units[unit_type][unit]['description']}
    
    except AttributeError as e:
        raise TypeError('Error in the data') from e
    
def magnitudes(data_units):
    """
    Show all magnitudes available.
    """
    if not isinstance(data_units, dict) or not data_units:
        raise ValueError('Invalid or empty data provided.')

    try: 
        return {'magnitudes': list(data_units.keys())}

    except Exception as e: 
        raise TypeError('Error in the data.') from e

    
def all_fullname_units_available(data_units):
    if not data_units:
        raise ValueError('The data of API is not available.')
    
    try: 
        dict_only_units = {}

        for magnitude, data in data_units.items():
            list_fullnames = []
            for name in data.values():
                list_fullnames.append(name['name'])
            dict_only_units[magnitude] = list_fullnames

        return dict_only_units
    except AttributeError as e:
        raise TypeError('Error in the data') from e
    
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