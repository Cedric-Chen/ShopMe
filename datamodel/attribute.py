#!/usr/bin/python
# -*- coding: utf-8 -*-

class Attribute(object):
    def get_attribute(self):
        return {
            'BikeParking': 1,
            'BusinessAcceptsCreditCards': 1,
            'BusinessParking': {
                'garage': False,
                'lot': True,
                'street': False,
                'valet': False,
                'validated': False
            },
            'ByAppointmentOnly': 0,
            'HairSpecializesIn': {
                'africanamerican': False,
                'asian': False,
                'coloring': False,
                'curly': False,
                'extensions': False,
                'kids': False,
                'perms': False,
                'straightperms': False
            },
            'RestaurantsPriceRange2': 2,
            'WheelchairAccessible': 1
        }

model = Attribute()
