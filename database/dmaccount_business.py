#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMAccount_Business(DataModel):
    def __init__(self, cls):
        super().__init__(cls)
        self.dm_attr = [u'username', u'merchantid', u'password']

#    def check_existence(self, username):
#        self.query_sql = u'SELECT count(*) FROM account_user \
#            WHERE username = "%s"' % (username)
#        ret = super().execute()
#        if ret[0]:
#            return True
#        else
#            return False 
    def check(self, username, password):
        self.query_sql = u'SELECT username FROM account_business \
            WHERE username = "%s" and password=password("%s")'\
            % (username,password)
        ret = super().execute()

        if not len(ret):
            return False, u"Business login failed!"

        return True, None

    def get_id(self, username):
        self.query_sql = u'SELECT merchantid FROM account_business \
            WHERE username = "%s"' % (username)
        ret = super().execute()

        if not len(ret):
            return ''
        else:
            return ret[0][0]

    def insert(self, username, password, merchantid=''):
        self.query_sql = u'SELECT merchantid FROM account_business \
            WHERE username = "%s"' % (username)
        ret = super().execute()
        if len(ret):
            return False, 'Username has been used'

        self.query_sql = \
            u'INSERT INTO account_business(username, merchantid, password) \
            values("%s", "%s", "%s") ' % (username, merchantid, password)
        super().commit()
        return True, \
            'Congratulations, you register successfully! Please Login.'

    def update(self, business_id, new_username, new_password):
        if new_username != '':
            self.query_sql = u'SELECT merchantid FROM account_business \
                WHERE username = "%s"' % (new_username)
            ret = super().execute()
            if len(ret):
                return False, 'Username has been used'

        self.query_sql = u'SELECT merchantid FROM account_business \
            WHERE merchantid = "%s"' % (business_id)
        ret = super().execute()
        if not len(ret):
            self.insert(new_username, new_password, business_id)
            return True, 'Update succeeds.'+business_id

        if new_username != '':
            self.query_sql = u'UPDATE account_business \
                SET username="%s" \
                WHERE merchantid = "%s"' % (new_username,business_id)
            ret = super().commit()

        if new_password != '':
            self.query_sql = u'UPDATE account_business \
                SET password="%s" \
                WHERE merchantid = "%s"' % (new_password,business_id)
            ret = super().commit()
        
        return True, 'Update succeeds.'
