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
@app.route('/admin/stastics/')
def admin_stastics():
    if session['account_type'] == 'admin':
        return render_template(
            'admin_stastics.html',
            data = [
         ['Element', 'Density'],
         ['Copper', 8.94],        
         ['Silver', 10.49],         
         ['Gold', 19.30],
         ['Platinum', 21.45 ]
      ]
        )
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('/'))

@login_required
@app.route('/admin/database/')
def admin_database(commands={}, results={}):
    if session['account_type'] == 'admin':
        return render_template(
            'admin_database.html',
            commands = commands,
            results = results
        )
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('/'))

@login_required
@app.route('/admin/database/do/', methods=['POST'])
def admin_database_do():
    if session['account_type'] == 'admin':
        from viewmodel.sqltransact import SQLTransaction
        querys = request.form['querys']
        rb_all = request.form.get('rb_all')
        rb_all = True if rb_all=='all' else False
        transaction, sql = admin_database_parse(querys)
#        return str(transaction) + '<br>' + str(sql) + '<br>' + str(rb_all)
        sqltransaction = SQLTransaction(transaction,sql,rb_all)
        ret = sqltransaction.run()
#        return str(ret.commands) + '<br>' + str(ret.results)

        return render_template(
            'admin_database.html',
            commands = ret.commands,
            results = ret.results,
            querys = querys,
            rb_all = rb_all
        )
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('/'))

def admin_database_parse(querys):
    values = querys.split(';')
    values.pop()
    transaction = []
    sql = []
    for value in values:
        transaction.append(value.count('+') + 1)
        sql.append(
		value.replace('+','').replace('\r','').replace('\n','')+';')
    return transaction, sql

@login_required
@app.route('/admin/account/search', methods=['POST'])
@app.route('/admin/account/search/<kw>', methods=['GET'])
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
@app.route('/admin/account/delete/group/<kw>/', methods=['POST'])
def admin_account_delete_group(kw):
    if session['account_type'] == 'admin':
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
        flash(info, category='success')
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
