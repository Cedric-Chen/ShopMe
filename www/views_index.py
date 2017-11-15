#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template

from config import app

# other views
@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')

# only for modifying front-end page
@app.route('/profile')
def profile():
    user = 'Cedric'
    return render_template('profile.html',
        title='Cedric is awesome!',
        user=user
    )
