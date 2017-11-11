#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMUser(DataModel):
    def __init__(self, cls):
        super().__init__(cls)
        self.dm_attr = [u'id', u'name', u'review_count', u'yelping_since', \
            u'useful', u'funny', u'cool', u'fans', u'average_stars', \
            u'compliment_hot', u'compliment_more', u'compliment_profile', \
            u'compliment_cute', u'compliment_list', u'compliment_note', \
            u'compliment_plain', u'compliment_cool', u'compliment_funny', \
            u'compliment_writer', u'compliment_photos'
        ]

    def get_user(self, _id):
        self.query_sql = u'SELECT %s ' % (u', '.join(self.dm_attr)) \
            + u'FROM user WHERE id = "%s"' % (_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            result = {
                self.dm_attr[index]: value \
                for index, value in enumerate(entry)
            }
        return result
