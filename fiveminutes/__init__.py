import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from flask_mail import Mail

app = Flask(__name__)

if 'CONFIG' not in os.environ:
    os.environ['CONFIG'] = os.path.abspath(os.path.join(os.path.dirname(__name__), 'settings.cfg.template'))

app.config.from_envvar('CONFIG')
app.config['ROOT_PATH'] = os.path.split(os.path.abspath(__file__))[0]
app.config['PATH_MAP'] = {'/js': os.path.join(app.config['ROOT_PATH'], 'static', 'js'),
                          '/css': os.path.join(app.config['ROOT_PATH'], 'static', 'css'),
                          '/img': os.path.join(app.config['ROOT_PATH'], 'static', 'img')}

db = SQLAlchemy(app)
mail = Mail(app)
oid = OpenID(app, '/tmp')

import views
