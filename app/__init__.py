from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, patch_request_class

app = Flask(__name__, static_url_path='')
app.config.from_object('config')
db = SQLAlchemy(app)


files = UploadSet('files')
configure_uploads(app, files)
patch_request_class(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views, models


