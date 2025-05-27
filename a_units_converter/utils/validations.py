
def data_validate(func):
    """
    Handler exeptions for not repeat code in functions.

    This decorator verify the parameter was a dictionary and 
    not not empty or data is available.

    Args:
        func (function): Function to decorate.

    Returns:
        function: decorate function with add validate.

    Raises:
        ValueError: If parameter not exists.
        TypeError: If input parameter not a dict.
    """
    def wrapper(units_data, *args, **kwargs):
        if not units_data:
            raise ValueError('The API data is not available or empty')
        if not isinstance(units_data, dict):
            raise TypeError('Expected a dictionary for data_units')
        return func(units_data, *args, **kwargs)
    return wrapper



def data_validate_no(units_data):
    """
    Handler exeptions for not repeat code in functions.

    This function verify the parameter was a dictionary and 
    not not empty or data is available.

    Args:
        units_data (dict): All data.

    Returns:
        units_data (dict): equal data verified with exceptions.

    Raises:
        ValueError: If parameter not exists.
        TypeError: If input parameter not a dict.
    """
    """ if not units_data:
        raise ValueError('The API data is not available or empty')
    
    if not isinstance(units_data, dict):
        raise TypeError('Expected a dictionary for data_units')
    
    return units_data """
