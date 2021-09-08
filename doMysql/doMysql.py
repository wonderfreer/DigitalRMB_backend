#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/3 9:36
# @Author  : WangFei
# @Des     :
import pymysql
import testbackend.config as config
import json
import logging
db=config.db
logger=config.logger
#user_apply_info_table 用户注册信息表
user_apply_info_table="user_apply_info"  #用户注册信息表
user_bank_card_table="user_bankcard_info"    #用户绑定银行卡信息表
name_idcard_table="name_idcard_info"

keylist=["RMB_opreating_agency","name","IDcard_type","IDcard_number","mobile_number","university","faculty","major"]



#db=pymysql.connect("localhost","root","123","mytestdb")#本机数据库连接
#db.close()#关闭数据库
#print("db has close.")
#远程连接数据库
# db = pymysql.connect(
#          host='192.168.100.110',
#          port=3306,
#          user='root',
#          passwd='123456',
#          db ='库名',
#          charset='utf8'
#          )

def print_user_info(user_info):
    #for i,j in enumerate(user_info):
    for val in user_info:
        print(val,end=" ")
    print("")


#验证姓名、身份证号的准确性
#错误返回0，正确返回1
def judge_name_id(name,IDcard_number):
    #sql="select * from name_idcard_tables where IDcard_number="+IDcard_number + "and name="+name
    sql = "select * from {tablename} where IDcard_number='{IDcard_number}' and name='{name}';".format(tablename=name_idcard_table,IDcard_number=IDcard_number,name=name)
    #print(sql)

    try:
        with db.cursor() as cursor:  # 使用cursor()方法获取操作游标
            cursor.execute(sql)  # 执行sql语句
            select_result = cursor.fetchone()  # 返回数据库查询的一条信息，用元组显示
            if select_result is None:
                print("****  user name doesn't match IDcard number")
                logger.warn("user name doesn't match IDcard number")
                return 0
            else:
                print("the user name is correct with IDcard number")
                print(select_result)
                logger.info("the user name is correct with IDcard number")
                logger.info(select_result)

                return 1
    except Exception as e:
        print(e)
        logger.error(e)
    return -1



#查询所有的用户记录
def search_record_all():
    #查询不是原子操作
    sql="select * from {tablename};".format(tablename=user_apply_info_table)
    try:
        with db.cursor() as cursor: #使用cursor()方法获取操作游标
            cursor.execute(sql) #执行sql语句
            select_result = cursor.fetchall()   #返回数据库查询的所有信息，用元组显示
            if select_result is None:
                print("no record")
            else:
                for record in select_result:
                    print_user_info(record)
                    #print(record)
    except Exception as e:
        print(e)

#通过身份证查询一条用户记录
#0为未查到，1为查到
def search_record_by_IDcard_number(IDcard_number):

    sql="select * from {tablename} where IDcard_number='".format(tablename=user_apply_info_table)+IDcard_number+"';"
    try:
        with db.cursor() as cursor:  # 使用cursor()方法获取操作游标
            cursor.execute(sql)  # 执行sql语句
            select_result = cursor.fetchone()  # 返回数据库查询的一条信息，用元组显示
            if select_result is None:
                print("User is not registered， you can sign in")
                logger.info("User is not registered， you can sign in")
                return 0
            else:
                print("User is already registered")
                print_user_info(select_result)
                logger.warn("User is already registered")

                return 1
    except Exception as e:
        print(e)
        logger.error(e)
        return -1

