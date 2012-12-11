from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from flask_mail import Mail

app = Flask(__name__)
app.config.from_envvar('CONFIG')

oid = OpenID(app, '/tmp')

db = SQLAlchemy(app)
mail = Mail(app)

import views
