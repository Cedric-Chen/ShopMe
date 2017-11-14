#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template

from config import app
from datamodel.business import business
from datamodel.category import category
from datamodel.checkin import checkin
from datamodel.review import review
from datamodel.user import user

@app.route(u'/search/<business_id>/')
def search(business_id):
    # for datamodel
    business_item = business.select(business_id)
    review_items = review.select(business_id,'*')
    keys = list(review_items.keys())
    review_item = review_items[keys[0]]
    user_id = review_item['user_id']
    user_item = user.select(user_id)
    checkin_item = checkin.select(business_id)
    category_item = category.select(business_id)

    # For now, the searched kw is business_id only, so the lists below are generated
    # by using this only one result.
    num_item = 1
    business_list = [business_item for i in range(num_item)]
    review_list = [review_item for i in range(num_item)]
    user_list = [user_item for i in range(num_item)]
    checkin_list = [checkin_item for i in range(num_item)]
    num_checkin_list = []
    for c in checkin_list:
        num_checkin_list.append(sum(list(c.values())))
    category_list = [category_item for i in range(num_item)]

    # When the search result lists are generated.
    laglng_list = [[b['name'], b['latitude'], b['longitude']] for b in business_list]
    result_list = list()
    for idx in range(num_item):
        result = dict()
        result['business'] = business_list[idx]
        result['review'] = review_list[idx]
        result['user'] = user_list[idx]
        result['num_checkin'] = num_checkin_list[idx]
        result['category'] = category_list[idx]
        result_list.append(result)

    return render_template(u'search.html',
                            result_list=result_list,
                            laglng_list=laglng_list)
