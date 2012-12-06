from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from flask_mail import Mail

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fiveminutes.db'
app.config['MAIL_SERVER'] = 'FILLMEIN'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'FILLMEIN'
app.config['MAIL_PASSWORD'] = 'FILLMEIN'
app.secret_key = 'FILLMEIN'

oid = OpenID(app, '/tmp')

db = SQLAlchemy(app)
mail = Mail(app)

import views
