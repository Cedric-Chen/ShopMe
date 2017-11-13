#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import __init__

from flask import render_template
from config import app, app_debug, log_dir
from www.url import *
from www import assets

import views

@app.route(u'/hello_world/')
@app.route(u'/hello_world/<name>/')
def hello_world(name=None):
    return render_template(u'hello_world.html', name=name)


@app.route(u'/hello_database/')
def hello_database():
    from random import random
    from database.mysql.engine import DbCtx
    db = DbCtx()
    name_list = []
    with db() as cursor:
        cursor.execute(
            u'SELECT name FROM user WHERE review_count>=%s and review_count<=%s'
            %(3 * random(), 3 * (1 + random())))
        name_list = [x[0] for x in cursor.fetchall()]
    return u'name list:\n' + u'\n'.join(name_list[1:min(len(name_list), 50)])


@app.route(u'/hello_log/')
def hello_log():
    app.logger.error(u'This is debug log')
    app.logger.info(u'This is info log')
    app.logger.warning(u'This is warning log')
    app.logger.error(u'This is error log')
    app.logger.critical(u'This is critical log')
    return u'This is log test page'

app.logger.debug(u'ShopMe launched successfully')

if __name__ == '__main__':
    app.run(debug=app_debug)
