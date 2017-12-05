#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMAccount_User(DataModel):
    def __init__(self, cls):
        super().__init__(cls)
        self.dm_attr = [u'username', u'userid', u'password']

#    def check_existence(self, username):
#        self.query_sql = u'SELECT count(*) FROM account_user \
#            WHERE username = "%s"' % (username)
#        ret = super().execute()
#        if ret[0]:
#            return True
#        else
#            return False

    def check(self, username, password):
        self.query_sql = u'SELECT username FROM account_user \
            WHERE username = "%s" and password=password("%s")' \
            % (username,password)
        ret = super().execute()

        if not len(ret):
            return False, u"Login Failed!"
        return True, None

    def get_id(self, username):
        self.query_sql = u'SELECT userid FROM account_user \
            WHERE username = "%s"' % (username)
        ret = super().execute()

        if not len(ret):
            return ''
        else:
            return ret[0][0]

    def insert(self, username, password):
        self.query_sql = u'SELECT userid FROM account_user \
            WHERE username = "%s"' % (username)
        ret = super().execute()
        if len(ret):
            return False, 'Username has been used'


        self.query_sql = \
            u'INSERT INTO account_user(username, userid, password) \
            values("%s", "", "%s") ' % (username,password)
        super().commit()
        return True, \
            'Congratulations, you register successfully! Please Login.'
