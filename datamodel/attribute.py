#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.dmattribute import DMAttribute

class Attribute(DMAttribute):
    def __init__(self):
        super().__init__(self)

    def get_attribute(self, business_id):
        '''
        @return: dict
        '''
        try:
            return self.attribute
        except:
            self.attribute = super().get_attribute(business_id)
        return self.attribute

model = Attribute()
