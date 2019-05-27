from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, files
from flask import make_response
from app.models import User, HomeWork, Course, ElectiveCourse, Completion, AdditionalStudentInfo
import time
import re
import os, base64


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

    print (homework_id)
    print (student_id)

    completion = Completion.query.filter(and_(Completion.homework_id == homework_id,
                                              Completion.student_id == student_id)).first()

    if completion:
        completion.comment = comment
        completion.score = score

        db.session.add(completion)
        db.session.commit()

        message = "提交评分和评语成功！"
    else:
        message = "提交评分和评语失败！"

    return jsonify(message)


@app.route('/download/<filename>', methods=['GET'])
@login_required
def download_file(filename):
    import os
    from flask import send_from_directory
    directory = os.getcwd() + '/app/static/homeworks'
    return send_from_directory(directory, filename, as_attachment=True)


@app.route('/index', methods=['GET'])
@login_required
def index():
    result = []
    for i in g.user.created_courses:
        result.append((url_for('t_class_section', course_id=i.id), i.course_name))

    session.pop('result', None)
    session['result'] = result

    return render_template('index.html', result=result)


@app.route('/work_arrange', methods=['GET', 'POST'])
@login_required
def work_arrange():
    from app.forms import WorkArrangeForm
    import datetime
    form = WorkArrangeForm()
    form.course_id.choices += [(r.id, str(r.course_name + " ID:" + r.id)) for r in g.user.created_courses]
    form.course_id.choices.insert(0, ('', '请选择课程'))
    form.homework_batch.choices += [(i, str(i)) for i in range(1, 15)]
    form.homework_batch.choices.insert(0, (-1, '请选择作业批次'))
    if request.method == "GET":

        return render_template('work_arrange.html', form=form)

    else:
        if form.validate_on_submit():

            if form.attach.data:
                index = None
                for i in range(len(form.attach.data.filename) - 1, -1, -1):
                    if form.attach.data.filename[i] == ".":
                        index = i
                        break
                if index:
                    postfix = form.attach.data.filename[index:]
                else:
                    postfix = ''
                postfix = postfix.lower()
                name = form.course_id.data + "_" + str(form.homework_batch.data) + postfix
                filename = files.save(form.attach.data, name=name)
                file_url = files.url(filename)
            else:
                filename = ""

            # print(form.start_time.data, type(form.start_time.data))
            # print(form.end_time.data, type(form.end_time.data))
            # print(datetime.date.today(), type(datetime.date.today()))
            if form.end_time.data >= datetime.date.today():
                state = "进行中"
            else:
                state = "已截止"
            newhomework = HomeWork(form.course_id.data, form.homework_batch.data,
                                   form.homework_describe.data, filename,
                                   form.start_time.data, form.end_time.data, 0, state)

            db.session.add(newhomework)

            message = "创建作业成功！"

            course = Course.query.filter_by(id=form.course_id.data).first()
            course.homeworks.append(newhomework)
            db.session.add(course)
            db.session.commit()

            return render_template('work_arrange.html', form=form, message=message)

        return render_template('work_arrange.html', form=form)


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
        each_info['user_name'] = record.student.username
        each_info['complete_time'] = record.complete_time
        each_info['attach'] = 'download/' + record.address
        each_info['score'] = record.score if record.score else "暂无"
        each_info['comment'] = record.comment if record.comment else "暂无"

        info["homework_info"].append(each_info)

    each_info = dict()
    each_info["homework_id"] = homework_id
    info["homework_info"].append(each_info)

    return jsonify(info)


@app.route('/', methods=['GET'])
@login_required
def index_or_home():
    if g.user.identity == "T":
        return redirect(url_for('index'))
    else:
        return redirect(url_for('home'))


