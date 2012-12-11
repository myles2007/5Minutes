from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from flask_mail import Mail

app = Flask(__name__)
try:
    app.config.from_envvar('CONFIG')
except RuntimeError:
    from config import CONFIG, SECRET_KEY
    for key in CONFIG:
        app.config[key] = CONFIG[key]
    app.secret_key = SECRET_KEY

oid = OpenID(app, '/tmp')

db = SQLAlchemy(app)
mail = Mail(app)

import views
