#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.dmfriend import DMFriend

class Friend(DMFriend):
    def __init__(self):
        super().__init__(self)

    def get_business(self, user_id):
        '''
        @return: dict
        '''
        try:
            return self.friend
        except:
            self.friend = super().get_friend(user_id)
        return self.business

model = Friend()
