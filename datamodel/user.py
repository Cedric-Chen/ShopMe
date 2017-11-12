#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime


class User(object):
    def get_user(self):
        return {
            'average_stars': 3.03,
            'compliment_cool': 1,
            'compliment_cute': 0,
            'compliment_funny': 1,
            'compliment_hot': 0,
            'compliment_list': 0,
            'compliment_more': 1,
            'compliment_note': 0,
            'compliment_photos': 0,
            'compliment_plain': 1,
            'compliment_profile': 0,
            'compliment_writer': 1,
            'cool': 0,
            'fans': 0,
            'funny': 1,
            'id': '5QOtcHU1SoqEqBCRR6FhsA',
            'name': 'Edward',
            'review_count': 143,
            'useful': 17,
            'yelping_since': datetime.datetime(2009, 3, 3, 0, 0)
        }

model = User()

