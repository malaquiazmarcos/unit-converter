from django.urls import path
from a_units_converter.views import *

urlpatterns = [
    path('unit-convert', unit_convert, name='unit_convert'),
    path('all-data', show_all_data, name='show_all_data'),
    path('units-available', show_units_available, name='show_units_available'),
    path('short-description', show_short_description, name='show_short_description'),
    path('magnitudes-available', show_magnitudes, name='show_magnitudes'),
    path('full-name-all-units', show_all_fullname, name='show_all_fullname'),
    path('full-name-units', fullname_wanted_units, name='fullname_wanted_units'),
]