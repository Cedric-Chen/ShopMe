#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMPhoto(DataModel):
    def __init__(self, cls):
        super().__init__(cls)
        self.dm_attr = [u'id', u'business_id', u'caption', u'label']

    def get_photo(self, business_id):
        self.query_sql = u'SELECT %s ' % (u', '.join(self.dm_attr)) \
            + u'FROM photo WHERE business_id = "%s"' % (business_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            result[entry[0]] = {
                self.dm_attr[index]: value \
                for index, value in enumerate(entry)
            }
        return result
