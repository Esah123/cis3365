import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Basketball23!'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:Basketball23!@cis3368.cfkaqeuq6e3f.us-east-1.rds.amazonaws.com/cis3368'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'Basketball23!'
