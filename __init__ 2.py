from flask import Flask

app = Flask(__name__) #"app" here is an variable
# app.config.from_object('config')

from app import views #"app" here is a package, different from above "app"
