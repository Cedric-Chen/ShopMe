#!/usr/bin/python
# -*- coding: utf-8 -*-

import ast

from flask import Flask, redirect, render_template, request, \
     session, url_for, flash, abort, Response
from flask.ext.login import LoginManager, UserMixin, login_required, \
    login_user, logout_user, current_user

from config import app
from datamodel.account_user import account_user

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
   
    status, info = account_user.check(username, password)
    if status:
        user = User(username)
        login_user(user)
    return redirect(request.args.get('next') or \
	request.referrer or \
	url_for('index'))

    flash(info)
    return redirect(request.args.get('next') or \
	request.referrer or \
	url_for('index'))
   
#    from databse.datamodel import DataModel
#    cur.execute("SELECT COUNT(1) FROM account_user WHERE username = %s;", \
#        [username_form]) # CHECKS IF USERNAME EXSIST
#    if cur.fetchone()[0]:
#        cur.execute("SELECT password FROM account_user \
#            WHERE username = %s;", 
#            [username_form]) # FETCH THE HASHED PASSWORD
#        for row in cur.fetchall():
#            if md5(password_form).hexdigest() == row[0]:
#                session['username'] = request.form['username']
#                return redirect(url_for('index'))
#            else:
#                error = "Invalid Credential"
#    else:
#        error = "Invalid Credential"
#    flask.flash(error)
#    return render_template('login.html', error=error)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
#    return Response('<p> Logged out </p>')
#    session.pop('username', None)
    return redirect(url_for('index'))

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(username):
    return User(username)
