#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template,request, session, url_for, redirect, flash
from flask_login import login_required
import requests, json
from config import app

@login_required
@app.route('/admin/account')
def admin_account():
    if session['account_type'] == 'admin':
        return render_template(
            'admin_account.html'
        )
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('/'))

@login_required
@app.route('/admin/database')
def admin_database():
    if session['account_type'] == 'admin':
        return render_template(
            'admin_database.html'
        )
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('/'))


@login_required
@app.route('/admin/account/search/<kw>', methods=['GET'])
@app.route('/admin/account/search', methods=['POST'])
def admin_account_search(kw=None):
    if session['account_type'] == 'admin':
        from datamodel.business import business
        if not kw:
            kw = request.form['kw']
        if kw == '':
            return render_template('admin_account.html')
        cond_kw = parse_keyword(kw)
        keys = list(cond_kw.keys())

        business_list = business.sort_by( \
            cond_kw, keys, [u'=']*len(keys), u'*', u'*')
        return render_template(
            'admin_account.html',
            business_list = business_list,
            kw = kw
        )
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('/'))

@login_required
@app.route('/admin/account/delete/')
@app.route('/admin/account/delete/<kw>/<business_id>')
def admin_account_delete(kw, business_id):
    if session['account_type'] == 'admin':
        from datamodel.business import business
        business.delete(business_id,business.select(business_id))
        return redirect(url_for('admin_account_search') + '/' + kw)
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('/'))

@login_required
@app.route('/admin/account/delete/group/')
@app.route('/admin/account/delete/group/<kw>/<business_id>')
def admin_account_delete(kw, business_id):
    if session['account_type'] == 'admin':
        from datamodel.business import business
        business.delete(business_id,business.select(business_id))
        return redirect(url_for('admin_account_search') + '/' + kw)
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('/'))

@login_required
@app.route('/admin/account/update/', methods=['POST'])
@app.route('/admin/account/update/<kw>/<business_id>', methods=['POST'])
def admin_account_update(kw, business_id):
    if session['account_type'] == 'admin':
        from datamodel.account_business import account_business
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        status,info = account_business.update(business_id, new_username, new_password)
        flash(info)
        return redirect(url_for('admin_account_search') + '/' + kw)
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('/'))

def parse_keyword(kw):
    l = kw.replace(' ', '').split(',')
    d = dict()
    for x in l:
        if(len(x.split(':')) == 2):
            k = x.split(':')[0]
            v = x.split(':')[1]
            d[k] = v
    return d
