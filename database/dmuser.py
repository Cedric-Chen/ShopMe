#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMUser(DataModel):
    def __init__(self, cls):
        super().__init__(cls)
        self.dm_attr = [u'id', u'name', u'review_count', u'yelping_since', \
            u'useful', u'funny', u'cool', u'fans', u'average_stars', \
            u'compliment_hot', u'compliment_more', u'compliment_profile', \
            u'compliment_cute', u'compliment_list', u'compliment_note', \
            u'compliment_plain', u'compliment_cool', u'compliment_funny', \
            u'compliment_writer', u'compliment_photos'
        ]

    def select(self, _id):
        self.query_sql = u'SELECT %s ' % (u', '.join(self.dm_attr)) \
            + u'FROM user WHERE id = "%s"' % (_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            result = {
                self.dm_attr[index]: value \
                for index, value in enumerate(entry)
            }
        return result

    def delete(self, _id, user):
        from datamodel.elite_years import model as m_elite_years
        from datamodel.friend import model as m_friend
        from datamodel.review import model as m_review
        from datamodel.tip import model as m_tip
        for model in [m_elite_years, m_friend]:
            model.delete(_id, {})
        for model in [m_review, m_tip]:
            model.delete(u'*', _id, {})
        self.query_sql = u'DELETE FROM `user` where id="%s"' % _id
        super().execute()

    def insert(self, user_id, user):
        key = []
        value = []
        user[u'id'] = user_id
        for attr in self.dm_attr:
            if attr in user:
                key.append(attr)
                value.append(self.quote_sql(user[attr]))
        self.query_sql = u'INSERT INTO `user`(%s) VALUES(%s)' \
            % (u','.join([u'`%s`' % k for k in key]), u','.join(value))
        super().execute()

    def update(self, user_id, user):
        pair = []
        for key, value in user.items():
            pair.append(u'%s=%s' % (key, self.quote_sql(value)))
        self.query_sql = u'UPDATE `user` SET %s WHERE id="%s"' \
            % (u','.join(pair), user_id)
        super().execute()
