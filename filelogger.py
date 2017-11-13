#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import TimedRotatingFileHandler
from flask import request

class RequestFormatter(logging.Formatter):
    def format(self, record):
        try:
            record.url = request.url
            record.remote_addr = request.remote_addr
        except RuntimeError:
            record.url = '*'
            record.remote_addr = u'*.*.*.*'
        return super().format(record)

def filelogger(filename):
    file_handler = TimedRotatingFileHandler(filename, when=u'H', interval=1,
        backupCount=0, encoding=u'utf-8', delay=False, utc=False, atTime=None)
    file_handler.setFormatter(
        RequestFormatter(
            u'[%(asctime)s %(levelname)s %(process)d-%(thread)d]: '
            u'%(remote_addr)s REQUESTED %(url)s\n'
            u'MESSAGE %(message)s IN %(pathname)s:%(lineno)d'
        )
    )
    # Text logging level for the message
    # ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
    file_handler.setLevel(logging.NOTSET)
    return file_handler
