#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
import warnings
import pymysql


resource_path = sys.path[0] + '/resource'

# init backend
print("backend start")
# connect db
print("connect db success")
db=pymysql.connect(host="localhost",user="root",password="123456",database="DigitalRMB")#本机数据库连接

