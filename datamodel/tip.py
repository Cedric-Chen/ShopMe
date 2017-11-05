#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.dmtip import DMTip

class Tip(DMTip):
    def __init__(self):
        super().__init__(self)

    def get_tip(self, business_id, user_id):
        '''
        @return: dict
        '''
        try:
            return self.tip
        except:
            self.tip = super().get_tip(business_id, user_id)
        return self.tip

model = Tip()
