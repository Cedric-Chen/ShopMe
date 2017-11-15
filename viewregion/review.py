#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import make_response, render_template
from config import app

from datamodel.business import business
from datamodel.review import review

from viewmodel.pagination import Pagination

review_pagination = None
review_perpage = 4
review_pages = 5

@app.route(u'/information/review/sort/')
@app.route(u'/information/review/sort/<business_id>:<field>:<order>/')
def review_sort(business_id, field=u'date', order=u'-1'):
    global review_pagination
    _business = business.select(business_id)
    _review = review.sort(business_id, u"*", field, int(order))
    _review = {no: val for no, val in enumerate(_review)}
    review_pagination = Pagination(u'review', review_perpage, len(_review), \
        review_pages)
    return render_template(u'review_board.html', business=_business, \
        review=_review, pagination=review_pagination)

@app.route(u'/information/review/update/')
@app.route(u'/information/review/update/<business_id>:<review_id>:<field>:<value>/')
def review_update(business_id, review_id, field='date', value=1):
    current_review = review.select(business_id, u'*')
    if len(current_review) == 0:
        return make_response(u'succeed', 406)
    return make_response(u'succeed', 200)

@app.route(u'/information/review/')
@app.route(u'/information/review/<business_id>:<page>/')
def review_board(business_id, page_no):
    global review_pagination
    if not review_pagination:
        _review = review.select(business_id, u"*")
        review_pagination = Pagination(u'review', review_perpage, \
            len(_review), review_pages)
    else:
        review_pagination.jump(page_no)
    return render_template(u'review_board.html', review=_review, 
        pagination=review_pagination)
