#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob, sys
from os.path import dirname, basename, isfile
modules = glob.glob(dirname(__file__) + u'/*.py')
__all__ = [basename(f)[:-3] for f in modules \
    if isfile(f) and not f.endswith(u'__init__.py')]

from datamodel import *
from database.datamodel import dmcounter
dmcounter.check()
