#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.dmcheckin import DMCheckIn

class CheckIn(DMCheckIn):
    def __init__(self):
        super().__init__(self)

    def get_checkin(self, business_id):
        '''
        @return: dict
        '''
        try:
            return self.check_in
        except:
            self.check_in = super().get_checkin(business_id)
        return self.check_in

model = CheckIn()
