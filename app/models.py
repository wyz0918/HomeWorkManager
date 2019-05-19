from flask_login import unicode
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(54), primary_key=True)
    username = db.Column(db.String(54), unique=True)
    passwdhash = db.Column(db.String(54))
    identity = db.Column(db.String(4))


    def __init__(self, id,username, password,identity):
        self.id = id
        self.username = username
        self.set_password(password)
        self.identity = identity

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(str(self.id))

    def set_password(self, password):
        self.passwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwdhash, password)

    def get_username(self):
        return unicode(str(self.username))

    def get_indentity(self):
        return unicode(str(self.identity))


class HomeWork(db.Model):
    __tablename__ = 'homework'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(54))
    batch = db.Column(db.Integer)
    homework_name = db.Column(db.String(120))
    publish_time = db.Column(db.String(24))
    end_time = db.Column(db.String(24))
    upload_status = db.Column(db.String(24))
    status = db.Column(db.String(24))

    def __init__(self, course_name,batch, homework_name,publish_time,end_time,upload_status,status):
        self.course_name = course_name
        self.batch = batch
        self.homework_name = homework_name
        self.publish_time = publish_time
        self.end_time = end_time
        self.upload_status = upload_status
        self.status = status


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(54))
    course_name = db.Column(db.String(54))

    def __init__(self, id,user_id,course_name,):
        self.id = id
        self.user_id = user_id
        self.course_name = course_name

