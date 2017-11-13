from flask import render_template, redirect, url_for, request
#from flask_sqlalchemy import SQLAlchemy
#from flask.ext.security import Security, SQLAlchemyUserDatastore,\
#    UserMixin, RoleMixin, login_required
from config import app

# back-end function
from datamodel_test.business import model as Business
from datamodel_test.attribute import model as Attribute
from datamodel_test.category import model as Category
from datamodel_test.hours    import model as Hours
from datamodel_test.photo    import model as Photo

@app.route('/merchant')
def merchant():
#    businessname = 'Cedric'
#    business = get_business(businessname)
#    attribute = get_attribute(businessname)
#    category = get_category(businessname)
#    hours = get_hour(businessname)
#    photo = get_photo(businessname)

    # for debug
    merchant.business    = Business.get_business()
    merchant.attribute   = Attribute.get_attribute()
    merchant.category    = Category.get_category()
    merchant.hours       = Hours.get_hours()
    merchant.photo       = Photo.get_photo()

    return render_template(
        'merchant.html',
        business = merchant.business,
        attribute= merchant.attribute,
        category = merchant.category,
        hours    = merchant.hours,
        photo    = merchant.photo
    )

@app.route('/merchant/update_info', methods=['POST'])
def update_merchant_info():
    business = {}

    newname = request.form['newname']
    if newname != '' and newlongitude != merchant.business['name']:
        business['name'] = newname

    newopenornot = request.form.get('newopenornot')
    if newopenornot:
        if not merchant.business['is_open']:
            business['is_open'] = 1
    else:
        if merchant.business['is_open']:
            business['is_open'] = 0

    newstreet = request.form['newstreet']
    if newstreet != '' and newlongitude != merchant.business['street']:
        business['street'] = newstreet
    newcity = request.form['newcity']
    if newcity != '' and newlongitude != merchant.business['city']:
        business['city'] = newname
    newstate = request.form['newstate']
    if newstate != '' and newlongitude != merchant.business['state']:
        business['state'] = newstate
    newneighborhood = request.form['newneighborhood']
    if newneighborhood != '' and newlongitude != merchant.business['neighborhood']:
        business['neighborhood'] = newneighborhood
    newpostal_code = request.form['newpostal_code']
    if newpostal_code != '' and newlongitude != merchant.business['postal_code']:
        business['postal_code'] = newpostal_code
    newlatitude = request.form['n from app import aewlatitude']
    if newlatitude != '' and newlongitude != merchant.business['latitude']:
        business['latitude'] = newlatitude
    newlongitude = request.form['newlongitude']
    if newlongitude != '' and newlongitude != merchant.business['longitude']:
        business['longitude'] = newlongitude

    return redirect(request.referrer)

@app.route('/merchant/update_attr', methods=['POST'])
def update_merchant_attr():
    attribute = {}

    for field1, value1 in merchant.attribute.items():
        if type(value1) == dict:
            for field2, value2 in value1.items():
                newvalue = request.form.get(field1+'_'+field2)
                if newvalue:
                    newvalue = True
                else:
                    newvalue = False
                if newvalue != value2:
                    if field1 not in attribute:
                        attribute[field1] = {}
                    attribute[field1][field2] = newvalue
        else:
            newvalue = request.form.get(field1)
            if newvalue:
                newvalue = True
            else:
                newvalue = False
            if newvalue != value1:
                attribute[field1] = newvalue

    return redirect(request.referrer)

@app.route('/merchant/update_hours', methods=['POST'])
def update_merchant_hours():
    hours = {}
    for date in ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday']:
        newvalue = request.form[date+'_start_at'] + '-' + \
            request.form[date+'_end_at']
        if newvalue != '-' and newvalue != merchant.hours[date]:
            hours[date] = newvalue

    return str(hours)
