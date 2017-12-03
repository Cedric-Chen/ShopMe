#!/usr/bin/python
# -*- coding: utf-8 -*-

from databas.mysql.engine import DbCtx


class Transation(dict):

    def __init__(self):
        self.__transaction = 0
        self.__dbctx = DbCtx()
        self.__stack = list()

    def __enter__(self):
        self.__transaction += 1
        ctx = list()
        if self.__transaction == 1:
            self[u'transaction'] = self.__transaction
            self[u'context'] = ctx
        else:
            self.__stack[-1].append({
                u'transaction': self.__transaction,
                u'context': ctx,
                })
        self.__stack.append(ctx)
        return self.__dbctx.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        message = {
            'exc_type': None,
            'exc_value': None,
            'traceback': None,
            'action': None,
        }
        if exc_type:
            message[u'exc_type'] = exc_type
            message[u'exc_value'] = exc_value
            message[u'traceback'] = traceback
            message[u'message'] = u'Rollback'
            self.__dbctx.rollback()
        else:
            message[u'exc_value'] = u'Succeeded'
            message[u'action'] = u'Commit'
            self.__dbctx.commit()
        self.__stack[-1].append(message)
        self.__stack.pop()
        self.__transaction -= 1
        if not self.__transaction:
            self.__dbctx.clean()
