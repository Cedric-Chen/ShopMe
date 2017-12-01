#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from config import app
from database.datamodel import DataModel

class DMAttribute(DataModel):
    def __init__(self, cls):
        super().__init__(cls)

    def select(self, business_id):
        self.query_sql = u'SELECT name, value FROM attribute WHERE ' \
            + 'business_id = "%s"' % (business_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            value = entry[1]
            try:
                value = json.loads(entry[1])
            except Exception as e:
                app.logger.warning(u'Exception when json.loads(%s) ' % (value)\
                    + u'with query: %s' % (self.query_sql))
            result[entry[0]] = value
        return result

    def val2sql(self, attr):
        attr_value = attr if self.basetype_sql(attr) or type(attr) == str \
            else json.dumps(attr)
        return self.quote_sql(attr_value)

    def delete(self, business_id, attribute):
        if len(attribute) == 0:
            self.query_sql = u'DELETE FROM `attribute` WHERE business_id="%s"' \
                % (business_id)
            super().execute()
        for key in attribute:
            self.query_sql = \
                u'DELETE FROM `attribute` WHERE business_id="%s" AND name=%s' \
                % (business_id, self.quote_sql(key))
            super().execute()

    def insert(self, business_id, attribute):
        from datamodel.business import business
        if len(business.select(business_id)) < 1:
            business.insert(business_id, {})
        for key, val in attribute.items():
            self.query_sql = \
                u'INSERT INTO `attribute`(`business_id`, `name`, `value`) ' \
                + 'VALUES("%s", %s, %s)' \
                % (business_id, self.quote_sql(key), self.val2sql(val))
            super().execute()

    def update(self, business_id, attribute, old_attribute):
        for key, val in attribute.items():
            self.query_sql = \
                u'UPDATE `attribute` SET value=%s WHERE ' \
                % (self.val2sql(val)) + 'business_id="%s" AND name=%s' \
                % (business_id, self.quote_sql(key))
#            assert False, self.query_sql
            
            super().execute()
