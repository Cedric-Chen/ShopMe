#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import make_response, render_template

from config import app
from datamodel.attribute import attribute
from datamodel.business import business
from datamodel.category import category
from datamodel.checkin import checkin
from datamodel.elite_years import elite_years
from datamodel.friend import friend
from datamodel.hours import hours
from datamodel.photo import photo
from datamodel.review import review
from datamodel.tip import tip
from datamodel.user import user
from viewmodel.pagination import Pagination
from utility.lrudecorator import LRUDecorator

REVIEW_PERPAGE = 3
REVIEW_PAGES = 5


@app.route(u'/information/')
@app.route(u'/information/<business_id>/')
def view_merchant_info(business_id):
    _attribute_ = attribute.select(business_id)
    _business = business.select(business_id)
    _category = category.select(business_id)
    _checkin = checkin.select(business_id)
    _hours = hours.select(business_id)
    _review = review.sort(business_id, u'*', 'date', -1)
    review_pagination = Pagination(u'review', len(_review), REVIEW_PERPAGE, \
        REVIEW_PAGES)
    print(review_pagination)
    _review = _review[review_pagination['start']: review_pagination['end']]
    return render_template(u'information.html', business=_business, \
        category=_category, hours=_hours, review=_review, \
        pagination=review_pagination)


@LRUDecorator(50)
def review_result(business_id, field, order):
    return review.sort(business_id, u'*', field, int(order))


@app.route(u'/information/review/')
@app.route(u'/information/review/<business_id>:<page>:<field>:<order>/')
def review_board(business_id, page, field, order):
    _business = business.select(business_id)
    _review = review_result(business_id, field, order)
    review_pagination = Pagination(u'review', len(_review), REVIEW_PERPAGE, \
        REVIEW_PAGES)
    review_pagination.jump(page)
    _review = _review[review_pagination['start']: review_pagination['end']]
    return render_template(u'review_board.html', business=_business, \
        review=_review, pagination=review_pagination)

@app.route(u'/information/review/update/')
@app.route(u'/information/review/update/<business_id>:<review_id>:<field>:<value>/')
def review_update(business_id, review_id, field, value):
    current_review = review.select(business_id, u'*')
    new_review = dict()
    new_review[field] = current_review[review_id][field] + int(value)
    review.update(business_id, current_review[review_id][u'user_id'], \
        {review_id: new_review}, {review_id: current_review[review_id]})
    return make_response(u'succeed', 200)
