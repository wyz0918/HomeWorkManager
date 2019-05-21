import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = '2928918a'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'demo.db')
UPLOADED_FILES_DEST = os.getcwd() + '/app/static/pics'