#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMReview(DataModel):
    def __init__(self, cls):
        super().__init__(cls)
        self.dm_attr = [u'id', u'stars', u'date', u'text', u'useful', \
            u'funny', u'cool', u'user_id', u'business_id'
        ]

    def get_review(self, business_id, user_id):
        self.query_sql = u'SELECT %s ' % (u', '.join(self.dm_attr)) \
            + u'FROM review WHERE business_id = "%s" AND user_id = "%s"' \
            % (business_id, user_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            result[entry[0]] = {
                self.dm_attr[index]: value \
                for index, value in enumerate(entry)
            }
        return result
