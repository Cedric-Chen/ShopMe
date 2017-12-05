#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.dmreview import DMReview

class Review(DMReview):
    def __init__(self):
        super().__init__(self)

    def select_top_review(self):
        self.query_sql = u'SELECT %s ' % (u', '.join(self.dm_attr)) \
                + u'FROM review LIMIT 4'

        ret = super().execute()
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

review = Review()
