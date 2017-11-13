from flask import render_template, redirect, url_for, request
from config import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# only for modifying front-end page
@app.route('/profile')
def profile():
    user = 'Cedric'
    return render_template('profile.html',
        title='Cedric is awesome!',
        user=user
    )
