from flask import render_template, flash, redirect, session, url_for, request, g,jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm,files
from flask import make_response
from app.models import User,HomeWork,Course,ElectiveCourse,Completion
import datetime
import re


@lm.user_loader
def load_user(uid):
    return User.query.get(uid)


@app.before_request
def before_request():
    g.user = current_user


@app.route('/about', methods=['GET'])
@login_required
def about():
    return render_template('about.html')


@app.route('/score_comment', methods=['POST'])
@login_required
def score_comment():
    from sqlalchemy import and_
    homework_id = request.values['homework_id']
    student_id = request.values['student_id']
    score = request.values['score']
    comment = request.values['comment']

    completion = Completion.query.filter(and_(Completion.homework_id == homework_id,
                                              Completion.student_id == student_id)).first()
    if completion:
        completion.comment = comment
        completion.score = score

        db.session.add(completion)
        db.session.commit()

        message = "提交评分和评语成功！"

    return jsonify(message)


@app.route('/download/<filename>', methods=['GET'])
@login_required
def download_file(filename):
    import os
    from flask import  send_from_directory
    directory = os.getcwd()+'/app/static/pics'
    return send_from_directory(directory, filename, as_attachment=True)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@login_required
def index():

    result = []
    for i in g.user.courses:

        result.append((url_for('t_class_section', course_id=i.id), i.course_name))

    session.pop('result', None)
    session['result'] = result

    return render_template('index.html', result=result)


@app.route('/work_arrange', methods=['GET','POST'])
@login_required
def work_arrange():
    from app.forms import WorkArrangeForm
    form = WorkArrangeForm()
    form.course_id.choices += [(r.id, str(r.course_name + " ID:" + r.id)) for r in g.user.courses]
    form.course_id.choices.insert(0, ('', '请选择课程'))
    form.homework_batch.choices += [(i, str(i)) for i in range(1, 15)]
    form.homework_batch.choices.insert(0, (-1, '请选择作业批次'))
    if request.method == "GET":

        return render_template('work_arrange.html', form=form)

    else:
        if form.validate_on_submit():

            if form.attach.data:
                filename = files.save(form.attach.data)
                file_url = files.url(filename)
            else:
                filename = ""

            newhomework = HomeWork(form.course_id.data, form.homework_batch.data,
                                form.homework_describe.data, filename,
                                form.start_time.data, form.end_time.data, 0, "进行中")

            db.session.add(newhomework)

            message = "创建作业成功！"

            course = Course.query.filter_by(id=form.course_id.data).first()
            course.homework.append(newhomework)
            db.session.add(course)
            db.session.commit()

            return render_template('work_arrange.html', form=form,message=message)

        return render_template('work_arrange.html',form=form)


@app.route('/search_homework', methods=['POST'])
@login_required
def search_homework():
    homework_id = request.values['homework_id']
    session['homework_id'] = homework_id

    info = dict()
    info["homework_info"] = list()

    completion = Completion.query.filter_by(homework_id=homework_id).all()

    for record in completion:
        each_info = dict()
        each_info["student_id"] = record.student_id
        each_info['user_name'] = record.user.username
        each_info['complete_time'] = record.complete_time
        each_info['attach'] = 'download/'+record.work_name
        each_info['score'] = record.score
        each_info['comment'] = record.comment

        info["homework_info"].append(each_info)

    return jsonify(info)


@app.route('/marking', methods=['GET', 'POST'])
@login_required
def marking():
    from app.forms import MarkingForm
    form = MarkingForm()
    form.course_id.choices += [(r.id, str(r.course_name + " ID:" + r.id)) for r in g.user.courses]
    form.course_id.choices.insert(0, ('', '请选择课程'))
    form.homework_batch.choices += [(i, str(i)) for i in range(1, 15)]
    form.homework_batch.choices.insert(0, (-1, '请选择批次'))
    if request.method == "GET":

        return render_template('marking.html', form=form)
    else:

        if form.validate_on_submit():
            from sqlalchemy import and_
            homework = HomeWork.query.filter(and_(HomeWork.course_id ==form.course_id.data,HomeWork.batch==form.homework_batch.data)).all()
            course_info = Course.query.filter_by(id=form.course_id.data).first()

            for i in homework:
                if i.attach:
                    i.attach = files.url(i.attach)

            return render_template('marking.html', form=form,homework=homework,course_info=course_info)

        return render_template('marking.html',form=form)


@app.route('/create_course', methods=['POST'])
@login_required
def create_course():
    from random import choice
    from string import ascii_uppercase as uc, digits as dg

    course_name = request.values['course_name']
    part1 = ''.join(choice(uc) for j in range(3))  # 三个大写的英文
    part2 = ''.join(choice(dg) for j in range(3))  # 三个随机数字
    invitation_code = part1 + part2
    search_result = Course.query.filter_by(id=invitation_code).first()

    while search_result is not None:
        part1 = ''.join(choice(uc) for j in range(3))  # 三个大写的英文
        part2 = ''.join(choice(dg) for j in range(3))  # 三个随机数字
        invitation_code = part1 + part2

    newcourse = Course(invitation_code, course_name)
    user = User.query.filter_by(id=g.user.id).first()
    newcourse.users.append(user)

    db.session.add(newcourse)
    db.session.commit()

    result = session['result']
    result.append((url_for('t_class_section', course_id=invitation_code),  course_name))
    session.pop('result', None)
    session['result'] = result

    return jsonify(invitation_code)


@app.route('/t_class_section', methods=['GET', 'POST'])
@login_required
def t_class_section():
    if request.method == "GET":
        course_id = request.args.get('course_id')

        homework = HomeWork.query.filter_by(course_id=course_id).all()
        course_info = Course.query.filter_by(id=course_id).first()

        for i in homework:
            if i.attach:
                i.attach = files.url(i.attach)

    return render_template('t_class_section.html', homework=homework, course_info=course_info)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    from app.forms import SignupForm

    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if user is not None:
            form.username.errors.append("用户已经被注册！")
            return render_template('signup.html', form=form)

        if form.id.data.startswith("T"):
            identity = 'T'
        else:
            identity = 'S'

        newuser = User(form.id.data, form.username.data,form.password.data,identity)
        db.session.add(newuser)
        db.session.commit()

        session['id'] = newuser.id
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    from app.forms import LoginForm

    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        user = User.query.filter_by(id=form.id.data).first()
        if user and user.check_password(form.password.data):
            session['id'] = form.id.data
            login_user(user, remember=session['remember_me'])
            return redirect(url_for('index'))

        else:
            return render_template('login.html', form=form, failed_auth=True)

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# @app.route('/init')
# def init():
#     user = User.query.filter_by(id="031602331").first()
#     completion = Completion.query.filter_by(student_id="031602331").first()
#     completion.user.append(completion)
#     return 1;