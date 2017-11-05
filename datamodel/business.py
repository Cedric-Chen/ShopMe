#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.dmbusiness import DMBusiness

class Business(DMBusiness):
    def __init__(self):
        super().__init__(self)

    def get_business(self, business_id):
        '''
        @return: dict
        '''
        try:
            return self.business
        except:
            self.business = super().get_business(business_id)
        return self.business

model = Business()
