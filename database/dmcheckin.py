#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMCheckIn(DataModel):
    def __init__(self, cls):
        super().__init__(cls)

    def get_checkin(self, business_id):
        self.query_sql = u'SELECT date, count FROM checkin WHERE ' \
            + u'business_id = "%s"' % (business_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            k_date = entry[0]
            result[k_date] = result.get(k_date, 0) + entry[1]
        return result
