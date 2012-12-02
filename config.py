import os

class Config(object):
    CONFIG_TYPE = 'BASE'
    DEBUG = False
    TESTING = False
    ROOT_PATH = os.path.split(os.path.abspath(__file__))[0]
    PATH_MAP = {'/js': os.path.join(ROOT_PATH, os.path.join('static', 'js')),
                '/css': os.path.join(ROOT_PATH, os.path.join('static', 'css')),
                '/img': os.path.join(ROOT_PATH, os.path.join('static', 'img'))
               }

class Development(Config):
    CONFIG_TYPE = 'DEVELOPMENT'
    DEBUG = True
    DATABASE = '/tmp/5minutes.db'
    SECRET_KEY = 'development key'
    USERNAME = 'admin'
    PASSWORD = 'default'

