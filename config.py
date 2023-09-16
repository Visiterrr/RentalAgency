import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://userr:zQIqLBm4Sy6MZl75YsPR5BgCXFwVQ0nr@dpg-ck2bpg821fec73akon3g-a/td_a4bv'


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI =  os.environ.get('SQLALCHEMY_DATABASE_URI')