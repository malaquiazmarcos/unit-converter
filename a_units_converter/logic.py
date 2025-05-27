"""
logic.py

This module contains all functions logic for the API unit converter, 
from the convert to show relevant information.

Imports: 
    - data_validate: Validation decorator to check input data.
""" 
from a_units_converter.utils.validations import data_validate

@data_validate
def temperature_converter(units_data, value, unit_type, unit_from, unit_to):
    """
    Special function to convert no linear magnitude when temperature.

    Args: 
        value (int, float): Value to user wanted convert.
        unit_type (str): Magnitude input for the user to search data.
        unit_from (str): Abbreviation of the units name input for user (e.g. 'MB', 'mm', etc.).
        unit_to (str): Abbreviation of the desired unit for user (e.g. 'MB', 'mm', etc.).
        units_data (dict): Dictionary with all unit data.

    Returns:
        dict: A dictionary with all data input for the user.
            (e.g. 
                {"value": 1.0, "unit_type": "temperature", "unit_from": "C", "unit_to": "K", "result": 274.15}
            )
        
    Raises: 
        ValueError: If user input not a number.
        KeyError: 'unit_type' not in API data.
        ValueError: When unit input for user not belong to unit type.
        ZeroDivisionError: Zero Division.
        Exception: Unexpected error.
    """
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
    
    except ZeroDivisionError: 
        raise ZeroDivisionError('Not possible zero division.')
    except Exception as e:
        raise Exception('Unexpected error in unit convert') from e

@data_validate
def units_converter(units_data, value, unit_type, unit_from, unit_to):
    """
    Main function and logic of the API.

    Args: 
        value (int, float): Value to user wanted convert.
        unit_type (str): Magnitude input for the user to search data.
        unit_from (str): Abbrevation of the units name input for user (e.g. 'MB', 'mm', etc.).
        unit_to (str): Abbreviation of the desired unit for user (e.g. 'MB', 'mm', etc.).
        units_data (dict): Dictionary with all unit data.

    Returns:
        dict: A dictionary with all data input for the user.
            (e.g. 
                {"value": 1.0, "unit_type": "data", "unit_from": "GiB", "unit_to": "MiB", "result": 1024.0}
            )
        
    Raises: 
        ValueError: If user input not a number.
        KeyError: 'unit_type' not in API data.
        ValueError: When unit input for user not belong to unit type.
        ZeroDivisionError: Zero Division.
        Exception: Unexpected error.
    """

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

@data_validate
def all_data(units_data):
    """
    Returns all data.

    Args: 
        units_data (dict): Dictionary with all unit data.

    Returns:
        dict: Dictionary with several sub dicionaries.
            (e.g. 
                {'length': {'mm': {"name": "nanomolar",
                                "symbol": "nM",
                                "factor": 1e-9,
                                "system": "Chemistry",
                                "description": "Trace concentration (1 nM = 10⁻⁹ M)."}, 
                            ...}, 
                ...})
    """
    return units_data

@data_validate
def units_available(units_data):  # want convert to the units e.g. um => micro or explain in documentation
    """
    Returns all units available in the API.

    Args: 
        units_data (dict): Dictionary with all unit data.

    Returns:
        dict: A dictionary with magnitudes (key) and their respective units in a list (value).
            (e.g. {'length': ['mm', 'cm', ..], 'data': ['MB', 'GB', ...], ...})

    Raises:
        TypeError: If 'units_data' is an invalid structure.
    """    
    try: 
        dict_only_units = {}
        for magnitude, units in units_data.items():
            dict_only_units[magnitude] = list(units.keys())

        return dict_only_units
    except AttributeError as e:
        raise TypeError('Invalid data structure in unit definitions') from e

@data_validate
def short_description_unit(units_data, unit_type, unit):
    """
    Returns a short description of one unit wanted for the user.

    Args:
        units_data (dict): Dictionary with all unit data.
        unit_type (str): Magnitude input for the user to search data.
        unit (str): Abbrevation of the units name (e.g. 'MB', 'mm', etc.).

    Returns: 
        dict: Contains a dictionary with the unit (key) and description (value).
            (e.g. {"MB": "Common file size unit (1 MB = 1,000,000 bytes). Used for storage devices."})

    Raises: 
        TypeError: If 'units_data' is an invalid structure.
    """
    if not (unit_type and unit): 
        raise ValueError('The data of API is not available.')
    
    try: 
        return {unit: units_data[unit_type][unit]['description']}
    
    except AttributeError as e:
        raise TypeError('Invalid data structure in unit definitions') from e
    
@data_validate
def magnitudes(units_data):
    """
    Returns all magnitudes available.

    Args:
        units_data (dict): Dictionary with all unit data.

    Returns:
        dict: A dictionary with one key (magnitude) and one list with all magnitudes.
            (e.g. {'magnitudes': ['length', 'temperature', ...]})

    Raises:
        TypeError: If 'units_data' is an invalid structure.
    """
    try: 
        return {'magnitudes': list(units_data.keys())}

    except Exception as e: 
        raise TypeError('Invalid data structure in unit definitions') from e

@data_validate
def all_fullname_units_available(units_data):
    """
    Returns all full names of the units available in the API.

    Args:
        units_data (dict): Dictionary with all unit data.

    Returns:
        dict: A dictionary contains the name of magnitude (key) and list with the name of units (value).
            (e.g. { 'length': ['milimeter', 'centimeter', ...], 'temperature': ['celcius', 'kelvin', ...], ... }) 

    Raises:
        TypeError: If 'units_data' is an invalid structure.
    """
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
    
@data_validate
def fullname_units_available(units_data, unit_type):
    """
    Returns the full name of units for specific magnitude. 

    Args:
        units_data (dict): Dictionary with all unit data.
        unit_type (str): Magnitude input for the user to search data.

    Returns:
        dict: Dictionary with data wanted for the user.
            (e.g. {'data': 'MB', 'GB', 'TB'})

    Raises:
        KeyError: If 'unit_type' not in units_data.
        TypeError: If 'units_data' is an invalid structure.
    """
    if unit_type not in units_data:
        raise KeyError(f'Unit type "{unit_type}" not found in available data')
    
    try: 
        list_fullnames = []
        for units in units_data[unit_type].values():
            list_fullnames.append(units['name'])

        return {unit_type: list_fullnames}
    
    except AttributeError as e:
        raise TypeError('Invalid data structure in unit definitions') from e
    




    
