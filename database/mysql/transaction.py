#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from config import app
from database.mysql.engine import DbCtx


class Transaction(dict):

    def __init__(self):
        self.transact = 0
        self.__dbctx = DbCtx()
        self.__cursor = self.__dbctx.cursor()
        self.__stack = list()
        self.results = list()
        self.__cmd_st = list()
        self.commands = list()
        self.failed = None

    def prepared(self):
        self.__cursor = self.__dbctx.prepared().cursor()
        return self

    def __enter__(self):
        self.transact += 1
        ctx = list()
        if self.transact == 1:
            self[u'transaction'] = self.transact
            self[u'context'] = ctx
        else:
            self.__stack[-1].append({
                u'transaction': self.transact,
                u'context': ctx,
                })
        self.__stack.append(ctx)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        message = {
            u'exc_type': None,
            u'exc_value': None,
            u'traceback': None,
            u'action': None,
        }
        if exc_type:
            message[u'exc_type'] = exc_type
            message[u'exc_value'] = exc_value
            message[u'traceback'] = traceback
            message[u'action'] = u'Rollback'
            self.__dbctx.rollback()
            if not self.failed:
                self.failed = message
            app.logger.debug(u'[ROLLBACK] TRANSACTION %s, %s' \
                % (self.transact, message))
        else:
            message[u'exc_value'] = u'Succeeded'
            message[u'action'] = u'Commit'
            self.__dbctx.commit()
            app.logger.debug(u'[COMMIT] TRANSACTION %s: %s' \
                % (self.transact, message))
        self.__stack[-1].append(message)
        self.__stack.pop()
        while self.__cmd_st and self.__cmd_st[-1][0] == self.transact:
            self.__cmd_st.pop().insert(1, message[u'action'])
        self.transact -= 1
        if not self.transact:
            self.__dbctx.cleanup()

    def execute(self, sql, placeholder):
        sql = sql.strip()
        cmd = [self.transact, sql, placeholder]
        self.__cmd_st.append(cmd)
        self.commands.append(cmd)
        app.logger.debug(u'[EXECUTE] %s' % (cmd))
        if re.match(r'^CALL', sql, re.IGNORECASE):
            sql = sql.lower().split('CALL ')[1].strip().split('()')[0]
            self.__cursor.callproc(sql, placeholder)
            self.results.append([ret.fetchall() \
                for ret in self.__cursor.stored_results()])
        else:
            self.__cursor.execute(sql, placeholder)
            try:
                ret = self.__cursor.fetchall()
            except:
                ret = []
            self.results.append(ret)
        return self
