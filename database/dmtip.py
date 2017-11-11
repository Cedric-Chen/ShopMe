#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMTip(DataModel):
    def __init__(self, cls):
        super().__init__(cls)
        self.dm_attr = [u'user_id', u'business_id', u'text', u'date', u'likes']

    def get_tip(self, business_id, user_id):
        self.query_sql = u'SELECT %s ' % (u', '.join(self.dm_attr)) \
            + u'FROM tip WHERE business_id = "%s" AND user_id = "%s"' \
            % (business_id, user_id)
        ret = super().select()
        result = dict()
        for no, entry in enumerate(ret):
            result[no] = {
                self.dm_attr[index]: value \
                for index, value in enumerate(entry)
            }
        return result
