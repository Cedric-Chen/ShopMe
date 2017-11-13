#!/usr/bin/python
# -*- coding: utf-8 -*-

class MetaDatabase(dict):
    def __init__(self, cls):
        self.MetaDB_name = cls.__class__.__name__.lower()
        self.MetaDB_relational = u'mysql'

    def schema2dict(self, key):
        raise Exception(u'impletment schema2dict for current database ' \
            + u'table/collection/graph')

    def delete(self, query):
        raise Exception(u'impletment DELETE for current relational database')

    def insert(self, query):
        raise Exception(u'impletment INSERT for current relational database')

    def select(self, query):
        raise Exception(u'impletment SELECT for current relational database')

    def update(self, query):
        raise Exception(u'impletment UPDATE for current relational database')
