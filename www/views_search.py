#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template

from config import app
from datamodel.business import business
from datamodel.category import category
from datamodel.checkin import checkin
from datamodel.review import review
from datamodel.user import user

@app.route(u'/search/<key>:<value>/')
def search(key, value):
    business_list = business.sort_by({key: value}, [key], [u'='], u'*', u'*')
    category_list = []
    checkin_list = []
    review_list = []
    user_list = []
    for business_item in business_list:
        business_id = business_item[u'id']
        category_list.append(category.select(business_id))
        checkin_list.append(checkin.select(business_id))
        review_items = review.select(business_id,u'*')
        review_list.append(review_items)
        keys = list(review_items.keys())
        if len(keys) > 0:
            user_list.append(user.select(review_items[keys[0]][u'user_id']))
        else:
            user_list.append({})

    num_checkin_list = []
    for c in checkin_list:
        num_checkin_list.append(sum(list(c.values())))

    # When the search result lists are generated.
    laglng_list = [[b['name'], b['latitude'], b['longitude']] for b in business_list]
    result_list = list()
    for idx in range(0, len(business_list)):
        result = dict()
        result['category'] = category_list[idx]
        result['business'] = business_list[idx]
        result['num_checkin'] = num_checkin_list[idx]
        result['review'] = review_list[idx]
        result['user'] = user_list[idx]
        result_list.append(result)

    return render_template(u'search.html',
        business = business_list[0] if len(business_list) > 0 else None,
        result_list=result_list,
        laglng_list=laglng_list)
