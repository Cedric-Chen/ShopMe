#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel


class DMBusiness(DataModel):
    def __init__(self, cls):
        super().__init__(cls)
        self.dm_attr = [u'id', u'name', u'neighborhood', u'address', u'city', \
                        u'state', u'postal_code', u'latitude', u'longitude', \
                        u'stars', u'review_count', u'is_open']

    def sort_ret(self):
        return [{self.dm_attr[index]: value \
                for index, value in enumerate(entry)
            } for entry in super().select()
        ]

    def sort_by(self, business, field_list, op_list, key, order):
        if len(field_list) != len(op_list):
            return []
        cond = []
        for x in range(0, len(field_list)):
            field = field_list[x]
            if field in self.dm_attr and field in business:
                cond.append(u'%s %s %s' \
                    % (field, op_list[x], self.quote_sql(business[field])))
        self.query_sql = u'SELECT %s FROM business WHERE %s ' \
            % (u', '.join(self.dm_attr), u' AND '.join(cond))
        self.query_sql += self.select_order(key, order)
        return self.sort_ret()

    def keyword_search(self, query_dict):
        condition = ['category.business_id = business.id']
        if "keyword" in query_dict:
            keywords = query_dict["keyword"]
            for key in keywords:
                condition.append(
                    u"(category like '%" + key + "%'" + u" OR " + u"name like '%" + key + "%')")
            self.query_sql = u'SELECT %s FROM category, business WHERE ' %(','.join(self.dm_attr))
        else:
            self.query_sql = u'SELECT * FROM business WHERE '

        if "attribute" in query_dict:
            attributes = query_dict["attribute"]
            for attr in query_dict["attribute"]:
                if attr in self.dm_attr:
                    condition.append(attr + attributes[attr])
        self.query_sql += u' AND '.join(condition)
        self.query_sql += self.select_order([u"name"], 1)
        return self.sort_ret()



    def sort_close(self, business, distance, key, order):
        longi = business.get(u'longitude', None)
        latit = business.get(u'latitude', None)
        self.query_sql = u'SELECT %s FROM business WHERE ' \
            % (u', '.join(self.dm_attr)) \
            + u' ST_Distance(Point(%s, %s), Point(longitude,latitude)) <= %s ' \
            % (longi, latit, distance)
        self.query_sql += self.select_order(key, order)
        return self.sort_ret()

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
        from datamodel.attribute import attribute
        from datamodel.category import category
        from datamodel.checkin import checkin
        from datamodel.hours import hours
        from datamodel.photo import photo
        from datamodel.review import review
        from datamodel.tip import tip
        for model in [attribute, category, checkin, hours, photo]:
            model.delete(business_id, {})
        for model in [review, tip]:
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
        for key in self.dm_attr:
            if key in business:
                pair.append(u'%s=%s' % (key, self.quote_sql(business[key])))
        self.query_sql = u'UPDATE `business` SET %s WHERE id="%s"' \
            % (u','.join(pair), business_id)
        super().execute()
