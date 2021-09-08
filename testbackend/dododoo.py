#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/20 19:47
# @Author  : WangFei
# @Des     :
import json
from django.http import HttpResponse
import testbackend.config as config
logger=config.logger
import urllib
import doMysql.doMysql as doMysql
import requests
from urllib import parse,request

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8',
}


def get_form_data(request):
    json_param = {}
    json_param["name"]=""
    json_param["IDcard_number"]=""

    result={"code":0,"msg":"verification code error"}#-1是验证码错误，0是身份不符，1是用户已经注册，2是注册成功
    #只接受POST请求
    if request.method == 'POST':
        postheader=request.environ
        posttype=postheader["CONTENT_TYPE"]
        print(posttype)
        print(type(posttype))
        #浏览器以json格式传输数据
        if posttype.find('application/json')!=-1:
            postbody = str(request.body, encoding="utf-8")
            print(postbody)
            json_param = json.loads(postbody)
            #print(type(json_param))
            #print(json_param)
            #print(json_param["IDcard_number"])
        # 浏览器以表单格式传输数据
        elif posttype.find('application/x-www-form-urlencoded')!=-1:
            if request.POST:
                json_param["RMB_opreating_agency"] = request.POST.get('RMB_opreating_agency', 12345678910)
                json_param["name"] = request.POST.get('name', 12345678910)
                json_param["IDcard_type"] = request.POST.get('IDcard_type', 12345678910)
                json_param["IDcard_number"] = request.POST.get('IDcard_number', 12345678910)
                json_param["mobile_number"] = request.POST.get('mobile_number', 12345678910)
                json_param["university"] = request.POST.get('university', 12345678910)
                json_param["faculty"] = request.POST.get('faculty', 12345678910)
                json_param["major"] = request.POST.get('major', 12345678910)
                #print(json_param)
            # 表单为空报错
            else:
                print('no params  error post')
                logger.warn("no params  error post")
        # 其他格式传输报错
        else:
            print("posttype error")
            logger.warn("posttype error")
    else:
        print('method error! Please ues POST method')
        logger.error('method error! Please ues POST method')
    print("__________")

    #如果用户姓名与身份证不符，则返回失败
    if doMysql.judge_name_id(json_param["name"],json_param["IDcard_number"])==0:
        print ("user put in error")

        result["code"]=0
        result["msg"]="identity error"
        logger.warn("identity error")
    else:
        #判断用户是否已经注册
        if doMysql.search_record_by_IDcard_number(json_param["IDcard_number"])==1:
            print ("user has signed")
            result["code"] = 1
            result["msg"] = "registered"
            logger.warn("uesr registered")
        else:
            #用户符合条件，注册成功
            doMysql.inser_record(json_param)
            print ("sign in succeed")
            logger.info("user sign in succeed")
            result["code"] = 2
            result["msg"] = "success"
    response = HttpResponse(json.dumps(result, ensure_ascii=False))
    response["Access-Control-Allow-Origin"] = "*"
    return response


def get_SMS(mobile_number):
    url = "http://116.62.192.167:8080/api/send"
    from_data = { "subSys": "eams","phone": mobile_number, "messageContent": "wf"}
    try:
        response = requests.post(url, data=json.dumps(from_data), headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)
        logger.error('Error', e.args)


def test(request):
    result={"msg":"success"}
    response = HttpResponse(json.dumps(result, ensure_ascii=False))
    response["Access-Control-Allow-Origin"] = "*"
    return response

def judge_sms(request):
    mobile_number=123
    result = {"code": 0,"msg":"fail"}
    #只接受POST请求
    if request.method == 'POST':
        postheader=request.environ
        posttype=postheader["CONTENT_TYPE"]
        #print(posttype)
        #浏览器以json格式传输数据
        if posttype.find('application/json')!=-1:
            postbody = str(request.body, encoding="utf-8")
            #print(postbody)
            json_param = json.loads(postbody)
            mobile_number=json_param["mobile_number"]
            #print(type(json_param))
            #print(json_param)
        # 浏览器以表单格式传输数据
        elif posttype.find('application/x-www-form-urlencoded')!=-1:
            if request.POST:
                mobile_number = request.POST.get('mobile_number', 12345678910)
                print(mobile_number)
            # 表单为空报错
            else:
                print('no params  error post')
                logger.warn("no params  error post")
        # 其他格式传输报错
        else:
            print("posttype error")
            logger.warn("posttype error")
    else:
        print('method error! Please ues POST method')
        logger.error("method error! Please ues POST method")
    print("__________")



    jsda = get_SMS(mobile_number)
    print(jsda)
    if jsda["success"]==True:
        result["code"]=1    #验证码已发送到您邮箱，请查收
        result["msg"]="success"
        logger.info("msg send success")
    response = HttpResponse(json.dumps(result, ensure_ascii=False))
    response["Access-Control-Allow-Origin"] = "*"
    return response

def bind_bank(request):
    result = {"code": 0, "msg": "fail"}  # 0为绑定失败，该银行卡已被绑定；1为绑定成果
    json_param={}
    json_param["card_holder"]=""
    json_param["bank_card_number"]=""
    json_param["mobile_number"]=""
    # 只接受POST请求
    if request.method == 'POST':
        postheader = request.environ
        posttype = postheader["CONTENT_TYPE"]
        #print(posttype)
        # 浏览器以json格式传输数据
        if posttype.find('application/json')!=-1:
            postbody = str(request.body, encoding="utf-8")
            #print(postbody)
            json_param = json.loads(postbody)
            #print(type(json_param))
            #print(json_param)
        # 浏览器以表单格式传输数据
        elif posttype.find('application/x-www-form-urlencoded')!=-1:
            if request.POST:
                json_param["card_holder"] = request.POST.get('card_holder', 12345678910)
                json_param["bank_card_number"] = request.POST.get('bank_card_number', 12345678910)
                json_param["mobile_number"] = request.POST.get('mobile_number', 12345678910)
            # 表单为空报错
            else:
                print('no params  error post')
                logger.warn("no params  error post")
        # 其他格式传输报错
        else:
            print("posttype error")
            logger.warn("posttype error")
    else:
        print('method error! Please ues POST method')
        logger.error('method error! Please ues POST method')
    print("__________")

    if doMysql.search_record_by_bankcard_number(json_param["bank_card_number"])==1:
        result["code"]=0
        print("bank card number has signed in")
        logger.warn("bank card number has signed in")
    else:
        doMysql.inser_bank_card_record(json_param)
        result["code"] = 1
        result["msg"]="success"
        logger.info("bank card bind success")
    response = HttpResponse(json.dumps(result, ensure_ascii=False))
    response["Access-Control-Allow-Origin"] = "*"
    return response



#test
if __name__ == '__main__':
    pass