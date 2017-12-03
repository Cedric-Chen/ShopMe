#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import app
from database.mysql.table import Table, metatable

class DataModel(Table):
    def __init__(self, cls):
        super().__init__(cls)
        self.init_schema(dmcounter, metatable)

    def init_schema(self, dmcounter_, metatable_):
        if self.MetaDB_name in dmcounter_:
            return
        dmcounter_.datamodel += 1
        if self.MetaDB_name in metatable_:
            self.schema2dict(self.MetaDB_name)
            app.logger.info(u'PHYSICALMODEL -> DATAMODEL: %s' \
                % (self.MetaDB_name))
            dmcounter_.add(self.MetaDB_name)
        else:
            app.logger.warning(u'NOT FOUNT PHYSICALMODEL: %s' \
                % (self.MetaDB_name))

    def basetype_sql(self, value):
        return type(value) in [bool, float, int]

    def quote_sql(self, value):
        return u'%s' % value if self.basetype_sql(value) else u"'%s'" % value

    def select_order(self, key, order):
        query_sql = ''
        if key in self.dm_attr:
            query_sql = u' ORDER BY %s ' % key
            if order < 0:
                query_sql += u' DESC'
            elif order > 0:
                query_sql += u' ASC'
        return query_sql

    def execute(self):
        # delete, insert, update
        if self.db == self.MetaDB_relational:
            query = self.query_sql
        return super().execute(query)

    def select(self):
        if self.db == self.MetaDB_relational:
            query = self.query_sql
        return super().select(query)

class DataModelCounter(set):
    def __init__(self):
        self.datamodel = 0

    def check(self):
        app.logger.info(u'PHYSICALMODEL -> DATAMODEL: Initialized Count: %d'
            % (self.datamodel))
        for name in metatable:
            if name not in self:
                app.logger.warning(u'NOT FOUNT DATAMODEL: %s'
                    % (name))

dmcounter = DataModelCounter()
