import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://userr:7tZfyeK42j5bvpkRUVqghp54EgHNgyjK@dpg-cjhm5rl1a6cs73955a80-a.singapore-postgres.render.com/reokroke'


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI =  os.environ.get('SQLALCHEMY_DATABASE_URI')