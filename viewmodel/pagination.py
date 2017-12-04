#!/usr/bin/python
# -*- coding: utf-8 -*-

class Pagination(dict):
    def __init__(self, name, total, page_size, pages):
        self[u'name'] = name
        self[u'total'] = total
        self[u'page_size'] = page_size
        self[u'current'] = 1
        self[u'first'] = 1
        full_page = total // page_size
        self[u'last'] = 0 if full_page * page_size == total else 1
        self[u'last'] += full_page
        pages = pages // 2 * 2 + 1
        # total pages displayed each time
        self[u'pages'] = min(self[u'last'], pages)
        # page number to be displayed
        self[u'page_no'] = [x for x in range(1, self[u'pages'] + 1)]
        # the index for list of current page
        self[u'start'] = 0
        self[u'end'] = min(total, page_size)

    def jump(self, page):
        page = int(page)
        if page < 1 or page > self[u'last']:
            return self
        self[u'current'] = page
        start = (page - 1) * self[u'page_size']
        self[u'start'] = start
        self[u'end'] = min(self[u'total'], start + self[u'page_size'])
        page_no = list(range(page - self[u'pages'] // 2, \
            page + self[u'pages'] // 2 + 1))
        if page_no[-1] > self[u'last']:
            tmp = page_no[-1] - self[u'last']
            for i in range(len(page_no)):
                page_no[i] -= tmp
        if page_no[0] < 1:
            tmp = 1 - page_no[0]
            for i in range(len(page_no)):
                page_no[i] += tmp
        while page_no and page_no[-1] > self[u'last']:
            page_no.pop()
        self[u'page_no'] = page_no
        return self
