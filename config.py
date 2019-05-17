import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = 'secret_key_1'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'demo.db')
