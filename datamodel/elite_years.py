#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.dmelite_years import DMElite_Years

class Elite_Years(DMElite_Years):
    def __init__(self):
        super().__init__(self)

    def get_elite_years(self, business_id):
        '''
        @return: dict
        '''
        try:
            return self.elite_years
        except:
            self.elite_years = super().get_elite_years(business_id)
        return self.elite_years

model = Elite_Years()
