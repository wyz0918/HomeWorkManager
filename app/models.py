from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class ElectiveCourse(db.Model):
    __tablename__ = 'elective_course'

    student_id = db.Column(db.String(54), db.ForeignKey("user.id"), primary_key=True)
    course_id = db.Column(db.String(54), db.ForeignKey("course.id"), primary_key=True)
    num = db.Column(db.Integer)
    student = db.relationship("User", back_populates="joined_courses")
    joined_course = db.relationship("Course", back_populates="students")

    def __init__(self, student_id, course_id):
        self.student_id = student_id
        self.course_id = course_id

    def obj2dict(self):
        return {
            "student_id": self.student_id,
            "course_id": self.course_id
        }


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(54), primary_key=True)
    username = db.Column(db.String(54), unique=True)
    passwdhash = db.Column(db.String(54))
    identity = db.Column(db.String(4))

    created_courses = db.relationship("Course", back_populates="creator", lazy='dynamic')
    homeworks = db.relationship("Completion", back_populates="student", lazy='dynamic')
    joined_courses = db.relationship("ElectiveCourse", back_populates="student", lazy='dynamic')

    is_authenticated = True
    is_active = True
    is_anonymous = False

    def __init__(self, id, username, password, identity):
        self.id = id
        self.username = username
        self.set_password(password)
        self.identity = identity

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.passwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwdhash, password)

    def get_username(self):
        return self.username

    def get_indentity(self):
        return self.identity

    def obj2dict(self):
        if self.identity == "T":
            return {
                "id": self.id,
                "username": self.username,
                "identity": self.identity
            }
        else:
            return {
                "id": self.id,
                "username": self.username,
                "identity": self.identity,
                "commit_num": self.temp_commit_num if self.__dict__.get("temp_commit_num") is not None else None
            }


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.String(54), primary_key=True)
    course_name = db.Column(db.String(54))
    creator_id = db.Column(db.String(54), db.ForeignKey('user.id'))

    creator = db.relationship("User", back_populates="created_courses")
    homeworks = db.relationship("HomeWork", back_populates="course", lazy='dynamic')
    students = db.relationship("ElectiveCourse", back_populates='joined_course', lazy='dynamic')

    def __init__(self, id, course_name, creator_id):
        self.id = id
        self.course_name = course_name
        self.creator_id = creator_id

    def obj2dict(self):
        return {
            "id": self.id,
            "course_name": self.course_name,
            "creator_id": self.creator_id,
            "creator_name": self.creator.username
        }


class HomeWork(db.Model):
    __tablename__ = 'homework'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(54), db.ForeignKey('course.id'))
    batch = db.Column(db.Integer)
    homework_describe = db.Column(db.String(120))
    attach = db.Column(db.String(120))
    start_time = db.Column(db.String(24))
    end_time = db.Column(db.String(24))
    upload_num = db.Column(db.Integer)
    status = db.Column(db.String(24))

    course = db.relationship("Course", back_populates="homeworks")
    students = db.relationship("Completion", back_populates="homework", lazy='dynamic')

    def __init__(self, course_id, batch, homework_describe, attach, start_time, end_time, upload_num, status):
        self.course_id = course_id
        self.batch = batch
        self.homework_describe = homework_describe
        self.attach = attach
        self.start_time = start_time
        self.end_time = end_time
        self.upload_num = upload_num
        self.status = status

    def obj2dict(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "batch": self.batch,
            "homework_describe": self.homework_describe,
            "attach": self.attach,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "upload_num": self.upload_num,
            "status": self.status,
            "course_name": self.course.course_name
        }


# 完成情况
class Completion(db.Model):
    __tablename__ = 'completion'
    student_id = db.Column(db.String(54), db.ForeignKey("user.id"), primary_key=True)
    homework_id = db.Column(db.Integer, db.ForeignKey("homework.id"), primary_key=True)
    complete_time = db.Column(db.String(24))
    score = db.Column(db.Integer)
    comment = db.Column(db.String(240))
    address = db.Column(db.String(54))

    student = db.relationship("User", back_populates="homeworks")
    homework = db.relationship("HomeWork", back_populates="students")

    def __init__(self, student_id, homework_id, complete_time, score, comment, address):
        self.student_id = student_id
        self.homework_id = homework_id
        self.complete_time = complete_time
        self.score = score
        self.comment = comment
        self.address = address

    def obj2dict(self):
        return {
            "student_id": self.student_id,
            "homework_id": self.homework_id,
            "complete_time": self.complete_time,
            "score": self.score if self.score else "暂无",
            "comment": self.comment if self.comment else "暂无",
            "address": self.address
        }


class AdditionalStudentInfo(db.Model):
    __tablename__ = 'addtional_student_info'
    student_id = db.Column(db.String(54), db.ForeignKey("user.id"), primary_key=True)
    enrollment_year = db.Column(db.String(8))
    university = db.Column(db.String(54))
    college = db.Column(db.String(54))
    major = db.Column(db.String(54))
    birthday = db.Column(db.String(24))

    def __init__(self, student_id, enrollment_year, university, college, major, birthday):
        self.student_id = student_id
        self.enrollment_year = enrollment_year
        self.university = university
        self.college = college
        self.major = major
        self.birthday = birthday

    def obj2dict(self):
        return {
            "student_id": self.student_id,
            "enrollment_year": self.enrollment_year,
            "university": self.university,
            "college": self.college,
            "major": self.major,
            "birthday": self.birthday
        }
