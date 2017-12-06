#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests, json
from decimal import Decimal
from flask import render_template,request, session, url_for, redirect, flash
from flask_login import login_required

from config import app


@login_required
@app.route('/admin/account')
def admin_account():
    if 'account_type' in session and session['account_type'] == 'admin':
        return render_template(
            'admin_account.html'
        )
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('index'))

@login_required
@app.route('/admin/account/search', methods=['POST'])
@app.route('/admin/account/search/<kw>', methods=['GET'])
def admin_account_search(kw=None):
    if  'account_type' in session and session['account_type'] == 'admin':
        from datamodel.business import business
        kw = request.form.get('kw', kw)
        cond_kw, op_list = parse_keyword(kw)
        if not kw:
            return render_template('admin_account.html')
        if not cond_kw:
            return render_template('admin_account.html', kw = kw)

        business_list = business.sort_by( \
            cond_kw, list(cond_kw.keys()), op_list, u'*', u'*')
        return render_template(
            'admin_account.html',
            business_list = business_list,
            kw = kw
        )
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('index'))

@login_required
@app.route('/admin/account/delete/')
@app.route('/admin/account/delete/<kw>/<business_id>')
def admin_account_delete(kw, business_id):
    if  'account_type' in session and session['account_type'] == 'admin':
        from datamodel.business import business
        business.delete(business_id,business.select(business_id))
        return redirect(url_for('admin_account_search') + '/' + kw)
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('index'))

@login_required
@app.route('/admin/account/delete/group/')
@app.route('/admin/account/delete/group/<kw>/', methods=['POST'])
def admin_account_delete_group(kw):
    if  'account_type' in session and session['account_type'] == 'admin':
        for key, value in request.form.to_dict().items():
            business_ids_str = key
            from datamodel.business import business
            for business_id in business_ids_str.split('~'):
                business.delete(business_id,business.select(business_id))
            flash('Delete group succeeds.', category='success')
        return redirect(url_for('admin_account_search') + '/' + kw)
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('index'))

@login_required
@app.route('/admin/account/update/', methods=['POST'])
@app.route('/admin/account/update/<kw>/<business_id>', methods=['POST'])
def admin_account_update(kw, business_id):
    if  'account_type' in session and session['account_type'] == 'admin':
        from datamodel.account_business import account_business
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        status,info = account_business.update(business_id, new_username, new_password)
        flash(info, category='success')
        return redirect(url_for('admin_account_search') + '/' + kw)
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('index'))

def parse_keyword(kw):
    l = kw.replace('  ', ' ').split(',')
    d = dict()
    op_list = list()
    for x in l:
        for op in ['<=', '>=', '!=', '<>', '=', '<', '>']:
            if(len(x.split(op)) == 2):
                k = x.strip().split(op)[0].strip()
                v = x.strip().split(op)[1].strip()
                d[k] = v
                op_list.append(op)
                break
    return d, op_list

