#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.mysql.transaction import Transaction

class SQLTransaction(object):
    def __init__(self, transaction, sql, rb_all):
        self.transact = transaction
        self.sql = sql
        self.__tctx = Transaction()
        self.__rb_all = rb_all

    def run(self):
        if self.__rb_all:
            try:
                self.rb_all(0)
            except:
                pass
        else:
            self.rb_current(0)
        return self.__tctx

    def rb_all(self, index):
        with self.__tctx as curser:
            while index < len(self.transact):
                tran_no = self.transact[index]
                print(tran_no)
                if tran_no == self.__tctx.transact:
                    curser.execute(self.sql[index], tuple())
                    index += 1
                elif tran_no < self.__tctx.transact:
                    return index
                else:
                    index = self.rb_all(index)
        return index

    def rb_current(self, index):
        try:
            with self.__tctx as curser:
                while index < len(self.transact):
                    tran_no = self.transact[index]
                    if tran_no == self.__tctx.transact:
                        curser.execute(self.sql[index], tuple())
                        index += 1
                    elif tran_no < self.__tctx.transact:
                        return index
                    else:
                        index = self.rb_current(index)
        except:
            pass
        return index
