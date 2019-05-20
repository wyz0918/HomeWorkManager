#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/20 13:19
# @Author  : wyz
# @Site    : 
# @File    : init_sql.py
# @Software: PyCharm


from app import db
from app.models import *

db.drop_all()
db.create_all()

