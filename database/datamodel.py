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

    # single select delete, insert, update with commit
    def commit(self):
        if self.db == self.MetaDB_relational:
            super().commit(self.query_sql)

    # single select delete, insert, update only
    def execute(self):
        if self.db == self.MetaDB_relational:
            return super().execute(self.query_sql)


class DataModelCounter(set):
    def __init__(self):
        self.datamodel = 0

    def check(self):
        app.logger.info(u'PHYSICALMODEL -> DATAMODEL: Initialized Count: %d'
            % (self.datamodel))
        for name in metatable:
            if name not in self:
                app.logger.warning(u'NOT FOUNT DATAMODEL: %s' % (name))

dmcounter = DataModelCounter()
