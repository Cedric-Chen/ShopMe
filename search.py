#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask import render_template

#from config import app, app_debug, log_dir
#from www import url
from datamodel_test.business import model as Business
from datamodel_test.review import model as Review
from datamodel_test.user import model as User
from datamodel_test.hours import model as Hours

app = Flask(__name__)

@app.route(u'/search')
def search():
    business = Business.get_business()
    review = Review.get_review()
    user = User.get_user()
    num_item = 10
    business_list = [business for i in range(num_item)]
    review_list = [review for i in range(num_item)]
    user_list = [user for i in range(num_item)]

    return render_template(u'search.html',
                            business_list=business_list,
                            review_list=review_list,
                            user_list=user_list,)


if __name__ == '__main__':
    app.run()
