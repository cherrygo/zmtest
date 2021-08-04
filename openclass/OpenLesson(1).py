# -*- encoding=utf8 -*-
__author__ = "Administrator"

import requests
import json
import time

#账号
# Teachaccount = "18655550189"
# Teachpassword = "hello0189"
# StudentAccount = "18517720921"
# StudentPassword ="hello0921"
Teachaccount = "17822222460"
Teachpassword = "qinghualaoshi1dui1"
StudentAccount = "13799996122"
StudentPassword ="qinghualaoshi1dui1"



#全局变量
jsonheader = {'Content-Type': 'application/json;charset=utf-8'}
header = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}

#case判断token

class OpenClassJob():
    def Login(self, BasicUrl,teachaccount,teachpassword):
        LoginAPI = BasicUrl + "/api/oauth/login?access_token=undefined"
        LoginParam = {"username":teachaccount,"password":teachpassword,"clientId":"18bd1e36-45e1-45a7-8102-7c6af21a28f2","clientSecret":"SOKnh1IO"}
        result = requests.post(LoginAPI, headers =globals()['header'],data = LoginParam, verify = False)
        print(result)
        resultjson = result.json()
        print(resultjson)
        accesstoken = resultjson['data']['accessToken']
        globals()['header'] = {
                                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
                                'accessToken':accesstoken
                            }
        globals()['jsonheader'] = {
            'Content-Type': 'application/json;charset=utf-8',
            'accessToken': accesstoken
        }
        print("===========time===================")
        print(result.elapsed.total_seconds())
        return accesstoken

    def GeCourseID(self, BasicUrl,teachaccount,teachpassword,access_token):
        basicinfo = BasicUrl + "/api/user/get-basic-info"
        AccessToken = r"?access_token=" + access_token
        TestUrl =basicinfo + AccessToken
        PostParam = {"mobile":teachaccount,"password":teachpassword,"role":"teacher"}
        result = requests.post(TestUrl, headers=globals()['jsonheader'], data=json.dumps(PostParam), verify=False)
        resultjson = result.json()
        print(resultjson)
        teacherID = resultjson['data']['id']
        StuInfo = BasicUrl + "/api/teacher/course-management-list"
        AccessToken = r"?access_token=" + access_token
        TestUrl = StuInfo + AccessToken
        PostParam = {"id" :teacherID,"index":1,"size":1000}
        result = requests.post(TestUrl, headers=globals()['header'], data=PostParam, verify=False)
        resultjson = result.json()
        print(resultjson)
        CrouseID = resultjson['data']['data'][0]['courseId']
        return CrouseID

    def Open1v1Class(self,BasicUrl,teachaccount,teachpassword,time):
        access_token = OpenClassJob().Login(BasicUrl,teachaccount,teachpassword)
        CrouseID = OpenClassJob().GeCourseID(BasicUrl,teachaccount,teachpassword,access_token)
        OpenClass =  BasicUrl + "/api/teacher/finishOpenLesson"
        AccessToken = r"?access_token=" + access_token
        TestUrl = OpenClass + AccessToken
        #知识点：16012
        PostParam = {"beforeStartTime":0,"afterEndTime":0,"duration":30,"mobile":teachaccount,"password":teachpassword,"lessonTypeId":2,"courseId":CrouseID,"keyPoints":16012,"customPoints":"","startTime":time}
        print(PostParam)
        result = requests.post(TestUrl, headers=globals()['header'], data=PostParam, verify=False)
        resultjson = result.json()
        lessonID = resultjson['data']
        if resultjson['code'] == 2:
            return result.json()
        else:
            return lessonID

    def CreateTestEduCourse(self,Mode,Time,Grade,StuAccount,TeaAccount):
        #课程模式1."视频课" 2.
        #[CHINESE_LOGIC 语文思维训练;  ENGLISH_CONCEPT 英语;LEARNING_ABILITY_TRAINING 学习力训练;MATH 数学MATH_LOGIC 数理逻辑训练]
        #PRIMARY_SCHOOL_3  [PRIMARY_SCHOOL_1 小一;  PRIMARY_SCHOOL_2 小二PRIMARY_SCHOOL_3 小三 ;PRIMARY_SCHOOL_4 小四KINDERGARTEN_2 幼儿园中班; KINDERGARTEN_3 幼儿园大班 ;PRESCHOOL_CLASS 学前班]
        Url = "http://open-test.zmlearn.com/api/packet/super/openLesson"
        CourseParam = {"bu": 2,
                       "classMode": Mode,
                       "classType": 0,
                       "duration": 45,
                       "firstStartTime": Time,
                       "grade": Grade,
                       "lessonNum": 1,
                       "studentAccounts": StuAccount,
                       "subject": "MATH_LOGIC",
                       "teacherAccount": TeaAccount,
                       "timeList": [{
                           "day": "4",
                           "startTime": "10:42:00"
                       }]
                       }
        print(CourseParam)
        result = requests.post(Url, headers=globals()['jsonheader'], data=json.dumps(CourseParam), verify=False)
        print(result.json())
        resultCode = result.json()['code']
        return resultCode

    def GetName(self, BaseUrl,Account,pwd):
        RoleList = BaseUrl +"/api/user/getRoleList/" + Account + "?access_token=undefined"
        print(RoleList)
        Roleresult = requests.post(RoleList, headers=globals()['jsonheader'], verify=False)
        RoleJson = Roleresult.json()
        Role = RoleJson['data']['roleList']
        if "seller" in Role:
            Role = "seller"
        print(Role)
        basicinfo = BaseUrl + "/api/user/get-basic-info"
        PostParam = {"mobile":Account,"password":pwd,"role":Role}
        result = requests.post(basicinfo, headers=globals()['jsonheader'], data=json.dumps(PostParam), verify=False)
        resultjson = result.json()
        print(resultjson)
        TeacherName = resultjson['data']['name']
        return TeacherName

class test():
    num = []

    def prt(self, number):
        print(number)

if __name__ == '__main__':
    #OpenClassJob.GetName("https://chat.uat.zmops.cc",Teachaccount,Teachpassword)
    timeNow = time.strftime("%Y-%m-%d %H:%M:%S")
    classA = OpenClassJob()
    classA.CreateTestEduCourse("视频班",timeNow,"PRIMARY_SCHOOL_2",[StudentAccount],Teachaccount)
    # classA.CreateTestEduCourse("图像班", timeNow, "PRIMARY_SCHOOL_2", [StudentAccount], Teachaccount)
    #classA.Open1v1Class("http://x-chat-test.zmlearn.com",Teachaccount,Teachpassword,timeNow)