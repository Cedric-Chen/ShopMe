#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template,request, session, url_for, redirect, flash
from flask_login import login_required
import requests, json
from config import app
from decimal import Decimal

@login_required
@app.route('/admin/stastics/')
def admin_stastics():
    if  'account_type' in session and session['account_type'] == 'admin':
        categories = ['state_checkin', 'state_is_open',
            'state_review_count', 'state_stars']

        from viewmodel.sqlstats import sql_stats
        if sql_stats != {}:
            with open('/home/ShopMe/viewmodel/sqlstats_sample.json','w') as f:
                json.dump(sql_stats,f,default=default)
        data = \
            json.load(open('/home/ShopMe/viewmodel/sqlstats_sample.json'))

        state_is_open = data['state_is_open'] 
        state_review_count = data['state_review_count']
        state_stars = data['state_stars']
        state_checkin = data['state_checkin']

        return render_template(
            'admin_stastics.html',
            state_is_open = state_is_open,
            state_review_count = state_review_count,
            state_stars = state_stars,
            state_checkin = state_checkin
        )
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('index'))

def default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)
