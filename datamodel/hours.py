#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.dmhours import DMHours

class Hours(DMHours):
    def __init__(self):
        super().__init__(self)

    def get_hour(self, business_id):
        '''
        @return: dict
        '''
        try:
            return self.business_hour
        except:
            self.business_hour = super().get_hour(business_id)
        return self.business_hour

model = Hours()
