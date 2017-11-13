#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMReview(DataModel):
    def __init__(self, cls):
        super().__init__(cls)
        self.dm_attr = [u'id', u'stars', u'date', u'text', u'useful', \
            u'funny', u'cool', u'user_id', u'business_id'
        ]

    def select(self, business_id, user_id):
        self.query_sql = u'SELECT %s ' % (u', '.join(self.dm_attr)) \
            + u'FROM review WHERE business_id = "%s" AND user_id = "%s"' \
            % (business_id, user_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            result[entry[0]] = {
                self.dm_attr[index]: value \
                for index, value in enumerate(entry)
            }
        return result

    def delete(self, business_id, user_id, review):
        if len(review) == 0:
            if business_id == u'*':
                self.query_sql = \
                    u'DELETE FROM `review` WHERE user_id="%s"' % (user_id)
            elif user_id == u'*':
                self.query_sql = \
                    u'DELETE FROM `review` WHERE business_id="%s"' \
                    % (business_id)
            else:
                self.query_sql = \
                    u'DELETE FROM `review` WHERE business_id="%s"' \
                    % (business_id) + u' AND user_id="%s"' % (user_id)
            super().execute()
        for key, val in review.items():
            pair = [u'id=%s' % (self.quote_sql(key))]
            for k, v in val.items():
                if k != 'id':
                    pair.append(u'%s=%s' % (k, self.quote_sql(v)))
            self.query_sql = u'DELETE FROM `review` WHERE %s' \
                % (' AND '.join(pair))
            super().execute()

    def insert(self, business_id, user_id, review):
        from datamodel.business import model as m_business
        if len(m_business.select(business_id)) < 1:
            m_business.insert(business_id, {})
        from datamodel.user import model as m_user
        if len(m_user.select(user_id)) < 1:
            m_user.insert(user_id, {})
        for key, val in review.items():
            k = [u'id']
            v = [self.quote_sql(key)]
            for attr in self.dm_attr:
                if attr in val and attr != u'id':
                    k.append(attr)
                    v.append(self.quote_sql(val[attr]))
            self.query_sql = u'INSERT INTO `review`(%s) ' % (u','.join(k)) \
                + 'VALUES(%s)' % (u','.join(v))
            super().execute()

    def update(self, business_id, user_id, review, old_review):
        for key, val in review.items():
            if key not in old_review \
                and key not in self.select(business_id, user_id):
                self.insert(business_id, user_id, {key: val})
            else:
                pair = [u'id=%s' % (self.quote_sql(key))]
                for k, v in val.items():
                    if k != 'id':
                        pair.append(u'%s=%s' % (k, self.quote_sql(v)))
                self.query_sql = u'UPDATE review SET %s WHERE id="%s"' \
                    % (u', '.join(pair), key)
                super().execute()