#插入一条用户信息记录
def inser_record(jsondata):
    #jsondata={"subject":"bbb","start_date":"2022-07-21","end_date":"2023-07-21","description":"mysql test2222"}
    #jsondata={"RMB_opreating_agency":"1","name":"王2","IDcard_type":"1","IDcard_number":"130988200001011235","mobile_number":"12345678910","university":"北京航空航天大学","faculty":"计算机学院","major":"计算机技术"}
    #jsda=json.loads(jsondata)
    jsda=jsondata
    # #keylist = ["RMB_opreating_agency", "name", "IDcard_type", "IDcard_number", "mobile_number", "university", "faculty","major", "bank_id", "card_number"]

    # keyliststr=""
    # valuesliststr=""
    # for key in jsondata:
    #     keyliststr+=key+","
    #sql = "INSERT INTO {0}(description,subject, start_date, end_date) VALUES('{1}','{2}', '{3}','{4}');".format(user_apply_info_table,jsondata["description"],jsondata["subject"],jsondata["start_date"],jsondata["end_date"])
    sql="INSERT INTO {0} VALUES('{1}', '{2}','{3}','{4}','{5}','{6}','{7}','{8}');".format(user_apply_info_table, jsda["RMB_opreating_agency"],jsda["name"],jsda["IDcard_type"],jsda["IDcard_number"],jsda["mobile_number"],jsda["university"],jsda["faculty"],jsda["major"])
    #print(sql)
    try:
        with db.cursor() as cursor:
            cursor.execute(sql)
        db.commit()
        print ("insert success")
        logger.info("insert success")
    except Exception as e:
        print ("insert error")
        print(e)
        logger.error("insert error")
        logger.error(e)
        db.rollback()



#通过银行卡号查询一条记录
def search_record_by_bankcard_number(bankcard_number):
    #sql = "select * from {tablename} where card_number='".format(tablename=user_bank_card_table) + bankcard_number + "';"
    sql = "select * from {tablename} where bank_card_number='{bank_card_number}';".format(tablename=user_bank_card_table,bank_card_number=bankcard_number)
    #print(sql)
    try:
        with db.cursor() as cursor:  # 使用cursor()方法获取操作游标
            cursor.execute(sql)  # 执行sql语句
            select_result = cursor.fetchone()  # 返回数据库查询的一条信息，用元组显示
            if select_result is None:
                print("the bankcard number is new")
                logger.info("the bankcard number is new")
                return 0
            else:
                print("the bankcard number is bond")
                logger.warn("the bankcard number is bond")
                #print(select_result)
                return 1
    except Exception as e:
        print(e)
        logger.error(e)
        return -1

#插入一条银行卡信息记录
def inser_bank_card_record(jsondata):
    #jsondata={"IDcard_number":"130988200001011234","bank_id":"1","card_number":"620000000000000001"}
    jsda = jsondata
    sql = "INSERT INTO {0} VALUES('{1}','{2}', '{3}');".format(user_bank_card_table,jsda["card_holder"], jsda["bank_card_number"], jsda["mobile_number"])
    #sql="INSERT INTO tasks(RMB_opreating_agency,name,IDcard_type,IDcard_number,mobile_number,university,faculty,major,bank_id,card_number) VALUES('{0}','{1}', '{2}','{3}','{4}','{5}','{6}','{7}');"
    #print(sql)
    try:
        with db.cursor() as cursor:
            cursor.execute(sql)
        db.commit()
        print ("insert bankcard success")
        logger.info("insert bankcard success")
    except Exception as e:
        print ("insert bankcard error")
        print(e)
        logger.error("insert bankcard error")
        logger.error(e)
        db.rollback()




#test
if __name__ == '__main__':



    jsondata={"RMB_opreating_agency":"1","name":"王飞","IDcard_type":"1","IDcard_number":"130988200001011234","mobile_number":"12345678910","university":"北京航空航天大学","faculty":"计算机学院","major":"计算机技术","bank_id":"1","card_number":"620000000000000001"}
    #jsondata={"subject":"aaa","start_date":"2022-07-21","end_date":"2023-07-21","description":"mysql test"}
    #inser_record(jsondata)
    search_record_all()

    #search_record_by_IDcard_number("130988200001011235")

    #inser_bank_card_record(jsondata)
    #search_record_by_bankcard_number("620000000002")

    judge_name_id("金祥海","411402198907096732")
    judge_name_id("金祥海", "41140219890709673X")

