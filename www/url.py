#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask import request, url_for
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
    if u':' not in request.url:
        url_for(u'log_file', filename=filename, max_lines=max_lines)
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
