#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template, session
from flask.ext.login import login_required

from www.tools import is_account_a_business

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

@login_required
@app.route(u'/merchant/information/')
def view_merchant_info():
    if is_account_a_business():
        business_id = session['id']
        _attribute_ = attribute.select(business_id)
        _business = business.select(business_id)
        _category = category.select(business_id)
        _checkin = checkin.select(business_id)
        _hours = hours.select(business_id)
        _review = review.select(business_id, u'*')
        pagination = Pagination(u'review', 4, len(_review), 5)
        return render_template(u'information.html', business=_business, \
            category=_category, hours=_hours, review=_review, pagination=pagination)
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('index'))
