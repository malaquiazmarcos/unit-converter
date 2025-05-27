from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit
import json
import logging
from a_units_converter.logic import *
from a_units_converter.utils.active_ratelimit import active_ratelimit

logger = logging.getLogger(__name__)

with open("a_units_converter/data/units.json", "r", encoding='utf-8') as data:
    units_data = json.load(data)

@require_http_methods(['GET'])
@ratelimit(key='ip', rate='10/m', block=False)
@active_ratelimit
def unit_convert(request):
    """
    Convert units based on user input.

    See the documentation for more details.
    """
    value = (request.GET.get('value')) 
    unit_type = request.GET.get('unit_type')
    unit_from = request.GET.get('unit_from')
    unit_to = request.GET.get('unit_to')

    if not all([value, unit_type, unit_from, unit_to]):
        logger.warning('Error, data missing')
        return JsonResponse(
            {'error': 'Requested data missing'},
            status=400
        )
    
    try: 
        value = float(value)
    except (ValueError, TypeError) as e:
        logger.error(f'Invalid value for conversation: {value} - Error: {str(e)}')
        return JsonResponse(
            {'error': 'Value is not a valid number'}, 
            status=400
        )

    if unit_type not in units_data:
        logger.warning(f'Unit type not available: {unit_type}')
        return JsonResponse(
            {'error': 'Unit type not available'}, 
            status=400
        )

    try:
        if unit_type == 'temperature':
            result = temperature_converter(units_data, value, unit_type.lower(), unit_from, unit_to)
        else:
            result = units_converter(units_data, value, unit_type.lower(), unit_from, unit_to)

        if not result:
            logger.warning('Units data is not available')
            return JsonResponse(
                {'error': 'Requested data not found'}, 
                status=404
            )
        
        return JsonResponse({
            'value': value,
            'unit_type': unit_type,
            'unit_from': unit_from,
            'unit_to': unit_to,
            'result': result
        })
        
    except Exception as e:
        logger.error(f'Error in unit_convert: {str(e)}', exc_info=True)
        return JsonResponse(
            {'error': 'Internal server error'},
            status=500
        )

@require_http_methods(['GET'])
@ratelimit(key='ip', rate='10/m', block=False)
@active_ratelimit
def show_all_data(request):
    """
    Show all available unit data from the API.

    See the documentation for more details.
    """
    try:
        result = all_data(units_data)

        if not result:
            logger.warning('All data not available')
            return JsonResponse(
                {'error': 'Requested data not found'}, 
                status=404
            )
        return JsonResponse(result, status=200)
    
    except Exception as e:
        logger.error(f'Error in show_all_units: {str(e)}', exc_info=True)
        return JsonResponse(
            {'error': 'Internal server error'},
            status= 500
        )

@require_http_methods(['GET'])
@ratelimit(key='ip', rate='10/m', block=False)
@active_ratelimit
def show_units_available(request):
    """
    Returns all units available in the API.

    See the documentation for more details.
    """
    try:
        result = units_available(units_data)

        if not result:
            logger.warning('Units available data is not available')
            return JsonResponse(
                {'error': 'Requested data not found'}, 
                status=404
            )
        return JsonResponse(result, status=200)
    
    except Exception as e:
        logger.error(f'Error in show_units_available: {str(e)}', exc_info=True)
        return JsonResponse(
            {'error': 'Internal server error'},
            status=500
        )

@require_http_methods(['GET'])
@ratelimit(key='ip', rate='10/m', block=False)
@active_ratelimit
def show_short_description(request):
    """
    Returns a short description of one unit requested by the user.

    See the documentation for more details.
    """
    unit_type = request.GET.get('unit_type')
    unit = request.GET.get('unit')

    try: 
        result = short_description_unit(units_data, unit_type.lower(), unit)

        if not result:
            logger.warning('Description data not available')
            return JsonResponse(
                {'error': 'Requested data not found'}, 
                status=404
            )
        return JsonResponse(result, status=200)

    except Exception as e:
        logger.error(f'Error in show_short_description: {str(e)}', exc_info=True)
        return JsonResponse(
            {'error': 'Internal server error'},
            status=500
        )          

@require_http_methods(['GET'])
@ratelimit(key='ip', rate='10/m', block=False)
@active_ratelimit
def show_magnitudes(request):
    """
    Returns all magnitudes available in the API.

    See the documentation for more details.
    """
    try: 
        result = magnitudes(units_data)

        if not result:
            logger.warning('Magnitudes data not available')
            return JsonResponse(
                {'error': 'Requested data not found.'}, 
                status=404
            )
        return JsonResponse(result, status=200)
    
    except Exception as e:
        logger.error(f'Error in show_magnitudes: {str(e)}', exc_info=True)
        return JsonResponse(
            {'error': f'Internal server error'}, 
            status=500
        )
    
@require_http_methods(['GET'])
@ratelimit(key='ip', rate='10/m', block=False)
@active_ratelimit
def show_all_fullname(request):
    """
    Returns all full names of the units available in the API.

    See the documentation for more details.
    """
    try:
        result = all_fullname_units_available(units_data)

        if not result:
            logger.warning('All full name data not available')
            return JsonResponse(
                {'error': 'Requested data not found'}, 
                status=404
            )
        return JsonResponse(result, status=200)
    
    except Exception as e:
        logger.error(f'Error in show_all_fullname: {str(e)}', exc_info=True)
        return JsonResponse(
            {'error': f'Internal server error'}, 
            status=500
        )

@require_http_methods(['GET'])
@ratelimit(key='ip', rate='10/m', block=False)
@active_ratelimit
def fullname_wanted_units(request):
    """
    Returns the full name of units for a specific magnitude.

    See the documentation for more details.
    """
    unit_type = request.GET.get('unit_type')

    try:
        result = fullname_units_available(units_data, unit_type.lower())

        if not result:
            logger.warning('Wanted full name data not available')
            return JsonResponse(
                {'error': 'Requested data not found'}, 
                status=404
            )
        return JsonResponse(result, status=200)
    
    except Exception as e:
        logger.error(f'Error in fullname_wanted_units: {str(e)}', exc_info=True)
        return JsonResponse(
            {'error': 'Internal server error'}, 
            status=500
        )