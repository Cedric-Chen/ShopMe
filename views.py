from flask import render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore,\
    UserMixin, RoleMixin, login_required
from app import app

# back-end function
from app.datamodel.business import model as Business
from app.datamodel.attribute import model as Attribute
from app.datamodel.category import model as Category
from app.datamodel.hours    import model as Hours   
from app.datamodel.photo    import model as Photo   


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SECRET_KEY'] = 'super-secret' 
app.config['SECURITY_REGISTERABLE'] = True 
app.debug = True 
db = SQLAlchemy(app) 
# Define models 
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.before_first_request
def create_user():
    db.create_all()
    user_datastore.create_user(email='test1@test.com', password='test')
    db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/merchant')
def merchant():
#    businessname = 'Cedric' 
#    business = get_business(businessname)
#    attribute = get_attribute(businessname)
#    category = get_category(businessname)
#    hours = get_hour(businessname)
#    photo = get_photo(businessname)

    # for debug
    business    = Business.get_business()
    attribute   = Attribute.get_attribute()
    category    = Category.get_category()
    hours       = Hours.get_hours()
    photo       = Photo.get_photo()

    return render_template(
        'merchant.html',
        business = business,
        attribute= attribute,
        category = category,
        hours    = hours,
        photo    = photo
    )


# only for modifying front-end page
@app.route('/profile')
def profile():
    user = 'Cedric' 
    return render_template('profile.html',
        title='Cedric is awesome!',
        user=user
    )

#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    form = LoginForm()
#    if form.validate_on_submit():
#        flash('Login requested for OpenID="%s", remember_me=%s' %
#              (form.openid.data, str(form.remember_me.data)))
#        return redirect('/index')
#    return render_template('login.html', 
#                           title='Sign In',
#                           form=form,
#                            providers=app.config['OPENID_PROVIDERS'])
