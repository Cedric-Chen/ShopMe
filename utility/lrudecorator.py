#!/usr/bin/python
# -*- coding: utf-8 -*-


import functools

from utility.lrucache import LRUCache

class LRUDecorator(object):
    def __init__(self, size):
        self.cache = LRUCache(size)

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            kwtuple = tuple((key, kwargs[key]) for key in sorted(kwargs.keys()))
            key = (args, kwtuple)
            try:
                return self.cache[key]
            except KeyError:
                pass

            value = func(*args, **kwargs)
            self.cache[key] = value
            return value

        wrapper.cache = self.cache
        wrapper.size = self.cache.size
        wrapper.clear = self.cache.clear
        return functools.update_wrapper(wrapper, func)
