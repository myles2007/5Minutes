import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from flask_mail import Mail

app = Flask(__name__)

if 'CONFIG' not in os.environ:
    os.environ['CONFIG'] = os.path.abspath(os.path.join(os.path.dirname(__name__), 'settings.cfg.template'))

app.config.from_envvar('CONFIG')

db = SQLAlchemy(app)
mail = Mail(app)
oid = OpenID(app, '/tmp')

import views
