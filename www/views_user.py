#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template, url_for

from config import app
from datamodel.attribute import attribute
from datamodel.business import business
from datamodel.category import category
from datamodel.checkin import checkin
from datamodel.elite_years import elite_years
from datamodel.friend import friend
from datamodel.hours import hours
from datamodel.photo import photo
from datamodel.review import review
from datamodel.tip import tip
from datamodel.user import user

@app.route('/user/<user_id>')
def view_user(user_id):
    friends = {}
    for one_id in friend.select(user_id):
        friend_dict = user.select(one_id)
        if 'name' in friend_dict:
            friends[one_id] = friend_dict
    return render_template('user.html',
        user=user.select(user_id),
        friend=friends
    )

@app.route('/friend')
def view_friend():
    url_for('static', filename='css/user.css')
    return render_template('friend.html',
        user=user.select("user_id not defined"),
    )

@app.route('/friend/remove/<friend_id>/<user_id>')
def remove_friend(friend_id, user_id):
    friend.delete(user_id, {friend_id:user_id})

@app.route('/friend/add/<friend_id>/<user_id>')
def add_friend(friend_id, user_id):
    friend.insert(user_id, {friend_id:user_id})

@app.route('/update/name/<name>/<user_id>')
def update_name(name, user_id):
    user.update(user_id,{"name":name})
