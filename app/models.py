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

    created_courses = db.relationship("Course", back_populates="creator", lazy='dynamic')  # *****
    homeworks = db.relationship("Completion", back_populates="student", lazy='dynamic')  # *****
    joined_courses = db.relationship("ElectiveCourse", back_populates="student", lazy='dynamic')  # *****

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
        return {
            "id": self.id,
            "username": self.username,
            "identity": self.identity
        }

        # if self.identity == "T":
        #     created_courses_info = list()
        #     for created_course in self.created_courses:
        #         created_course_info = dict()
        #         created_course_info["id"] = created_course.id
        #         created_course_info["course_name"] = created_course.course_name
        #         created_courses_info.append(created_course_info)
        #
        #     return {
        #         "id": self.id,
        #         "username": self.username,
        #         "identity": self.identity,
        #         "created_courses": created_courses_info
        #     }
        # else:
        #     homeworks_info = list()
        #     for homework in self.homeworks:
        #         homework_info = dict()
        #         homework_info["id"] = homework.id
        #         homework_info["course_id"] = homework.course_id
        #         homework_info["batch"] = homework.batch
        #         homework_info["homework_describe"] = homework.homework_describe
        #         homework_info["attach"] = homework.attach
        #         homework_info["start_time"] = homework.start_time
        #         homework_info["end_time"] = homework.end_time
        #         homework_info["upload_num"] = homework.upload_num
        #         homework_info["status"] = homework.status
        #         homeworks_info.append(homework_info)
        #
        #     joined_courses_info = list()
        #     for joined_course in self.joined_courses:
        #         joined_course_info = dict()
        #         joined_course_info["id"] = joined_course.id
        #         joined_course_info["course_name"] = joined_course.id
        #         joined_course_info["creator_id"] = joined_course.id
        #         joined_courses_info.append(joined_course_info)
        #
        #     return {
        #         "id": self.id,
        #         "username": self.username,
        #         "identity": self.identity,
        #         "homeworks_info": homeworks_info,
        #         "joined_courses_info": joined_courses_info
        #     }


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.String(54), primary_key=True)
    course_name = db.Column(db.String(54))
    creator_id = db.Column(db.String(54), db.ForeignKey('user.id'))  # *****

    creator = db.relationship("User", back_populates="created_courses")  # *****
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

        # homeworks_info = list()
        # for homework in self.homeworks:
        #     homework_info = dict()
        #     homework_info["id"] = homework.id
        #     homework_info["course_id"] = homework.course_id
        #     homework_info["batch"] = homework.batch
        #     homework_info["homework_describe"] = homework.homework_describe
        #     homework_info["attach"] = homework.attach
        #     homework_info["start_time"] = homework.start_time
        #     homework_info["end_time"] = homework.end_time
        #     homework_info["upload_num"] = homework.upload_num
        #     homework_info["status"] = homework.status
        #     homeworks_info.append(homework_info)
        #
        # students_info = list()
        # for student in self.students:
        #     student_info = dict()
        #     student_info["id"] = student.id
        #     student_info["username"] = student.username
        #     students_info.append(student_info)
        #
        # return {
        #     "id": self.id,
        #     "course_name": self.course_name,
        #     "creator": {
        #         "id": self.creator.id,
        #         "username": self.creator.username
        #     },
        #     "homeworks": homeworks_info,
        #     "students": students_info
        # }


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
    students = db.relationship("Completion", back_populates="homework", lazy='dynamic')  # *****

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

        # return {
        #     "id": self.id,
        #     "course_id": self.course_id,
        #     "batch": self.batch,
        #     "homework_describe": self.homework_describe,
        #     "attach": self.attach,
        #     "start_time": self.start_time,
        #     "end_time": self.end_time,
        #     "upload_num": self.upload_num,
        #     "status": self.status,
        #     "course": {
        #         "id": self.course.id,
        #         "name": self.course.course_name,
        #         "creator_id": self.course.creator_id
        #     }
        # }


# 完成情况
class Completion(db.Model):
    __tablename__ = 'completion'
    student_id = db.Column(db.String(54), db.ForeignKey("user.id"), primary_key=True)
    homework_id = db.Column(db.Integer, db.ForeignKey("homework.id"), primary_key=True)
    work_name = db.Column(db.String(24))
    complete_time = db.Column(db.String(24))
    score = db.Column(db.Integer)
    comment = db.Column(db.String(240))
    address = db.Column(db.String(54))

    student = db.relationship("User", back_populates="homeworks")
    homework = db.relationship("HomeWork", back_populates="students")

    def __init__(self, student_id, homework_id, work_name, complete_time, score, comment, address):
        self.student_id = student_id
        self.homework_id = homework_id
        self.work_name = work_name
        self.complete_time = complete_time
        self.score = score
        self.comment = comment
        self.address = address

    def obj2dict(self):
        return {
            "student_id": self.student_id,
            "homework_id": self.homework_id,
            "work_name": self.work_name,
            "complete_time": self.complete_time,
            "score": self.score,
            "comment": self.comment,
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
