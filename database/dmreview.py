#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict

from database.datamodel import DataModel

class DMReview(DataModel):
    def __init__(self, cls):
        super().__init__(cls)
        self.dm_attr = [u'id', u'stars', u'date', u'text', u'useful', \
            u'funny', u'cool', u'user_id', u'business_id'
        ]

    def select_query(self, business_id, user_id):
        query_sql = u''
        if business_id == u'*':
            query_sql = u'SELECT %s ' % (u', '.join(self.dm_attr)) \
                + u'FROM review WHERE user_id = "%s"' % (user_id)
        elif user_id == u'*':
            query_sql = u'SELECT %s ' % (u', '.join(self.dm_attr)) \
                + u'FROM review WHERE business_id = "%s"' % (business_id)
        else:
            query_sql = u'SELECT %s ' % (u', '.join(self.dm_attr)) \
                + u'FROM review WHERE business_id = "%s" AND user_id = "%s"' \
                % (business_id, user_id)
        return query_sql

    def sort(self, business_id, user_id, key, order):
        self.query_sql = self.select_query(business_id, user_id)
        self.query_sql += self.select_order(key, order)
        return [{self.dm_attr[index]: value \
                    for index, value in enumerate(entry)
                } for entry in super().select()
            ]

    def select(self, business_id, user_id):
        self.query_sql = self.select_query(business_id, user_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            result[entry[0]] = {
                self.dm_attr[index]: value \
                for index, value in enumerate(entry)
            }
        return result

    def select_top_review(self):
        self.query_sql = u'SELECT %s ' % (u', '.join(self.dm_attr)) \
                + u'FROM review LIMIT 4'

        ret = super().select()
        result = dict()
        for entry in ret:
            result[entry[0]] = {
                self.dm_attr[index]: value \
                for index, value in enumerate(entry)
            }
        
        from datamodel.business import business
        from datamodel.user import user
        imgs = [
        'https://www.redrobin.com/content/dam/web/menu/2015-june/royal-red-robin-burger-217.jpg',
        'http://www.santabarbara.com/dining/news/wp-content/uploads/2014/07/140724a-himialayan-kitchen.jpg',
        'https://media-cdn.tripadvisor.com/media/photo-s/02/ac/27/54/filename-pepperoni-oncan.jpg',
        'https://mediaassets.abc15.com/photo/2016/10/26/KNXV%20The%20Thumb%20on%20Tanked%204_1477513386718_48701044_ver1.0_640_480.jpg'
        ]
        top_reviews = list()
        i=0
        for key, value in result.items():
            businessid = value['business_id']
            userid = value['user_id']
            businessname = business.select(businessid)['name']
            username = user.select(userid)['name']
            text = value['text']
            top_reviews.append({'user_name': username, \
                 'business_name': businessname, \
                 'business_id': businessid, \
                 'user_id': userid, \
                 'text': text, \
                 'img': imgs[i]})
            i += 1
            
        return top_reviews

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
        from datamodel.business import business
        if len(business.select(business_id)) < 1:
            business.insert(business_id, {})
        from datamodel.user import user
        if len(user.select(user_id)) < 1:
            user.insert(user_id, {})
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