@app.route('/marking', methods=['GET', 'POST'])
@login_required
def marking():
    from app.forms import MarkingForm
    form = MarkingForm()
    form.course_id.choices += [(r.id, str(r.course_name + " ID:" + r.id)) for r in g.user.created_courses]
    form.course_id.choices.insert(0, ('', '请选择课程'))
    form.homework_batch.choices += [(i, str(i)) for i in range(1, 15)]
    form.homework_batch.choices.insert(0, (-1, '请选择批次'))
    if request.method == "GET":

        return render_template('marking.html', form=form)
    else:

        if form.validate_on_submit():
            from sqlalchemy import and_
            homework = HomeWork.query.filter(
                and_(HomeWork.course_id == form.course_id.data, HomeWork.batch == form.homework_batch.data)).all()
            course_info = Course.query.filter_by(id=form.course_id.data).first()

            course_info.__dict__["num"] = ElectiveCourse.query.filter_by(course_id=form.course_id.data).count()
            for i in homework:
                if i.attach:
                    i.attach = files.url(i.attach)

            return render_template('marking.html', form=form, homework=homework, course_info=course_info)

        return render_template('marking.html', form=form)


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

    newcourse = Course(invitation_code, course_name, g.user.id)
    user = User.query.filter_by(id=g.user.id).first()
    newcourse.creator = user

    db.session.add(newcourse)
    db.session.commit()

    result = session['result']
    result.append((url_for('t_class_section', course_id=invitation_code), course_name))
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

        course_info.__dict__["num"] = ElectiveCourse.query.filter_by(course_id=course_id).count()
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

        newuser = User(form.id.data, form.username.data, form.password.data, identity)
        db.session.add(newuser)
        db.session.commit()

        session['id'] = newuser.id
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index_or_home'))

    from app.forms import LoginForm

    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        user = User.query.filter_by(id=form.id.data).first()
        if user and user.check_password(form.password.data):
            session['id'] = form.id.data
            login_user(user, remember=session['remember_me'])
            return redirect(url_for('index_or_home'))

        else:
            return render_template('login.html', form=form, failed_auth=True)

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index_or_home'))


# @app.route('/init')
# def init():
#     user = User.query.filter_by(id="031602331").first()
#     completion = Completion.query.filter_by(student_id="031602331").first()
#     completion.user.append(completion)
#     return 1;


# @app.route('/home', methods=['GET', 'POST'])
# @login_required
# def home():
#     if request.method == "GET":
#         student_id = request.args.get('student_id')
#         course_id = request.args.get('course_id')
#
#         # ----- 学生的附加信息
#         student_additional_info = AdditionalStudentInfo.query.get(student_id)
#
#         # ----- course_id的课程需要完成的所有作业
#         homeworks_of_course_all = Course.query.get(course_id).homeworks
#
#         # ----- 已经上传的作业和未上传作业
#         homeworks_of_course_complete = list()
#         homeworks_of_course_incomplete = list()
#         completions_of_student = Completion.query.filter_by(student_id=student_id).all()
#         homeworks_of_student_complete = list()
#         for completion in completions_of_student:
#             homeworks_of_student_complete.append(completion.homework)
#         for homework in homeworks_of_course_all:
#             if homework in homeworks_of_student_complete:
#                 homeworks_of_course_complete.append(homework)
#             else:
#                 homeworks_of_course_incomplete.append(homework)


@app.route('/query_course', methods=['GET', 'POST'])
@login_required
def query_course():
    if request.method == "GET":
        course_id = request.args.get('course_id')

        course = Course.query.get(course_id)
        teacher = course.creator
        homeworks = HomeWork.query.filter_by(course_id=course_id).all()
        students = list()
        elective_course_records = ElectiveCourse.query.filter_by(course_id=course_id).all()
        for record in elective_course_records:
            students.append(User.query.get(record.student_id))

        homeworks_num = len(homeworks)
        students_num = len(students)


@app.route('/query_homework', methods=['GET', 'POST'])
@login_required
def query_homework():
    if request.method == "GET":
        homework_id = request.args.get('homework_id')
        homwork = HomeWork.query.get(homework_id)


