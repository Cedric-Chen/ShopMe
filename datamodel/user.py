#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.dmuser import DMUser

class User(DMUser):
    def __init__(self):
        super().__init__(self)

    def get_user(self, user_id):
        '''
        @return: dict
        '''
        try:
            return self.user
        except:
            self.user = super().get_user(user_id)
        return self.user

model = User()
