#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMCategory(DataModel):
    def __init__(self, cls):
        super().__init__(cls)

    def get_category(self, business_id):
        self.query_sql = u'SELECT category FROM category WHERE ' \
            + 'business_id = "%s"' % (business_id)
        ret = super().select()
        result = dict()
        for index, entry in enumerate(ret):
            result[index] = entry[0]
        return result