# 学生主页返回
@app.route("/home", methods=['GET'])
@login_required
def home():
    student = User.query.get(g.user.id)
    student_additional_info = AdditionalStudentInfo.query.get(g.user.id)
    if student_additional_info == None:
        student_additional_info = {"username": None, 'university': None, 'major': None, 'enrollment_year': None,
                                   'college': None, 'birthday': None}
    else:
        student_additional_info = student_additional_info.obj2dict()
    joined_courses = list()
    for joined_course_elect in student.joined_courses:
        joined_courses.append(Course.query.get(joined_course_elect.course_id))
    homeworks = list()
    for joined_course in joined_courses:
        homeworks += joined_course.homeworks
    homeworks_complete = list()
    homeworks_incomplete = list()
    completions_of_student = Completion.query.filter_by(student_id=g.user.id).all()
    homeworks_of_student_complete = list()
    for completion in completions_of_student:
        homeworks_of_student_complete.append(completion.homework)
    for homework in homeworks:
        if homework in homeworks_of_student_complete:
            homeworks_complete.append(homework)
        else:
            homeworks_incomplete.append(homework)
    h_c = []
    for h in homeworks_complete:
        comp = Completion.query.filter_by(student_id=g.user.id, homework_id=h.id).first()
        h = h.obj2dict()
        if comp.score != None:
            h['score'] = comp.score
        else:
            h['score'] = '暂无'
        h_c.append(h)
    res_dict = {
        "student_base_info": student.obj2dict(),
        "student_additional_info": student_additional_info,
        "joined_courses": [j.obj2dict() for j in joined_courses],
        "homeworks_incomplete": [h.obj2dict() for h in homeworks_incomplete],
        # "homeworks_complete": [h.obj2dict() for h in homeworks_complete],
        "homeworks_complete": h_c,
        'info': getinfo()
    }
    return render_template('home.html', content=res_dict)


# 修改个人信息
@app.route("/changemsg", methods=['GET', 'POST'])
@login_required
def changemsg():
    code = '101'
    data = request.get_json()
    student_additional_info = AdditionalStudentInfo.query.get(g.user.id)
    user = User.query.get(g.user.id)
    if data['username'] != '' and data['university'] != '' and data['major'] != '':
        user.username = data['username']
        code = '100'
        if student_additional_info == None:
            s_a_i = AdditionalStudentInfo(user.id, data['enrollment_year'], data['university'], data['college'],
                                          data['major'], data['birthday'])
            db.session.add(s_a_i)
            db.session.commit()
        else:
            student_additional_info.enrollment_year = data['enrollment_year']
            student_additional_info.university = data['university']
            student_additional_info.college = data['college']
            student_additional_info.major = data['major']
            student_additional_info.birthday = data['birthday']
            db.session.commit()
    student_additional_info = AdditionalStudentInfo.query.get(user.id)
    additional_info = {'university': None, 'major': None, 'enrollment_year': None, 'college': None, 'birthday': None}
    if student_additional_info != None:
        additional_info = student_additional_info.obj2dict()
    return jsonify({"code": code, "user": user.obj2dict(), 'student_additional_info': additional_info})


@app.route("/changepw", methods=['GET', 'POST'])
@login_required
# 修改密码
def changepw():
    data = request.get_json()
    code = '101'
    user = User.query.filter_by(id=g.user.id).first()
    if user.check_password(data['oldpassword']):
        user.set_password(data['newpassword'])
        code = '100'
        db.session.commit()
        logout()
    return jsonify({"code": code})


# 获取通知内容
def getinfo():
    infos = []
    user = User.query.get(g.user.id)
    courses = user.joined_courses.all()
    for course in courses:
        homeworks = (Course.query.get(course.course_id)).homeworks.all()
        for homework in homeworks:
            i = {'time': homework.start_time, 'msg': homework.course.course_name + '第' + str(homework.batch) + '批作业已发布'}
            infos.append(i)
    if len(infos) == 0:
        infos = None
    else:
        infos = sorted(infos, key=lambda i: i['time'], reverse=True)
    return infos


