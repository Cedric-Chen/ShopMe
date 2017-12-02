#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.dmaccount_business import DMAccount_Business

class Account_Business(DMAccount_Business):
    def __init__(self):
        super().__init__(self)

account_business = Account_Business()
