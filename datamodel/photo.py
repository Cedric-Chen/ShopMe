#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.dmphoto import DMPhoto

class Photo(DMPhoto):
    def __init__(self):
        super().__init__(self)

    def get_photo(self, business_id):
        '''
        @return: dict
        '''
        try:
            return self.photo
        except:
            self.photo = super().get_photo(business_id)
        return self.photo

model = Photo()
