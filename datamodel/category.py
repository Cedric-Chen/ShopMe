#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.dmcategory import DMCategory

class Category(DMCategory):
    def __init__(self):
        super().__init__(self)

    def get_category(self, business_id):
        '''
        @return: dict
        '''
        try:
            return self.category
        except:
            self.category = super().get_category(business_id)
        return self.category

model = Category()