# 查找课程
@app.route("/searchcourse", methods=['GET', 'POST'])
@login_required
def search_course():
    data = request.get_json()
    courses = Course.query.filter_by(course_name=data['search_text']).all()
    result = []
    if len(courses) == 0:
        result = None
    else:
        for course in courses:
            c = course.obj2dict()
            c['in_out'] = False
            if ElectiveCourse.query.filter_by(student_id=g.user.id, course_id=course.id).first() != None:
                c['in_out'] = True
            result.append(c)
    return jsonify({"course": result})


# 课程页返回
@app.route("/course")
@login_required
def course():
    # get方法
    if request.method == "GET":
        course_id = request.args.get("id")
        type = request.args.get('type')
        course = Course.query.get(course_id)
        teacher = course.creator
        homeworks = HomeWork.query.filter_by(course_id=course_id).all()
        students = list()
        elective_course_records = ElectiveCourse.query.filter_by(course_id=course_id).all()
        for record in elective_course_records:
            student = User.query.get(record.student_id)
            students.append(student)
            commit_completions = Completion.query.filter_by(student_id=student.id).all()
            homeworks_id = [h.id for h in homeworks]
            commit_homeworks_id = [c.homework_id for c in commit_completions]
            commit_homeworks_id_of_course = [x for x in homeworks_id if x in commit_homeworks_id]
            student.__dict__["temp_commit_num"] = len(commit_homeworks_id_of_course)
        h_w = []
        for h in homeworks:
            h = h.obj2dict()
            if Completion.query.filter_by(student_id=g.user.id, homework_id=h['id']).first() != None:
                h['completion'] = True
            else:
                h['completion'] = False
            h_w.append(h)
        homeworks_num = len(homeworks)
        students_num = len(students)
        res_dict = {
            "course_info": course.obj2dict(),
            "teacher": teacher.obj2dict(),
            "students_num": students_num,
            "students": [s.obj2dict() for s in students],
            "homeworks_num": homeworks_num,
            # "homeworks": [h.obj2dict() for h in homeworks],
            "homeworks": h_w,
            "type": type
        }
        return render_template('course.html', content=res_dict)


@app.route("/summit_homework", methods=['GET', 'POST'])
@login_required
# 提交作业
def summit_homework():
    if request.method == 'POST':
        data = request.get_json()
        datas = data['img'].split(',')
        font = data['font']
        basepath = os.path.dirname(__file__)
        path = os.path.join(basepath, 'static/homeworks/')
        filename = str(g.user.id) + '_' + data['work_id'] + '.' + font
        with open(path + filename, 'wb') as fdecode:
            decode_base64 = base64.b64decode(datas[1])
            fdecode.write(decode_base64)
        c = Completion.query.filter_by(student_id=g.user.id, homework_id=int(data['work_id'])).first()
        if c != None:
            c.address = filename
            db.session.commit()
        else:
            cp = Completion(g.user.id, int(data['work_id']), time.strftime("%Y-%m-%d"), None, None, filename)
            db.session.add(cp)
            HomeWork.query.get(int(data['work_id'])).upload_num += 1
            db.session.commit()
        return jsonify({'code': '100'})
    else:
        return jsonify({'code': '101'})


# 作业页返回
@app.route("/get_homework", methods=['GET', 'POST'])
@login_required
def get_homework():
    data = request.get_json()
    homework_id = data['work_id']
    homework = HomeWork.query.get(homework_id)
    completion = homework.students.filter_by(student_id=g.user.id).first()
    if completion != None:
        completion = completion.obj2dict()
    content = {'homework': homework.obj2dict(), 'completion': completion}
    return jsonify(content)


# 加入课程
@app.route("/add_course", methods=['GET', 'POST'])
@login_required
def add_course():
    data = request.get_json()
    code = '101'
    if data['course_id'] == data['varitify']:
        e_c = ElectiveCourse(g.user.id, data['course_id'])
        db.session.add(e_c)
        db.session.commit()
        code = '100'
    return jsonify({'code': code})
