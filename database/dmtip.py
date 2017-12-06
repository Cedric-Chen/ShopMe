#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMTip(DataModel):
    def __init__(self, cls):
        super().__init__(cls)
        self.dm_attr = [u'user_id', u'business_id', u'text', u'date', u'likes']

    def select_query(self, business_id, user_id):
        query_sql = u''
        if business_id == u'*':
            query_sql = u'SELECT %s ' % (u', '.join(self.dm_attr)) \
                + u'FROM `tip` WHERE user_id = "%s"' % (user_id)
        elif user_id == u'*':
            query_sql = u'SELECT %s ' % (u', '.join(self.dm_attr)) \
                + u'FROM `tip` WHERE business_id = "%s"' % (business_id)
        else:
            query_sql = u'SELECT %s ' % (u', '.join(self.dm_attr)) \
                + u'FROM `tip` WHERE business_id = "%s" AND user_id = "%s"' \
                % (business_id, user_id)
        return query_sql

    def sort(self, business_id, user_id, key, order):
        self.query_sql = self.select_query(business_id, user_id)
        self.query_sql += self.select_order(key, order)
        return [{self.dm_attr[index]: value \
                    for index, value in enumerate(entry)
                } for entry in super().execute()
            ]

    def select(self, business_id, user_id):
        self.query_sql = self.select_query(business_id, user_id)
        ret = super().execute()
        result = dict()
        for no, entry in enumerate(ret):
            result[no] = {
                self.dm_attr[index]: value \
                for index, value in enumerate(entry)
            }
        return result

    def del_sql(self, business_id, user_id):
        if business_id == u'*' and user_id != u'*':
            self.query_sql = u'DELETE FROM `tip` WHERE user_id=%s'
            self.query_args = (user_id,)
        elif business_id != u'*' and user_id == u'*':
            self.query_sql = u'DELETE FROM `tip` WHERE business_id=%s'
            self.query_args = (business_id,)
        else:
            self.query_sql = u'DELETE FROM `tip` WHERE business_id=%s AND ' \
                + 'user_id=%s'
            self.query_args = (business_id, user_id)
        return self

    def delete(self, business_id, user_id, tip):
        if len(tip) == 0:
            self.query_sql = self.del_sql(business_id, user_id).toquery()
            super().commit()
        for key, val in tip.items():
            pair = []
            for k, v in val.items():
                pair.append(u'%s=%s' % (k, self.quote_sql(v)))
            self.query_sql = u'DELETE FROM `tip` WHERE %s' \
                % (' AND '.join(pair))
            super().commit()

    def insert(self, business_id, user_id, tip):
        from datamodel.business import business
        if len(business.select(business_id)) < 1:
            business.insert(business_id, {})
        from datamodel.user import user
        if len(user.select(user_id)) < 1:
            user.insert(user_id, {})
        for key, val in tip.items():
            k = []
            v = []
            for attr in self.dm_attr:
                k.append(attr)
                v.append(self.quote_sql(val[attr]))
            self.query_sql = u'INSERT INTO `tip`(%s) ' % (u','.join(k)) \
                + 'VALUES(%s)' % (u','.join(v))
            super().commit()

    def update(self, business_id, user_id, tip, old_tip):
        for key, val in tip.items():
            if key not in old_tip \
                and key not in self.select(business_id, user_id):
                self.insert(business_id, user_id, {key: val})
            else:
                pair = []
                for k, v in val.items():
                    pair.append(u'%s=%s' % (k, self.quote_sql(v)))
                self.query_sql = u'UPDATE tip SET %s WHERE business_id="%s"' \
                    % (u', '.join(pair), business_id) \
                    + u' AND user_id="%s"' % (user_id)
                super().commit()
