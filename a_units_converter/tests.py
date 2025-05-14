from django.test import TestCase

import json
from logic import *

with open("a_units_converter/data/units.json", "r") as units:
    data_units = json.load(units)

