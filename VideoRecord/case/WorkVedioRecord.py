#coding:utf8

import requests
from pyExcelerator import *
import xlwt
import re
import json
import unittest
from GetLessonId import GetLessonUid


class workVedioRec(object):

     def __init__(self):
            pass

     def SelectInterface(self,lessouid):
         url = 'http://10.81.56.54:8093/task?lessonUid='
         for i in lessouid:
             r = requests.get(url + i+ '&env=fat')
             re=r.json()
             co=re['code']
             if co==200:
                 lesid=r.json()['data']['lessonUid']
                 dataContent=r.json()['data']['segmentList'][0]['audioFiles'][0]['url']
                 dataContent2 = r.json()['data']['segmentList'][0]['videoFiles'][0]['url']
                 getMp3=r'.mp3'
                 getMp4=r'.mp4'
                 pattern = re.compile(getMp3)
                 matchObj = pattern.findall(dataContent)
                 pattern = re.compile(getMp4)
                 matchObj2 = pattern.findall(dataContent2)
                 if co ==0 and matchObj!= None and matchObj2!= None:
                    print i,"success"
                 else:
                    print i,"mp3或mp4文件不存在"
             else:
                 print i,'该课程不存在'


     def PlayBackInterface(self,lessouid):
         url='http://10.29.180.192:8080/v1/playback/getUrls?lessonUID='
         for i in lessouid:
             geturl = requests.get(url+i)
             re = geturl.json()
             co = re['audio']['state']
             co2 = re['video']['state']
             if co==0 and co2==0:
                 print i,'success'
             else:
                 print i,'录像回放接口失败'


getJesList = []
print('>>> start! ')
queRes = GetLessonUid().query()
print('>>> return: %s' % queRes)
getJes = GetLessonUid().esLessonUid(queRes, getJesList)
print('>>> getJesList=%s' % getJesList)


a=workVedioRec()
result=a.SelectInterface(getJesList)
result=a.PlayBackInterface(getJesList)









