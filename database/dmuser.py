#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel
from database.mysql.transaction import Transaction


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
        ret = super().execute()
        result = dict()
        for entry in ret:
            result = {
                self.dm_attr[index]: value \
                for index, value in enumerate(entry)
            }
        return result

    def del_trigger(self, user_id):
        from datamodel.elite_years import elite_years
        from datamodel.friend import friend
        from datamodel.review import review
        from datamodel.tip import tip
        for model in [elite_years, friend]:
            yield model.del_sql(user_id)
        for model in [review, tip]:
            yield model.del_sql(u'*', user_id)

    def del_sql(self, user_id):
        self.query_sql = u'DELETE FROM `user` WHERE id=%s'
        self.query_args = (user_id,)
        return self

    def delete(self, user_id, user):
        with Transaction().prepared() as cursor:
            for model in self.del_trigger(user_id):
                cursor.execute(model.query_sql, model.query_args)
            sql_args = self.del_sql(user_id)
            cursor.execute(sql_args.query_sql, sql_args.query_args)

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
        super().commit()

    def update(self, user_id, user):
        pair = []
        for key, value in user.items():
            pair.append(u'%s=%s' % (key, self.quote_sql(value)))
        self.query_sql = u'UPDATE `user` SET %s WHERE id="%s"' \
            % (u','.join(pair), user_id)
        super().commit()
