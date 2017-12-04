#!/usr/bin/python
# -*- coding: utf-8 -*-

import ast

from flask import Flask, redirect, render_template, request, \
     session, url_for, flash, abort, Response
from flask.ext.login import LoginManager, UserMixin, login_required, \
    login_user, logout_user, current_user

from config import app
from datamodel.account_user import account_user
from datamodel.account_business import account_business

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# user model
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

@app.route('/login/')
def login():
    error = None
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/login/check_user/', methods=['GET','POST'])
def check_user():
    username = request.form['username']
    password = request.form['password']

    if username=='admin' and password =='admin':
        session['account_type'] = 'admin'
        user = User('admin')
        login_user(user)
        return redirect(request.args.get('next') or \
	    request.referrer or \
	    url_for('index'))

    try:
        account_type = request.form['account_type']
    except:
        flash('Please choose an account type.')
        return redirect(request.args.get('next') or \
	request.referrer or \
	url_for('index'))

    if account_type == 'user':   
        status, info = account_user.check(username, password)
    else:
        status, info = account_business.check(username, password)

    if status:
        user = User(username)
        login_user(user)
        session['account_type'] = account_type
        if account_type == 'user':
            session['id'] = account_user.get_id(username)
        else:
            session['id'] = account_business.get_id(username)
        return redirect(request.args.get('next') or \
	    request.referrer or \
	    url_for('index'))

    flash(info)
    return redirect(request.args.get('next') or \
	request.referrer or \
	url_for('index'))

@app.route('/login/register_user/', methods=['GET','POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    try:
        account_type = request.form['account_type']
    except:
        flash('Please choose an account type.')
        return redirect(request.args.get('next') or \
	request.referrer or \
	url_for('index'))

    if account_type == 'user':   
        status, info = account_user.insert(username, password)
    else:
        status, info = account_business.insert(username, password)

    if status:
        flash(info)
        return redirect(request.args.get('next') or \
	    request.referrer or \
	    url_for('index'))
    else:
        flash(info)
        return redirect(request.args.get('next') or \
	    request.referrer or \
	    url_for('index'))

@app.route('/logout/')
@login_required
def logout():
    logout_user()
#    return Response('<p> Logged out </p>')
    session.pop('account_type', None)
    session.pop('id', None)
    return redirect(url_for('index'))

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(username):
    return User(username)
