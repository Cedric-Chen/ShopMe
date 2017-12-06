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
        ret = super().execute()
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
        if self.basetype_sql(attr):
            return attr
        elif type(attr) == str:
            return "'%s'" % (attr)
        else:
            return "'%s'" % (json.dumps(attr))


    def del_sql(self, business_id):
        self.query_sql = u'DELETE FROM `attribute` WHERE business_id=%s'
        self.query_args = (business_id,)
        return self

    def delete(self, business_id, attribute):
        if len(attribute) == 0:
            self.query_sql = self.del_sql(business_id).toquery()
            super().commit()
        for key in attribute:
            self.query_sql = \
                u'DELETE FROM `attribute` WHERE business_id="%s" AND name=%s' \
                % (business_id, self.quote_sql(key))
            super().commit()

    def insert(self, business_id, attribute):
        from datamodel.business import business
        if len(business.select(business_id)) < 1:
            business.insert(business_id, {})
        for key, val in attribute.items():
            self.query_sql = \
                u'INSERT INTO `attribute`(`business_id`, `name`, `value`) ' \
                + 'VALUES("%s", %s, %s)' \
                % (business_id, self.quote_sql(key), self.val2sql(val))
            super().commit()

    def update(self, business_id, attribute, old_attribute):
        for key, val in attribute.items():
            self.query_sql = \
                u'UPDATE `attribute` SET value=%s WHERE ' \
                % (self.val2sql(val)) + 'business_id="%s" AND name=%s' \
                % (business_id, self.quote_sql(key))
#            assert False, self.query_sql
            
            super().commit()
