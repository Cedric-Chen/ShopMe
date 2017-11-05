#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMBusiness(DataModel):
    def __init__(self, cls):
        super().__init__(cls)
        self.dm_attr = [u'id', u'name', u'neighborhood', u'address', u'city', \
            u'state', u'postal_code', u'latitude', u'longitude', \
            u'stars', u'review_count', u'is_open']

    def get_business(self, business_id):
        self.query_sql = u'SELECT %s FROM business WHERE id = "%s"' \
            % (u', '.join(self.dm_attr), business_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            for index, value in enumerate(entry):
                result[self.dm_attr[index]] = value
        return result
