# coding:utf8
import requests
import MySQLdb
import pandas as pd
import time
import datetime


#公共参数
zmhost="http://*/"
trhost="http://*/"
courseId="p_63b67043-bff6-465c-b622-6aa0f08977c4"
head={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64)",
             "Content-Type": "application/json",
             "Accept-Encoding": 'zh-CN',
             "userId":"828"}

#连接mysql
db = MySQLdb.connect(host="*",port=3306,user="*",passwd="*",db="kids-game-resources",charset='utf8')


class CourseWare(object):

   def __init__(self):
        pass


   #修改课件使用场景
   def updata(self):
       url = zmhost + 'mgr/courseware/update'
       payload = {"coursewareId": courseId,
                  "directoryId": 302
                  }
       response = requests.post(url, json=payload, headers=head)
       print "=======", response.text


   #课件上传
   def CourseWareUpLoad(self,courseid):
       remarks = "testtesttest"
       url = zmhost+'mgr/courseware/upload'
       payload={"coursewareId":courseid,
                "remark":remarks
               }
       response =requests.post(url,json=payload,headers=head)
       versionCode=response.json()['data']['versionCode']
       return versionCode


   #课件上架
   def CourseWareupAndDown(self):
       time.sleep(60)
       cursor = db.cursor()
       sql="select * from backup_courseware where courseware_id='%s' ORDER BY id DESC limit 1" % courseId
       try:
           cursor.execute(sql)
           data = cursor.fetchall()
           for row in data:
               id = row[0]
               version = row[3]
               print "id=%s,version=%s" % \
                     (id, version)
               # sqlmanifest = "UPDATE backup_courseware SET manifest='' where id=%s" % id
               # cursor.execute(sqlmanifest)
               # db.commit()
       except:
           print "Error: unable to fecth data"
       vsurl= zmhost+'/tools/des/encrypt/version?version=%s' % version
       vs= requests.get(vsurl)
       versioncode= vs.json()['data']
       url = zmhost+'mgr/backUpCourseWareService/upOrDown'
       payload={
                "action": 1,
                "versionCode": versioncode,
                "courseWareId": courseId
               }
       response =requests.post(url,json=payload,headers=head)
       manifest='select manifest from backup_courseware where courseware_id = %s ORDER BY id DESC limit 1' % courseId
       db.close()
       print "上架=======",response.text
       return manifest

   #tr绑定课堂
   def editorZmg(self):
       manifest=self.CourseWareupAndDown()
       mouth_time = datetime.datetime.now().month
       hour_time=datetime.datetime.now().hour
       name= "cherry"+str(mouth_time)+str(hour_time)
       if courseId.startswith('P_'):
           fourthId=89147
       else:
           fourthId=89243
       url = trhost + 'formalCourseware/create/editorZmg'

       payload = {
              "classRank": 0,
              "courseSystemFirstId": 89079,
              "courseSystemFourthId": fourthId,
              "courseSystemSecondId": 89080,
              "courseSystemThirdId": 89146,
              "description": "string",
              "difficulty": 1,
              "edition": "cherry的正式课体系",
              "editionId": 342,
              "editorGameUid": courseId,
              "grade": "小一",
              "gradeCode": "PRIMARY_SCHOOL_1",
              "manifest": manifest,
              "name": name,
              "prepareVideoMaterialId": 1,
              "prepareVideoMaterialUrl": "http://blabla",
              "scenes": [
                2,3,4,5
              ],
              "subject": "数学",
              "subjectCode": "math",
              "videoMaterialId": 1,
              "videoUrl": "http://lalala"

                  }
       response = requests.post(url, json=payload, headers=head)
       data=response.json()['data']
       print "=======", data
       return data


   # tr上架
   def state(self):
       data=self.editorZmg()
       url = trhost + '/formalCourseware/update/state'
       payload = {"coursewareId": data,
                  "targetBizState": 1
                  }
       response = requests.post(url, json=payload, headers=head)
       print "=======", response.text


CourseWare().updata()
CourseWare().CourseWareUpLoad(courseId)
CourseWare().state()
