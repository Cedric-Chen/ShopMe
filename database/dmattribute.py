#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from config import app
from database.datamodel import DataModel


class DMAttribute(DataModel):
    def __init__(self, cls):
        super().__init__(cls)

    def get_attribute(self, business_id):
        self.query_sql = u'SELECT name, value FROM attribute WHERE ' \
                         + 'business_id = "%s"' % (business_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            value = entry[1]
            try:
                value = json.loads(entry[1])
            except Exception as e:
                app.logger.warning(u'Exception when json.loads(%s) ' \
                                   + u'with qeruy: %s' % (value, self.query_sql))
            result[entry[0]] = value
        return result
