#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, url_for, redirect, render_template
from config import app, log_dir

# from config import app, app_debug, log_dir
# from www import url
# import sys
# sys.path.append('../')
# from datamodel_test.business import model as Business
# from datamodel_test.review import model as Review
# from datamodel_test.user import model as User
# from datamodel_test.checkin import model as Checkin
# from datamodel_test.category import model as Category

from datamodel.business import business
from datamodel.review import review
from datamodel.user import user
from datamodel.checkin import checkin
from datamodel.category import category

app = Flask(__name__)

@app.route(u'/search/')
def search():
    business_id = request.args.get('business_id')
    # for datamodel_test
    # d = {Business.get_business()['id']:Business.get_business()}
    # business_item = d[business_id]
    # review_items = Review.get_review()
    # review_item = list(review_items.values())[0]
    # user_item = User.get_user()
    # checkin_item = Checkin.get_checkin()
    # category_items = list(Category.get_category().values())
    # category_string = ', '.join(category_items)

    # for datamodel
    business_item = business.select(business_id)
    review_items = list(review.select(business_id,'*').values())[0]
    review_item = list(review_items.values())[0]
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
    category_list = [category_string for i in range(num_item)]

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


if __name__ == '__main__':
    app.run()
