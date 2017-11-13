#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from config import app, log_dir
from flask import render_template, redirect, url_for, request
# from flask_sqlalchemy import SQLAlchemy
# from flask.ext.security import Security, SQLAlchemyUserDatastore, \
#     UserMixin, RoleMixin, login_required

# back-end function
from datamodel.business import model as Business
from datamodel.attribute import model as Attribute
from datamodel.category import model as Category
from datamodel.hours import model as Hours
from datamodel.photo import model as Photo
from datamodel.user import model as User
from datamodel.friend import model as Friend


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

from viewmodel.pagination import Pagination

@app.route(u'/log/')
def log():
    file_list = []
    for file in os.listdir(log_dir):
        file_list.append(os.path.basename(file))
    return u'%s/\n    %s'\
        % (os.path.basename(log_dir), u'\n    '.join(file_list))

@app.route(u'/log/<string:filename>:<int:max_lines>/')
@app.route(u'/log/<string:filename>/')
# @app.route(u'/log/<string:filename>/', defaults ={u'max_lines': 100})
# def log_file(filename, max_lines):
# using defaults will cause url re-write
def log_file(filename, max_lines=100):
    for file in os.listdir(log_dir):
        if filename == os.path.basename(file):
            with open(os.path.join(log_dir, file), u'r') as f:
                count = 0
                re_lines = []
                for line in reversed(f.readlines()):
                    re_lines.append(line)
                    count += 1
                    if count == max_lines:
                        break
                return u''.join(re_lines)
    return u'File %s Not Found' % (filename)

@app.route(u'/information/')
@app.route(u'/information/<business_id>/')
def information(business_id):
    _attribute_ = attribute.select(business_id)
    _business = business.select(business_id)
    _category = category.select(business_id)
    _checkin = checkin.select(business_id)
    _hours = hours.select(business_id)
    _review = review.select(business_id, u'*')
    pagination = Pagination(u'review', 4, len(_review), 5)
    return render_template(u'information.html', business=_business, category=_category, \
        hours=_hours, review=_review, pagination=pagination)


# friends = Friend.get_friend()
# Me = User.get_user()


@app.route('/user/<user_id>')
def user(user_id):
    friends = {}
    for id in Friend.select(user_id):
        friend = User.select(id)
        if 'name' in friend:
            friends[id] = friend
    return render_template('user.html',
                           user=User.select(user_id),
                           friend=friends
                           )


@app.route('/friend')
def friend():
    url_for('static', filename='css/user.css')
    return render_template('friend.html',
                           user=User.get_user()
                           )


@app.route('/friend/remove/<friend_id>/<id>')
def remove_friend(friend_id, id):
    Friend.delete(id, [friend_id])


@app.route('/friend/add/<friend_id>/<id>')
def add_friend(friend_id, id):
    Friend.insert(id, [friend_id])

@app.route('/update/name/<name>/<id>')
def update_name(name, id):
    User.update(id,{"name":name})
    # Me["name"] = name
    pass
