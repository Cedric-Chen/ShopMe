#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMCategory(DataModel):
    def __init__(self, cls):
        super().__init__(cls)

    def select(self, business_id):
        self.query_sql = u'SELECT category FROM category WHERE ' \
            + 'business_id = "%s"' % (business_id)
        ret = super().select()
        result = dict()
        for index, entry in enumerate(ret):
            result[index] = entry[0]
        return result

    def delete(self, business_id, category):
        if len(category) == 0:
            self.query_sql = u'DELETE FROM `category` WHERE business_id="%s"' \
                % (business_id)
            super().execute()
        for key, val in category.items():
            self.query_sql = \
                u'DELETE FROM `category` WHERE business_id="%s" AND category="%s"' \
                % (business_id, val)
            super().execute()

    def insert(self, business_id, category):
        from datamodel.business import business
        if len(business.select(business_id)) < 1:
            business.insert(business_id, {})
        for key, val in category.items():
            self.query_sql = \
                u'INSERT INTO `category`(`business_id`, `category`) ' \
                + 'VALUES("%s", "%s")' \
                % (business_id, val)
            super().execute()

    def update(self, business_id, category, old_category):
        for key, val in category.items():
            self.query_sql = \
                u'UPDATE `category` SET category=%s WHERE ' \
                % (self.quote_sql(val)) + 'business_id="%s" AND category=%s' \
                % (business_id, self.quote_sql(val))
            super().execute()
