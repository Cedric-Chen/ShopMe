#!/usr/bin/python
# -*- coding: utf-8 -*-

import mysql.connector, threading
from config import app

database = None

class _Engine(object):
    def __init__(self, connect):
        self.__connect = connect
    def connect(self):
        return self.__connect()

def create_database(kwargs):
    global database
    if database:
        return
    database = _Engine(lambda: mysql.connector.connect(**kwargs))
    app.logger.info(u'[INIT] mysql database <%s> ok, user=%s, database=%s' \
        %(hex(id(database)), kwargs[u'user'], kwargs[u'database']))

class _Connection(object):
    def __init__(self):
        self.__conn = None

    def cleanup(self):
        if self.__conn:
            app.logger.debug(u'[CONNECTION] <%s> CLOSE' % hex(id(self.__conn)))
            self.__conn.close()
            self.__conn = None

    def commit(self):
        if self.__conn:
            app.logger.debug('[CONNECTION] <%s> COMMIT' % hex(id(self.__conn)))
            self.__conn.commit()

    def cursor(self):
        if self.__conn is None:
            self.__conn = database.connect()
            app.logger.debug('[CONNECTION] <%s> OPEN' % hex(id(self.__conn)))
        return self.__conn.cursor()

    def rollback(self):
        if self.__conn:
            self.__conn.rollback()
            app.logger.debug('[CONNECTION] <%s> ROLLBACK' % hex(id(self.__conn)))

class DbCtx(threading.local):
    # define short cut for all the available db operations
    def __init__(self):
        self.__conn = _Connection()

    def __call__(self):
        return self

    def __enter__(self):
        return self.__conn.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()

    def cleanup(self):
        self.__conn.cleanup()
        self.__conn = None

    def commit(self):
        self.__conn.commit()
        return self

    def cursor(self):
        return self.__conn.cursor()

    def rollback(self):
        self.__conn.rollback()
        return self
