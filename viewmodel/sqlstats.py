#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading


from config import config_db
from viewmodel.sqltransact import SQLTransaction


class SQLStats(dict):

    def __init__(self):
        sql = u'SHOW PROCEDURE STATUS WHERE db = "%s";' \
            % (config_db[u'database'])
        self.__sp_name = [item[1] for item \
            in SQLTransaction([1], [sql], False).run().results[0] \
                if item[2] == u'PROCEDURE' \
            ]

    def refresh(self):
        for name in self.__sp_name:
            thread = threading.Thread(target=sql_stats.run, args=(name))
            thread.start()

    def run(self, name):
        sql = u'call %s();' % (name)
        ret = SQLTransaction([1], [sql], False).run()
        self[name] = ret.results[0][0]


sql_stats = SQLStats()
sql_stats.refresh()
