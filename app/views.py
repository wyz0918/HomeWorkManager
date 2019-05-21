from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm,files
from flask import make_response
from app.models import User,HomeWork,Course,ElectiveCourse
import datetime
import re


@lm.user_loader
def load_user(uid):
    return User.query.get(uid)


@app.before_request
def before_request():
    g.user = current_user



@app.route('/marking', methods=['GET', 'POST'])
@login_required
def marking():
    import paramiko
    from app.utils.operations import remote
    from config import basedir
    from app.forms import OperationsForm

    def isup(hostname):
        import socket

        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.settimeout(2)
        try:
            conn.connect((hostname, 22))
            conn.close()
        except:
            return False
        return True

    form = OperationsForm()
    if form.validate_on_submit():
        username = 'dong'
        pkey = basedir + '/sshkeys/id_rsa'

        hostname = form.hostname.data
        cmd = form.cmd.data

        if not isup(hostname):
            return render_template('marking.html', form=form, failed_host=hostname)

        blacklist = ['reboot', 'shutdown', 'poweroff',
                     'rm', 'mv', '-delete', 'source', 'sudo',
                     '<', '<<', '>>', '>']
        for item in blacklist:
            if item in cmd.split():
                return render_template('marking.html', form=form, blacklisted_word=item)

        try:
            out = remote(cmd, hostname=hostname, username=username, pkey=pkey)
        except paramiko.AuthenticationException:
            return render_template('marking.html', form=form, hostname=hostname, failed_auth=True)

        failed_cmd = out.failed
        succeeded_cmd = out.succeeded

        return render_template('marking.html',
                               form=form,
                               cmd=cmd,
                               hostname=hostname,
                               out=out,
                               failed_cmd=failed_cmd,
                               succeeded_cmd=succeeded_cmd)

    return render_template('marking.html', form=form)





@app.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    import os
    import time
    from hashlib import md5
    from app.utils.operations import local
    from app.forms import EditorForm

    form = EditorForm()
    if form.validate_on_submit():
        param_do = form.do_action.data
        file_path = form.file_path.data

        if param_do == 'read':
            file_access = os.access(file_path, os.W_OK)
            if not file_access:
                return render_template('about.html',
                                       form=form,
                                       file_path=file_path,
                                       file_access=file_access)

            with open(file_path, 'rb') as f:
                file_data = f.read()
            f.closed
            form.file_data.data = file_data
            return render_template('about.html',
                                   form=form,
                                   file_path=file_path,
                                   file_access=file_access)

        if param_do == 'save':
            file_access = os.access(file_path, os.W_OK)
            if not file_access:
                return render_template('about.html',
                                       form=form,
                                       file_path=file_path,
                                       file_access=file_access)

            file_md5sum = md5(open(file_path, 'rb').read()).hexdigest()
            form_md5sum = md5(form.file_data.data.replace('\r\n', '\n')).hexdigest()
            if file_md5sum == form_md5sum:
                return render_template('about.html',
                                       form=form,
                                       file_path=file_path,
                                       file_access=file_access,
                                       file_no_change=True)

            postfix = time.strftime("%Y%m%d%H%M%S")
            file_backup = file_path + "." + postfix

            backup_out = local("cp -p {0} {1}".format(file_path, file_backup))
            succeeded_backup = backup_out.succeeded
            failed_backup = backup_out.failed

            file = open(file_path, 'wb')
            file.write(form.file_data.data.replace('\r\n', '\n'))
            file.close()

        return render_template('about.html',
                               form=form,
                               file_path=file_path,
                               file_access=file_access,
                               postfix=postfix,
                               backup_out=backup_out,
                               failed_backup=failed_backup,
                               succeeded_backup=succeeded_backup)

    return render_template('about.html', form=form)


@app.route('/download/<filepath>', methods=['GET'])
@login_required
def download_file(filepath):
    return app.send_static_file(filepath)


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

    if request.method == "GET":
        from app.forms import WorkArrangeForm
        form = WorkArrangeForm()
        form.course_id.choices += [(r.id, str(r.course_name+" ID:"+r.id)) for r in g.user.courses]
        form.course_id.choices.insert(0, ('', '请选择课程'))
        form.homework_batch.choices += [(i, str(i)) for i in range(1,15)]
        form.homework_batch.choices.insert(0, (-1, '请选择作业批次'))
        return render_template('work_arrange.html', form=form)

    if request.method == "POST":

        from app.forms import WorkArrangeForm
        form = WorkArrangeForm()
        form.course_id.choices += [(r.id, str(r.course_name+" ID:"+r.id)) for r in g.user.courses]
        form.course_id.choices.insert(0, ('', '请选择课程'))
        form.homework_batch.choices += [(i, str(i)) for i in range(1,15)]
        form.homework_batch.choices.insert(0, (-1, '请选择作业批次'))

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


@app.route('/create_course', methods=['POST'])
@login_required
def create_course():
    from random import choice
    from string import ascii_uppercase as uc, digits as dg
    from flask import jsonify

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
