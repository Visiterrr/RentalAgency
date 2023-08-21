import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://aentalagency:RKLC58YerU7jXC340GZuql0XoIXPZqd3@dpg-cjhou4d1a6cs73elvp1g-a.singapore-postgres.render.com/aentalagency'


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI =  os.environ.get('SQLALCHEMY_DATABASE_URI')