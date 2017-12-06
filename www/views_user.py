#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template, url_for, session, request
from flask_login import login_required

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
from datamodel.frequentpattern import frequentpattern
from viewmodel.pagination import Pagination
from utility.lrudecorator import LRUDecorator

FRIEND_PERPAGE = 5
FRIEND_PAGES = 5


def get_recommendation(user_id):
    reviews = review.select('*',user_id)
    print(len(reviews))
    blist = [reviews[k]['business_id'] for k in reviews if reviews[k]['stars'] >= 4 ]
    blist = list(set(blist))
    return get_recommendation(blist)

@LRUDecorator(50)
def friend_result(user_id):
    friends = []
    for one_id in friend.select(user_id):
        friend_dict = user.select(one_id)
        if 'name' in friend_dict:
            friends.append(friend_dict)
    return friends


@login_required
@app.route('/user/profile')
def view_user():
    user_id = session['id']
    if 'account_type' in session and \
        session['account_type'] == 'user':
        friendlist = friend_result(user_id)
        friend_pagination = Pagination(u'friend', len(friendlist), \
            FRIEND_PERPAGE, FRIEND_PAGES)
        friend_pagination.jump(request.args.get('page', 1))
        friendlist = friendlist[ \
            friend_pagination['start']: friend_pagination['end']]
        print(friend_pagination)
        recommendations = get_recommendation(user_id)
        return render_template('user.html',
            user=user.select(user_id),
            friendlist=friendlist,
            pagination=friend_pagination,
            recommendations = recommendations
        )
    else:
        return redirect(request.args.get('next') or \
            request.referrer or \
            url_for('index'))

@login_required
@app.route('/friend')
def view_friend():
    url_for('static', filename='css/user.css')
    return render_template('friend.html',
        user=user.select("user_id not defined"),
    )

@login_required
@app.route('/friend/remove/<friend_id>/<user_id>')
def remove_friend(friend_id, user_id):
    friend.delete(user_id, {friend_id:user_id})

@login_required
@app.route('/friend/add/<friend_id>/<user_id>')
def add_friend(friend_id, user_id):
    friend.insert(user_id, {friend_id:user_id})

@login_required
@app.route('/update/name/<name>/<user_id>')
def update_name(name, user_id):
    user.update(user_id,{"name":name})
