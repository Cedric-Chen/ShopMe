#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel
from database.mysql.transaction import Transaction


class DMFrequentpattern(DataModel):
    def __init__(self, cls):
        super().__init__(cls)
        self.dm_attr = ['business1_id','business2_id']

    def select_frequent(self, business_id):
        self.query_sql = u'SELECT business2_id ' \
            + u'FROM frequentpattern WHERE business1_id = "%s"' % (business_id)
        print(self.query_sql)
        ret = super().execute()
        result1 = [entry[0] for entry in ret]
        self.query_sql = u'SELECT business1_id ' \
            + u'FROM frequentpattern WHERE business2_id = "%s"' % (business_id)
        print(self.query_sql)
        ret = super().execute()
        result2 = [entry[0] for entry in ret]
        return result1 + result2

    def select_recommendation(self, business_id_list):
        recommendation = []
        for business_id in business_id_list:
            recommendation += self.select_frequent(business_id)
        return recommendation

#    def del_trigger(self, user_id):
#        from datamodel.elite_years import elite_years
#        from datamodel.friend import friend
#        from datamodel.review import review
#        from datamodel.tip import tip
#        for model in [elite_years, friend]:
#            yield model.del_sql(user_id)
#        for model in [review, tip]:
#            yield model.del_sql(u'*', user_id)
#
#    def del_sql(self, user_id):
#        self.query_sql = u'DELETE FROM `user` WHERE id=%s'
#        self.query_args = (user_id,)
#        return self
#
#    def delete(self, user_id, user):
#        with Transaction().prepared() as cursor:
#            for model in self.del_trigger(user_id):
#                cursor.execute(model.query_sql, model.query_args)
#            sql_args = self.del_sql(user_id)
#            cursor.execute(sql_args.query_sql, sql_args.query_args)
#
#    def insert(self, user_id, user):
#        key = []
#        value = []
#        user[u'id'] = user_id
#        for attr in self.dm_attr:
#            if attr in user:
#                key.append(attr)
#                value.append(self.quote_sql(user[attr]))
#        self.query_sql = u'INSERT INTO `user`(%s) VALUES(%s)' \
#            % (u','.join([u'`%s`' % k for k in key]), u','.join(value))
#        super().commit()
#
#    def update(self, user_id, user):
#        pair = []
#        for key, value in user.items():
#            pair.append(u'%s=%s' % (key, self.quote_sql(value)))
#        self.query_sql = u'UPDATE `user` SET %s WHERE id="%s"' \
#            % (u','.join(pair), user_id)
#        super().commit()
