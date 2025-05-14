from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
import logging
from a_units_converter.logic import *

logger = logging.getLogger(__name__)

with open("a_units_converter/data/units.json", "r", encoding='utf-8') as data:
    units_data = json.load(data)

@require_http_methods(['GET'])
def unit_convert(request):
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
            result = temperature_converter(value, unit_type, unit_from, unit_to, units_data)
        else:
            result = units_converter(value, unit_type, unit_from, unit_to, units_data)

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
def show_all_data(request):
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
def show_units_available(request):
    try:
        result = units_available(units_data)

        if not result:
            logger.warning('Units available data is not available')
            return JsonResponse(
                {'error': 'Requested data is not found'}, 
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
def show_short_description(request):
    unit_type = request.GET.get('unit_type')
    unit = request.GET.get('unit')

    try: 
        result = short_description_unit(units_data, unit_type, unit)

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
def show_magnitudes(request):
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
def show_all_fullname(request):
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
def fullname_wanted_units(request):
    unit_type = request.GET.get('unit_type')

    try:
        result = fullname_units_available(units_data, unit_type)

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




# endpoint for test API
# curl "http://127.0.0.1:8000/V1/unit-convert/?value=1&unit_type=data&unit_from=GiB&unit_to=MiB"
# curl "http://127.0.0.1:8000/V1/all-data/"
# curl "http://127.0.0.1:8000/V1/units-available/"
# curl "http://127.0.0.1:8000/V1/short-description/?unit_type=data&unit=MB"
# curl "http://127.0.0.1:8000/V1/magnitudes-available/"
# curl "http://127.0.0.1:8000/V1/full-name-all-units/"
# curl "http://127.0.0.1:8000/V1/full-name-units/?unit_type=data"

    
