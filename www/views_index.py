#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template,request, session
from flask_login import login_required
import requests, json
from config import app

# other views
@app.route('/')
@app.route('/index/')
def index():
    # user_ip = request.remote_addr
    # user_loc = json.loads(requests.get('https://ipinfo.io/%s/geo' % (user_ip)).content)['loc']
    from datamodel.review import review
    return render_template(
        'index.html', 
        reviews = review.select_top_review()
    )

# only for modifying front-end page
@app.route('/profile')
def profile():
    user = 'Cedric'
    return render_template('profile.html',
        title='Cedric is awesome!',
        user=user
    )
