from flask_wtf import Form
from wtforms import StringField, BooleanField, SelectField, TextAreaField, SubmitField, \
    PasswordField, ValidationError, RadioField
from wtforms.validators import DataRequired, Email, EqualTo
from app import db


class SignupForm(Form):
    username = StringField('Username', validators=[DataRequired("请输入用户名.")])

    password = PasswordField('Password', validators=[DataRequired("请输入密码."),
                                                     EqualTo('confirm', message="密码必须一致")])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired("请输入用户名.")])
    password = PasswordField('Password', validators=[DataRequired("请输入密码.")])
    remember_me = BooleanField('remember_me', default=False)


class OperationsForm(Form):
    do_action = StringField('Action')
    hostname = StringField('Hostname', validators=[DataRequired()])
    cmd = StringField('Command', validators=[DataRequired()])


class RacktablesForm(Form):
    do_action = StringField('Action')
    objectname = StringField('Object Name')
    objecttype_choices = [('online_mode', 'Online Mode'),
                          ('offline_mode', 'Offline Mode'),
                          ('patch_panel', 'Patch Panel'),
                          ('network_switch', 'Network Switch'),
                          ('pdu', 'PDU'),
                          ('network_security', 'Network Security')]
    objecttype = RadioField('Object Type', choices=objecttype_choices)
    rackspace = StringField('Rackspace')
    rackposition_choices = [('none', 'rackposition'),
                            ('left', 'left'), ('right', 'right'),
                            ('front', 'front'), ('interior', 'interior'), ('back', 'back')]
    rackposition = SelectField('Rackposition', choices=rackposition_choices)


class EditorForm(Form):
    do_action = StringField('Action')
    file_path = StringField('File Path', validators=[DataRequired()])
    file_data = TextAreaField('File Data')


class HadoopForm(Form):
    do_action = StringField('Action')
    slave_hostname = StringField('Slave Hostname')
    choices = [('none', 'master_hostname'),
               ('idc1-hnn1', 'idc1-hnn1'), ('idc2-hnn1', 'idc2-hnn1'),
               ('idc1-hrm1', 'idc1-hrm1'), ('idc2-hrm1', 'idc2-hrm1')]
    master_hostname = SelectField('Master Hostname', choices=choices)
