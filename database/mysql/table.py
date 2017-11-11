#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import app
from __init__ import sql_attr
from database.metadatabase import MetaDatabase
from database.mysql.engine import DbCtx

class Table(MetaDatabase):
    def __init__(self, cls):
        super().__init__(cls)
        self.db = self.MetaDB_relational
        self.schema = None

    def schema2dict(self, key):
        '''
        @key: string
        '''
        assert(type(key) == str)
        self.schema = {}
        attr_list = metatable[key]
        for attr in attr_list:
            d = dict()
            for index, k_attr in enumerate(sql_attr):
                d[k_attr] = attr[index]
            self.schema[key] = d

    def execute(self, query):
        db = DbCtx()
        with db() as cursor:
            app.logger.info(u'[EXECUTE] %s' % (query))
            cursor.execute(query)

    def select(self, query):
        db = DbCtx()
        with db() as cursor:
            app.logger.info(u'[SELECT] %s' % (query))
            cursor.execute(query)
            return cursor.fetchall()

def MetaTable():
    table = Table(Table)
    db = DbCtx()
    with db() as cursor:
        cursor.execute(u'SHOW tables')
        for item in cursor.fetchall():
            table[item[0]] = []
        for k in table:
            cursor.execute(u'SHOW COLUMNS FROM %s' % (k))
            table[k] = cursor.fetchall()
    return table

metatable = MetaTable()
