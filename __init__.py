#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging, os, sys
app_dir = u'.'
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# set up app logger
from config import app, log_dir
app.logger.setLevel(logging.NOTSET)
from filelogger import filelogger
app.logger.addHandler(filelogger(os.path.join(log_dir, u'applog')))
from datetime import datetime
app.logger.info(u'Restarting @ {}'.format(datetime.utcnow()))
from www import assets
# create database
from config import config_db
from database.mysql.engine import create_database
create_database(config_db)
sql_attr = [u'Field', u'Type', u'Null', u'Key', u'Default', u'Extra']
