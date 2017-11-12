# -*- coding: utf-8 -*-

class Hours(object):
    def get_hours(self):
        return {
            'Friday': '10:00-21:00',
            'Monday': '10:00-21:00',
            'Saturday': '10:00-21:00',
            'Sunday': '11:00-18:00',
            'Thursday': '10:00-21:00',
            'Tuesday': '10:00-21:00',
            'Wednesday': '10:00-21:00'
        }

model = Hours()
