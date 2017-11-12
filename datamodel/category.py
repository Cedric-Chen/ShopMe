#!/usr/bin/python
# -*- coding: utf-8 -*-

class Category(object):
    def get_category(self):
        return {
            0: 'Food',
            1: 'Soul Food',
            2: 'Convenience Stores',
            3: 'Restaurants'
        }

model = Category()
