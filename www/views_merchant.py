#!/usr/bin/python
# -*- coding: utf-8 -*-

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
def view_merchant():

    merchant.business    = business.select(business_id)
    merchant.attribute   = attribute.slect(business_id)
    merchant.category    = category.select(business_id)
    merchant.hours       = hours.select(business_id)
    merchant.photo       = photo.select(business_id)

    return render_template(
        'merchant.html',
        business = merchant.business,
        attribute= merchant.attribute,
        category = merchant.category,
        hours    = merchant.hours,
        photo    = merchant.photo
    )

@app.route('/merchant/update_info/', methods=['POST'])
def update_merchant_info():
    business = {}

    newname = request.form['newname']
    if newname != '' and newname != merchant.business['name']:
        business['name'] = newname

    newopenornot = request.form.get('newopenornot')
    if newopenornot:
        if not merchant.business['is_open']:
            business['is_open'] = 1
    else:
        if merchant.business['is_open']:
            business['is_open'] = 0

    newstreet = request.form['newstreet']
    if newstreet != '' and newstreet != merchant.business['address']:
        business['address'] = newstreet
    newcity = request.form['newcity']
    if newcity != '' and newcity != merchant.business['city']:
        business['city'] = newname
    newstate = request.form['newstate']
    if newstate != '' and newstate != merchant.business['state']:
        business['state'] = newstate
    newneighborhood = request.form['newneighborhood']
    if newneighborhood != '' and newneighborhood != merchant.business['neighborhood']:
        business['neighborhood'] = newneighborhood
    newpostal_code = request.form['newpostal_code']
    if newpostal_code != '' and newpostal_code != merchant.business['postal_code']:
        business['postal_code'] = newpostal_code
    newlatitude = request.form['newlatitude']
    if newlatitude != '' and newlatitude != merchant.business['latitude']:
        business['latitude'] = newlatitude
    newlongitude = request.form['newlongitude']
    if newlongitude != '' and newlongitude != merchant.business['longitude']:
        business['longitude'] = newlongitude

    return redirect(request.referrer)

@app.route('/merchant/update_attr/', methods=['POST'])
def update_merchant_attr():
    attr = {}

    for field1, value1 in merchant.attribute.items():
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

    return redirect(request.referrer)

@app.route('/merchant/update_hours/', methods=['POST'])
def update_merchant_hours():
    _hours = {}
    for date in ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday']:
        newvalue = request.form[date+'_start_at'] + '-' + \
            request.form[date+'_end_at']
        if newvalue != '-' and newvalue != merchant.hours[date]:
            _hours[date] = newvalue

    return redirect(request.referrer)
