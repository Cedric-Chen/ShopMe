#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template, request
from flask_paginate import Pagination, get_page_args
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
import time

from config import app
from datamodel.business import business
from datamodel.category import category
from datamodel.checkin import checkin
from datamodel.review import review
from datamodel.user import user
from utility.lrudecorator import LRUDecorator

US_STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",  \
"HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", \
"MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", \
"NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", \
"SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

class recommender(object):

    def __init__(self, business_list, cond_loc):
        self.business_list = business_list
        if(cond_loc['__type__'] == "laglng"):
            self.user_laglng = (cond_loc['lag'], cond_loc['lng'])
        else:
            self.user_laglng = None

    def score(self,business):
        if self.user_laglng:
            distance = vincenty(self.user_laglng,(business['latitude'],business['longitude'])).miles
            score = business['stars'] + 1/distance
        else:
            score = business['stars']
        return score

    def recommend(self):
        return sorted(self.business_list, key = self.score, reverse = True)

def parse_kw(kw):
    l = kw.split(',')
    d = dict()
    d['attribute'] = dict()
    kws = []
    op_list = ['==','>=','<=','=','>','<']
    for x in l:
        for op in op_list:
            if(len(x.split(op)) == 2):
                k = x.split(op)[0].strip()
                v = x.split(op)[1].strip()
                try:
                    float(v)
                    v = op + v
                except ValueError:
                    v = op + "'" + v + "'"
                d['attribute'][k] = v
                break
            elif(op == op_list[-1]):
                if(x.strip() != ""):
                    kws.append(x.strip())
    d['keyword'] = kws
    return d

def parse_loc(loc):
    d = dict()
    if(len(loc.split(',')) == 2):
        try:
            d['lag'] = float(loc.split(',')[0].strip())
            d['lng'] = float(loc.split(',')[1].strip())
            geolocator = Nominatim()
            location = geolocator.reverse("%s, %s" %(d['lag'], d['lng']))
            try:
                d['postal_code'] = location.raw['address']['postcode']
            except KeyError:
                d['postal_code'] = None
        except ValueError:
            d['city'] = loc.split(',')[0].strip()
            d['state'] = loc.split(',')[1].strip()
        return d
    else:
        try:
            int(loc)
            d['postal_code'] = loc.strip()
            return d
        except:
            if(loc.strip().upper() in US_STATES):
                d['state'] = loc.strip().upper()
            else:
                d['city'] = loc.strip().lower()
            return d
    return {}


@LRUDecorator(50)
def search_result(kw, loc):
    start = time.time()
    cond_kw = parse_kw(kw)
    cond_loc = parse_loc(loc)
    if(cond_loc['city'] != None):
        cond_kw['attribute']['city'] = "='" + cond_loc['city'] + "'"
    if(cond_loc['state'] != None)
        cond_kw['attribute']['state'] = "='" + cond_loc['state'] + "'"
    if(cond_loc['postal_code'] != None):
        cond_kw['attribute']['postal_code'] = "='" + cond_loc['postal_code'] + "'"
    parse_over = time.time()
    # query
    business_list = business.keyword_search(cond_kw)
    query_over = time.time()
    # recommendation
    recommended_business_list = recommender(business_list,cond_loc).recommend()
    recommend_over = time.time()
    print("Parse time: %s" %parse_over - start)
    print("Query time: %s" %query_over - parse_over)
    print("Recommend time: %s" %recommend_over - query_over)
    return recommended_business_list


@app.route(u'/search/kw=<kw>&loc=<loc>/')
def search(kw, loc):
    business_list = search_result(kw, loc)
    # pagination
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    per_page = 10
    pagination = Pagination(page=page, per_page=per_page,total=len(business_list), search=False, record_name='results')
    business_list = business_list[(page - 1) * per_page: page * per_page]

    category_list = []
    checkin_list = []
    review_list = []
    user_list = []
    for business_item in business_list:
        business_id = business_item[u'id']
        category_list.append(category.select(business_id))
        checkin_list.append(checkin.select(business_id))
        review_items = review.select(business_id,u'*')
        keys = list(review_items.keys())
        if len(keys) > 0:
            user_list.append(user.select(review_items[keys[0]][u'user_id']))
            s = review_items[keys[0]]['text']
            s2 = ' '.join(s.split(' ')[0:80]) + "..."
            review_list.append(s2)
        else:
            user_list.append({})
            review_list.append(review_items)

    num_checkin_list = []
    for c in checkin_list:
        num_checkin_list.append(sum(list(c.values())))

    # When the search result lists are generated.
    laglng_list = [[b['name'], b['latitude'], b['longitude']] for b in business_list]
    result_list = list()
    for idx in range(0, len(business_list)):
        result = dict()
        result['category'] = ', '.join(list(category_list[idx].values()))
        result['business'] = business_list[idx]
        result['num_checkin'] = num_checkin_list[idx]
        result['review'] = review_list[idx]
        result['user'] = user_list[idx]
        result_list.append(result)


    return render_template(u'search.html',
        # business = business_list[0] if len(business_list) > 0 else None,
        result_list=result_list,
        laglng_list=laglng_list,
        page=page,
        per_page=per_page,
        pagination=pagination,
        kw = kw,
        loc = loc)
