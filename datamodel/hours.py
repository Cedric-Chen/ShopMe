#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.dmhours import DMHours

class Hours(DMHours):
    def __init__(self):
        super().__init__(self)

    def select(self, business_id):
        _hours = super().select(business_id)
        for key in self.dm_attr:
            if key not in _hours:
                _hours[key] = 'Not Available'
        return _hours

hours = Hours()
