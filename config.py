#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from config_override import app_debug, override_db


config_db = { 
    u'user': u'user',
    u'password': u'password',
    u'database': u'database',
    u'host': u'127.0.0.1',
    u'port': 3306,
    u'use_unicode': True,
    u'charset': u'utf8',
    u'collation': u'utf8_general_ci',
    u'autocommit': True,
    u'buffered': True,
}

for k, v in config_db.items():
    config_db[k] = override_db.get(k, v)

# create Flask app
from flask import Flask
app = Flask(__name__)
app.debug = app_debug
app.config['SECRET_KEY'] = 'nooneknows'

# directory
app_dir = os.path.dirname(__file__)
app_name = os.path.basename(app_dir)
log_dir = os.path.normpath(os.path.join(app_dir, u'./log'))
