#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMTip(DataModel):
    def __init__(self, cls):
        super().__init__(cls)
        self.dm_attr = [u'user_id', u'business_id', u'text', u'date', u'likes']

    def select(self, business_id, user_id):
        self.query_sql = u'SELECT %s ' % (u', '.join(self.dm_attr)) \
            + u'FROM tip WHERE business_id = "%s" AND user_id = "%s"' \
            % (business_id, user_id)
        ret = super().select()
        result = dict()
        for no, entry in enumerate(ret):
            result[no] = {
                self.dm_attr[index]: value \
                for index, value in enumerate(entry)
            }
        return result

    def delete(self, business_id, user_id, tip):
        if len(tip) == 0:
            if business_id == u'*':
                self.query_sql = \
                    u'DELETE FROM `tip` WHERE user_id="%s"' % (user_id)
            elif user_id == u'*':
                self.query_sql = \
                    u'DELETE FROM `tip` WHERE business_id="%s"' % (business_id)
            else:
                self.query_sql = u'DELETE FROM `tip` WHERE business_id="%s"' \
                    % (business_id) + u' AND user_id="%s"' % (user_id)
            super().execute()
        for key, val in tip.items():
            pair = []
            for k, v in val.items():
                pair.append(u'%s=%s' % (k, self.quote_sql(v)))
            self.query_sql = u'DELETE FROM `tip` WHERE %s' \
                % (' AND '.join(pair))
            super().execute()

    def insert(self, business_id, user_id, tip):
        from datamodel.business import model as m_business
        if len(m_business.select(business_id)) < 1:
            m_business.insert(business_id, {})
        from datamodel.user import model as m_user
        if len(m_user.select(user_id)) < 1:
            m_user.insert(user_id, {})
        for key, val in tip.items():
            k = []
            v = []
            for attr in self.dm_attr:
                k.append(attr)
                v.append(self.quote_sql(val[attr]))
            self.query_sql = u'INSERT INTO `tip`(%s) ' % (u','.join(k)) \
                + 'VALUES(%s)' % (u','.join(v))
            super().execute()

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
                print(self.query_sql)
                super().execute()
