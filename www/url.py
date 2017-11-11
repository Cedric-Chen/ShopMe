#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask import render_template
from config import app, log_dir

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

from datamodel.attribute import model as attribute_m
from datamodel.business import model as business_m
from datamodel.category import model as category_m
from datamodel.checkin import model as checkin_m
from datamodel.elite_years import model as elite_years_m
from datamodel.friend import model as friend_m
from datamodel.hours import model as hours_m
from datamodel.photo import model as photo_m
from datamodel.review import model as review_m
from datamodel.tip import model as tip_m
from datamodel.user import model as user_m

@app.route(u'/information/')
@app.route(u'/information/<business_id>/')
def information(business_id=None):
    if business_id is None:
        business_id = u'*'
    attribute = attribute_m.get_attribute(business_id)
    business = business_m.get_business(business_id)
    category = category_m.get_category(business_id)
    checkin = checkin_m.get_checkin(business_id)
    hours = hours_m.get_hours(business_id)
    if len(business) == 0:
        return information(u'--9QQLMTbFzLJ_oT-ON3Xw')
    return render_template(u'information.html', business=business, category=category, hours=hours)
