from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, TextAreaField, SubmitField, \
    PasswordField, ValidationError, RadioField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import DateField
from app import files
from flask import g
from app import db


class SignupForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired("请输入教工号／学号.")])
    username = StringField('User_name', validators=[DataRequired("请输入真实姓名.")])
    password = PasswordField('Password', validators=[DataRequired("请输入密码."),
                                                     EqualTo('confirm', message="密码必须一致")])
    confirm = PasswordField('Repeat Password')


class LoginForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired("请输入教工号／学号.")])
    password = PasswordField('Password', validators=[DataRequired("请输入密码.")])
    remember_me = BooleanField('remember_me', default=False)


class WorkArrangeForm(FlaskForm):

    course_id = SelectField('Course_id',choices=[],validators=[DataRequired("")])
    homework_batch = SelectField('Homework_batch', coerce=int,choices=[],validators=[DataRequired("")])
    homework_describe = TextAreaField('Homework_describe',validators=[DataRequired("请输入作业描述.")])
    attach = FileField('Your Attachment', validators=[FileAllowed(files, '可以上传文件和图片!')])
    start_time = DateField('DatePicker', format='%Y-%m-%d',validators=[DataRequired("请选择开始时间.")])
    end_time = DateField('DatePicker', format='%Y-%m-%d',validators=[DataRequired("请选择截止时间.")])



