#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template, request
from flask_paginate import Pagination, get_page_args
from geopy.distance import vincenty

from config import app
from datamodel.business import business
from datamodel.category import category
from datamodel.checkin import checkin
from datamodel.review import review
from datamodel.user import user

class recommender(object):
    def __init__(self, business_list, user_loc):
        self.business_list = business_list
        self.user_loc = user_loc
    def score(self,business):
        distance = vincenty(self.user_loc,(business['latitude'],business['longitude'])).miles
        return business['stars'] + 1/distance
    def recommend(self):
        return sorted(self.business_list, key = self.score, reverse = True)


@app.route(u'/search/<key>:<value>/')
def search(key, value):
    business_list = business.sort_by({key: value}, [key], [u'='], u'*', u'*')
    my_loc = (40.12889642298632,-88.22373041280238)
    RS = recommender(business_list,my_loc)
    business_list = RS.recommend()
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    per_page = 10
    pagination = Pagination(page=page, per_page=per_page,total=len(business_list), search=False, record_name='results')
    business_list = business_list[(page - 1) * per_page: page * per_page]

    category_list = []
    checkin_list = []
    review_list = []
    user_list = []
    for business_item in business_list:
        business_id = business_item[u'id']
        category_list.append(category.select(business_id))
        checkin_list.append(checkin.select(business_id))
        review_items = review.select(business_id,u'*')
        keys = list(review_items.keys())
        if len(keys) > 0:
            user_list.append(user.select(review_items[keys[0]][u'user_id']))
            s = review_items[keys[0]]['text']
            s2 = ' '.join(s.split(' ')[0:80]) + "..."
            review_list.append(s2)
        else:
            user_list.append({})
            review_list.append(review_items)

    num_checkin_list = []
    for c in checkin_list:
        num_checkin_list.append(sum(list(c.values())))

    # When the search result lists are generated.
    laglng_list = [[b['name'], b['latitude'], b['longitude']] for b in business_list]
    result_list = list()
    for idx in range(0, len(business_list)):
        result = dict()
        result['category'] = ', '.join(list(category_list[idx].values()))
        result['business'] = business_list[idx]
        result['num_checkin'] = num_checkin_list[idx]
        result['review'] = review_list[idx]
        result['user'] = user_list[idx]
        result_list.append(result)


    return render_template(u'search.html',
        business = business_list[0] if len(business_list) > 0 else None,
        result_list=result_list,
        laglng_list=laglng_list,
        page=page,
        per_page=per_page,
        pagination=pagination)
