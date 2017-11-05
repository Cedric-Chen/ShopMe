#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.dmreview import DMReview

class Review(DMReview):
    def __init__(self):
        super().__init__(self)

    def get_review(self, business_id, user_id):
        '''
        @return: dict
        '''
        try:
            return self.review
        except:
            self.review = super().get_review(business_id, user_id)
        return self.review

model = Review()
