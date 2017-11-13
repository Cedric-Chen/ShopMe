#!/usr/bin/python
# -*- coding: utf-8 -*-

class Pagination(dict):
    def __init__(self, name, page_size, total, pages):
        self[u'name'] = name
        self[u'page_size'] = page_size
        self[u'total'] = total
        self[u'current'] = 1
        self[u'first'] = 1
        full_page = total // page_size
        self[u'last'] = 0 if full_page * page_size == total else 1
        self[u'last'] += full_page
        pages = pages // 2 * 2 + 1
        self[u'pages'] = min(self[u'last'], pages)
        self[u'page_no'] = [x for x in range(1, self[u'pages'] + 1)]

    def jump(self, page):
        if page < 1 or page > self[u'last']:
            return self
        start = max(1, page - self[u'pages'] // 2)
        if self[u'last'] < page + self[u'pages'] // 2:
            self[u'page_no'] = [x for x in range(\
                self[u'last'] - self[u'pages'] + 1, self[u'last'] + 1)]
        else:
            self[u'page_no'] = [x for x in range(\
                page - self[u'pages'] // 2, page + self[u'last'] // 2 + 1)]
        self[u'current'] = page
        return self

    def prev(self):
        return self.jump(self.current - 1)

    def next(self):
        return self.jump(self.current + 1)
