#!/usr/bin/python
# -*- coding: utf-8 -*-

import ast

from flask import redirect, render_template, request
#from flask_sqlalchemy import SQLAlchemy
#from flask.ext.security import Security, SQLAlchemyUserDatastore,\
#    UserMixin, RoleMixin, login_required

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

@app.route('/merchant/<business_id>/')
def view_merchant(business_id):
    return render_template(
        u'merchant.html',
        attribute= attribute.select(business_id),
        business = business.select(business_id),
        category = category.select(business_id),
        hours    = hours.select(business_id),
        photo    = photo.select(business_id),
    )

@app.route('/merchant/update_info/', methods=['POST'])
def update_merchant_info():
    new_business = {}
    newname = request.form['newname']
    business_current = ast.literal_eval(request.args['business_key'])
    if newname != '' and newname != business_current['name']:
        new_business['name'] = newname

    newopenornot = request.form.get('newopenornot')
    if newopenornot:
        if not business_current['is_open']:
            new_business['is_open'] = 1
    else:
        if business_current['is_open']:
            new_business['is_open'] = 0

    newstreet = request.form['newstreet']
    if newstreet != '' and newstreet != business_current['address']:
        new_business['address'] = newstreet
    newcity = request.form['newcity']
    if newcity != '' and newcity != business_current['city']:
        new_business['city'] = newname
    newstate = request.form['newstate']
    if newstate != '' and newstate != business_current['state']:
        new_business['state'] = newstate
    newneighborhood = request.form['newneighborhood']
    if newneighborhood != '' and newneighborhood != business_current['neighborhood']:
        new_business['neighborhood'] = newneighborhood
    newpostal_code = request.form['newpostal_code']
    if newpostal_code != '' and newpostal_code != business_current['postal_code']:
        new_business['postal_code'] = newpostal_code
    newlatitude = request.form['newlatitude']
    if newlatitude != '' and newlatitude != business_current['latitude']:
        new_business['latitude'] = newlatitude
    newlongitude = request.form['newlongitude']
    if newlongitude != '' and newlongitude != business_current['longitude']:
        new_business['longitude'] = newlongitude
    business.update(business_current[u'id'], new_business, {})
    return redirect(request.referrer)

@app.route('/merchant/update_attr/', methods=['POST'])
def update_merchant_attr():
    attribute_current = ast.literal_eval(request.args[u'attr_key'])
    business_current = ast.literal_eval(request.args[u'business_key'])
    attr = {}
    for field1, value1 in attribute_current.items():
        if type(value1) == dict:
            for field2, value2 in value1.items():
                newvalue = request.form.get(field1+'_'+field2)
                if newvalue:
                    newvalue = True
                else:
                    newvalue = False
                if newvalue != value2:
                    if field1 not in attr:
                        attr[field1] = {}
                    attr[field1][field2] = newvalue
        else:
            newvalue = request.form.get(field1)
            if newvalue:
                newvalue = True
            else:
                newvalue = False
            if newvalue != value1:
                attr[field1] = newvalue
    attribute.update(business_current[u'id'], attr, {})
    return redirect(request.referrer)

@app.route('/merchant/delete_attr/', methods=['POST'])
def delete_merchant_attr():
    # need to add more delete functions
    business_current = ast.literal_eval(request.args[u'business_key'])
    attribute.delete(business_current[u'id'], {})
    return redirect(request.referrer)

@app.route('/merchant/update_hours/', methods=['POST'])
def update_merchant_hours():
    business_current = ast.literal_eval(request.args[u'business_key'])
    hours_current = ast.literal_eval(request.args[u'hours_key'])
    for date in ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday']:
        newvalue = request.form[date+'_start_at'] + '-' + \
            request.form[date+'_end_at']
        if newvalue != '-' and newvalue != hours_current[date]:
            hours_current[date] = newvalue
    hours.update(business_current[u'id'], hours_current, {})
    return redirect(request.referrer)
