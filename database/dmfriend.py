#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMFriend(DataModel):
    def __init__(self, cls):
        super().__init__(cls)

    def select(self, user_id):
        self.query_sql = u'SELECT friend_id FROM friend WHERE user_id = "%s"' \
            % (user_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            result[entry[0]] = user_id
        return result

    def delete(self, user_id, friend):
        if len(friend) == 0:
            self.query_sql = u'DELETE FROM `friend` WHERE user_id="%s"' \
                % (user_id)
            super().execute()
        for key in friend:
            self.query_sql = \
                u'DELETE FROM `friend` WHERE user_id="%s" AND ' \
                % (user_id) + 'friend_id="%s"' % (key)
            super().execute()

    def insert(self, user_id, friend):
        from datamodel.user import user
        if len(user.select(user_id)) < 1:
            user.insert(user_id, {})
        for key in friend:
            self.query_sql = \
                u'INSERT INTO `friend`(`user_id`, `friend_id`) ' \
                + 'VALUES("%s", "%s")' % (user_id, key)
            super().execute()

    def update(self, user_id, friend, old_friend):
        self.delete(user_id, old_friend)
        self.delete(user_id, friend)
        self.insert(user_id, friend)
