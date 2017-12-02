#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template,request
import requests, json
from config import app

# other views
@app.route('/')
@app.route('/index/')
def index():
    user_ip = request.access_route[-1]
    print(request.access_route)
    user_loc = json.loads(requests.get('https://ipinfo.io/%s/geo' % (user_ip)).content)
    print(user_loc)
    user_loc = user_loc['loc']
    return render_template('index.html', userloc = user_loc)

# only for modifying front-end page
@app.route('/profile')
def profile():
    user = 'Cedric'
    return render_template('profile.html',
        title='Cedric is awesome!',
        user=user
    )
