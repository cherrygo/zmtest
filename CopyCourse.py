# coding:utf8
import requests


class CourseWare(object):

   def __init__(self):
        pass


   #获取prod课件json
   def getProdCourse(self):
       url = 'https://*/kidsGameApi/tools/courseware/query/copyJson?courseWareId=80f34b79-2c1c-4a78-8bfe-bfd6607c9d5b&currentUserId=7'
       payload = {"courseWareId": "p_efa9c4c8-ed28-4f2e-a397-6a276aa5a4f7",
                  "currentUserId": 7
                  }
       response = requests.get(url, json=payload)
       print "=======", response.text
       return response.json()['data']

   # 复制到fat
   def copyToFat(self):
       url = 'http://*/kidsGameApi/tools/courseware/save/copyJson'
       jsondata=self.getProdCourse()
       head={
             "currentUserId": "7"
             }
       payload = {
           "copyCourseWareJson": jsondata
                  }
       response = requests.get(url, json=payload,headers=head)
       print "=======", response.text

   #复制到uat
   def copyToUat(self):
       url = 'http://*/kidsGameApi/tools/courseware/save/copyJson'
       jsondata=self.getProdCourse()
       head={
             "currentUserId": "1013483358"
             }
       payload = {
           "copyCourseWareJson": jsondata
                  }
       response = requests.get(url, json=payload,headers=head)
       print "=======", response.text

   #获取课件的名称
   def copyToUat(self,course):
       url = 'http://*/kidsGameApi/tools/courseware/save/copyJson'
       jsondata = self.getProdCourse()
       head = {
           "currentUserId": "1013483358"
       }
       payload = {
           "copyCourseWareJson": jsondata
       }
       response = requests.get(url, json=payload, headers=head)
       print "=======", response.text
