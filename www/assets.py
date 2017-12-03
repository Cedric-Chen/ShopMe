from flask_assets import Bundle, Environment
from config import app

bundles = {

    'bootstrap_js':Bundle(
        'js/bootstrap.bundle.js',
        'js/bootstrap.js',
        output = 'gen/bootstrap.js'
    ),

    'jquery_js': Bundle(
        'js/jquery-3.2.1.min.js',

        output= 'gen/jquery.js'
    ),

    'user_js': Bundle(

        'js/user.js',
        output='gen/user.js'),

    'user_css': Bundle(
        'css/user.css',
        output='gen/user.css')
}

assets = Environment(app)

assets.register(bundles)