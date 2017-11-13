#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime

class Review(object):
    def get_review(self):
        return {
            '---nya_pjxWmNFDFyAcfsA': {
                'business_id': 'zQNJwaWR1M1zDjLNVJiNEw',
                'cool': 1,
                'date': datetime.datetime(2012, 6, 27, 0, 0),
                'funny': 1,
                'id': '---nya_pjxWmNFDFyAcfsA',
                'stars': 1,
                'text': "Another case of the Emperor's New "\
                + 'Clothes.  Someone of the artsy set '\
                + 'decided that this relatively good but '\
                + 'overpriced fare was great pizza and all '\
                + 'the lemmings followed suit.  Will anyone '\
                + 'tell the Emperor he has no clothes?  The '\
                + 'limited hours, no delivery, and lack of '\
                + 'dining area add to the snob appeal.  '\
                + "Don't be taken in.",
                'useful': 3,
                'user_id': '5QOtcHU1SoqEqBCRR6FhsA'
            }
        }

model = Review()
