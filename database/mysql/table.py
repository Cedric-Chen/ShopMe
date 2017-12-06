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

    def basetype_sql(self, value):
        return type(value) in [bool, float, int]

    def quote_sql(self, value):
        return u'%s' % value if self.basetype_sql(value) else u'"%s"' % value

    def toquery(self):
        # convert query_sql, query_args -> query_sql
        return self.query_sql \
            % tuple([self.quote_sql(value) for value in self.query_args])

    def select_order(self, key, order):
        query_sql = ''
        if key in self.dm_attr:
            query_sql = u' ORDER BY %s ' % key
            if order < 0:
                query_sql += u' DESC'
            elif order > 0:
                query_sql += u' ASC'
        return query_sql

    # single select, delete, insert, update only
    def execute(self, query):
        db = DbCtx()
        with db() as cursor:
            app.logger.debug(u'[EXECUTE] %s' % (query))
            cursor.execute(query)
            return cursor.fetchall()

    # single delete, insert, update with commit
    def commit(self, query):
        db = DbCtx()
        with db() as cursor:
            app.logger.debug(u'[COMMIT] %s' % (query))
            cursor.execute(query)
            try:
                ret = cursor.fetchall()
            except:
                ret = []
            db.commit()
            return ret


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
