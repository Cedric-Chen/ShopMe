#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMElite_Years(DataModel):
    def __init__(self, cls):
        super().__init__(cls)

    def get_elite_years(self, user_id):
        self.query_sql = u'SELECT year FROM elite_years WHERE ' \
            + 'user_id = "%s"' % (user_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            result[entry[0]] = user_id
        return result
