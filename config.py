class Config(object):
    DEBUG = False
    TESTING = False

class Development(Config):
    DEBUG = True
    SECRET_KEY = 'development key'
    USERNAME = 'admin'
    password = 'default'
