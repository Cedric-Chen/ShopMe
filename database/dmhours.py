#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMHours(DataModel):
    def __init__(self, cls):
        super().__init__(cls)

    def get_hour(self, business_id):
        self.query_sql = u'SELECT hours FROM hours WHERE business_id = "%s"' \
            % (business_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            date, time = entry[0].split(u'|')
            result[date] = time
        return result
