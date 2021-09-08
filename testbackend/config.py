#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
import warnings
import pymysql
from testbackend.logger import LOGGING


resource_path = sys.path[0] + '/resource'

# init backend
print("backend start")
# connect db
print("connect db success")
db=pymysql.connect(host="localhost",user="root",password="123456",database="DigitalRMB")#本机数据库连接


# init logger
# 获取一个logger对象
logger = logging.getLogger("DigitalRMB")

