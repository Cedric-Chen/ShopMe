#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMFriend(DataModel):
    def __init__(self, cls):
        super().__init__(cls)

    def get_friend(self, user_id):
        self.query_sql = u'SELECT friend_id FROM friend WHERE user_id = "%s"' \
            % (user_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            result[entry[0]] = user_id
        return result
