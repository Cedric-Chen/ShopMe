#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMElite_Years(DataModel):
    def __init__(self, cls):
        super().__init__(cls)

    def select(self, user_id):
        self.query_sql = u'SELECT year FROM elite_years WHERE ' \
            + 'user_id = "%s"' % (user_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            result[entry[0]] = user_id
        return result

    def delete(self, user_id, elite_years):
        if len(elite_years) == 0:
            self.query_sql = u'DELETE FROM `elite_years` WHERE user_id="%s"' \
                % (user_id)
            super().execute()
        for key in elite_years:
            self.query_sql = \
                u'DELETE FROM `elite_years` WHERE user_id="%s" AND ' \
                % (user_id) + 'year="%s"' % (key)
            super().execute()

    def insert(self, user_id, elite_years):
        from datamodel.user import user
        if len(user.select(user_id)) < 1:
            user.insert(user_id, {})
        for key in elite_years:
            self.query_sql = \
                u'INSERT INTO `elite_years`(`user_id`, `year`) ' \
                + 'VALUES("%s", "%s")' % (user_id, key)
            super().execute()

    def update(self, user_id, elite_years, old_elite_years):
        self.delete(user_id, old_elite_years)
        self.delete(user_id, elite_years)
        self.insert(user_id, elite_years)
