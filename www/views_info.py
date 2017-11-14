#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template

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

@app.route(u'/information/')
@app.route(u'/information/<business_id>/')
def information(business_id):
    _attribute_ = attribute.select(business_id)
    _business = business.select(business_id)
    _category = category.select(business_id)
    _checkin = checkin.select(business_id)
    _hours = hours.select(business_id)
    _review = review.select(business_id, u'*')
    pagination = Pagination(u'review', 4, len(_review), 5)
    return render_template(u'information.html', business=_business, \
        category=_category, hours=_hours, review=_review, pagination=pagination)
