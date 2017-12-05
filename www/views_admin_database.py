#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template,request, session, url_for, redirect, flash
from flask_login import login_required
import requests, json
from config import app
from decimal import Decimal

@login_required
@app.route('/admin/database/')
def admin_database(commands={}, results={}):
    if  'account_type' in session and session['account_type'] == 'admin':
        return render_template(
            'admin_database.html',
            commands = commands,
            results = results
        )
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('index'))

@login_required
@app.route('/admin/database/do/', methods=['POST'])
def admin_database_do():
    if  'account_type' in session and session['account_type'] == 'admin':
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
            url_for('index'))

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

