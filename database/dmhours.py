#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMHours(DataModel):
    def __init__(self, cls):
        super().__init__(cls)

    def select(self, business_id):
        self.query_sql = u'SELECT hours FROM hours WHERE business_id = "%s"' \
            % (business_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            date, time = entry[0].split(u'|')
            result[date] = time
        return result

    def delete(self, business_id, hours):
        if len(hours) == 0:
            self.query_sql = u'DELETE FROM `hours` WHERE business_id="%s"' \
                % (business_id)
            super().execute()
        for key, val in hours.items():
            self.query_sql = \
                u'DELETE FROM `hours` WHERE business_id="%s" AND ' \
                % (business_id) + 'hours="%s"' % (key + "|" + val)
            super().execute()

    def insert(self, business_id, hours):
        from datamodel.business import business
        if len(business.select(business_id)) < 1:
            business.insert(business_id, {})
        for key, val in hours.items():
            self.query_sql = \
                u'INSERT INTO `hours`(`business_id`, `hours`) ' \
                + 'VALUES("%s", "%s")' % (business_id, key + "|" + val)
            super().execute()

    def update(self, business_id, hours, old_hours):
        self.delete(business_id, old_hours)
        self.delete(business_id, hours)
        self.insert(business_id, hours)
