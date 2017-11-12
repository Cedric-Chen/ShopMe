#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMBusiness(DataModel):
    def __init__(self, cls):
        super().__init__(cls)
        self.dm_attr = [u'id', u'name', u'neighborhood', u'address', u'city', \
            u'state', u'postal_code', u'latitude', u'longitude', \
            u'stars', u'review_count', u'is_open']

    def select(self, business_id):
        self.query_sql = u'SELECT %s FROM business WHERE id = "%s"' \
            % (u', '.join(self.dm_attr), business_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            for index, value in enumerate(entry):
                result[self.dm_attr[index]] = value
        return result

    def delete(self, business_id, business):
        from datamodel.attribute import model as m_attribute
        from datamodel.category import model as m_category
        from datamodel.checkin import model as m_checkin
        from datamodel.hours import model as m_hours
        from datamodel.photo import model as m_photo
        from datamodel.review import model as m_review
        from datamodel.tip import model as m_tip
        for model in [m_attribute, m_category, m_checkin, m_hours, m_photo]:
            model.delete(business_id, {})
        for model in [m_review, m_tip]:
            model.delete(business_id, u'*', {})
        self.query_sql = u'DELETE FROM `business` WHERE id="%s"' % business_id
        super().execute()

    def insert(self, business_id, business):
        key = []
        value = []
        business[u'id'] = business_id
        for attr in self.dm_attr:
            if attr in business:
                key.append(attr)
                value.append(self.quote_sql(business[attr]))
        self.query_sql = u'INSERT INTO `business`(%s) VALUES(%s)' \
            % (u','.join([u'`%s`' % k for k in key]), u','.join(value))
        super().execute()

    def update(self, business_id, business, old_business):
        pair = []
        for key, value in business.items():
            pair.append(u'%s=%s' % (key, self.quote_sql(value)))
        self.query_sql = u'UPDATE `business` SET %s WHERE id="%s"' \
            % (u','.join(pair), business_id)
        super().execute()
