#!/usr/bin/python
# -*- coding: utf-8 -*-

import ast

from flask import redirect, render_template, request, session, \
    url_for, escape

#from flask_sqlalchemy import SQLAlchemy
#from flask.ext.security import Security, \
#    UserMixin, RoleMixin, login_required

from config import app

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_form  = request.form['username']
        password_form  = request.form['password']
        cur.execute("SELECT COUNT(1) FROM account_user WHERE username = %s;", 
            [username_form]) # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            cur.execute("SELECT password FROM account_user 
                WHERE username = %s;", 
                [username_form]) # FETCH THE HASHED PASSWORD
            for row in cur.fetchall():
                if md5(password_form).hexdigest() == row[0]:
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
                else:
                    error = "Invalid Credential"
        else:
            error = "Invalid Credential"
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
