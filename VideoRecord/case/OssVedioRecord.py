#coding:utf8

import requests
import sys
import json
from GetLessonId import GetLessonUid
import oss2
import subprocess
import datetime
import time


sucMP3 =[]
sucMP4 =[]


class OssVedioRec(object):

   def __init__(self):
        pass


   def searchVideo(self,lessouid):
       url = 'https://zm-chat-lessons.oss-cn-hangzhou-internal.aliyuncs.com/'
       for i in lessouid:
           r = requests.head(url+i+'/audio.mp3')
           r2 = requests.head(url + i + '/audio.mp4')
           rlength = r.headers.get('Content-Length')
           r2length = r2.headers.get('Content-Length')
           if r.status_code==200:
               print ('oss mp3 success. lessonUid= %s' % i)
               sucMP3.append(i)
               if rlength == 0:
                   print ('\033[1;35moss mp3 file size is 0 ! lessonUid= %s \033[0m' % i)
           else:
               print ('\033[1;35moss mp3 file is null ! lessonUid= %s \033[0m' % i)

           if r2.status_code==200:
               print ('oss mp4 success. lessonUid=%s' % i)
               sucMP4.append(i)
               if r2length ==0:
                   print ('\033[1;35moss mp4 file size is 0 ! lessonUid=%s \033[0m' % i)
           else:
               print ('\033[1;35moss mp4 file is null ! lessonUid=%s \033[0m' % i)


   def ScreenShotInterface(self,lessonid):
         url = 'https://zms-record-screenshot.oss-cn-hangzhou-internal.aliyuncs.com/'
         for i in lessonid:
             r = requests.head(url + i + '/screenshot.zip')
             if r.status_code==200:
                 print i,'success'
             else:
                 print i, '截图不存在'


   def lessonLen(self,lesid):
               url = 'http://10.81.56.54:8093/task?lessonUid='
               r = requests.get(url + lesid + '&env=fat')
               segmentEnd = r.json()['data']['segmentList']
               segmentStart = r.json()['data']['lessonStartTime']
               endTime = segmentEnd[len(segmentEnd) - 1]['endTime']
               timeStamp = float(endTime / 1000)
               timeArray = time.localtime(timeStamp)
               otherStyleEndTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
               d1 = datetime.datetime.strptime(otherStyleEndTime, '%Y-%m-%d %H:%M:%S')
               timeStamp2 = float(segmentStart / 1000)
               timeArray2 = time.localtime(timeStamp2)
               otherStyleStartTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray2)
               d2 = datetime.datetime.strptime(otherStyleStartTime, '%Y-%m-%d %H:%M:%S')
               fanTime = float((d1 - d2).seconds)
               return fanTime


   def getAllFileLen(self,sucMP3,suffix):
          for j in sucMP3:
              mp3Audio = r'https://zm-chat-lessons.oss-cn-hangzhou-internal.aliyuncs.com/%s/audio.%s' % (j, suffix)
              commandMP3Audio = ["ffprobe.exe", "-loglevel", "quiet", "-print_format", "json", "-show_format", "-show_streams",
                          "-i", mp3Audio]
              resultMP3 = subprocess.Popen(commandMP3Audio, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
              outMP3 = resultMP3.stdout.read()
              tempMP3 = outMP3.decode('gbk').encode('utf-8')
              dataMP3 = float(json.loads(tempMP3)["format"]['duration'])
              fanTime = self.lessonLen(j)
              finalNum = dataMP3 - fanTime
              if 0 < finalNum < 15:
                  print ('oss %s success ! lessonUid=%s' %(suffix, j) )
              else:
                  print ('\033[1;35moss %s size and true size not same ! finalNum=%s , lessonUid=%s \033[0m' % (
                  suffix, finalNum, j))


getJesList = []
print('>>> start! ')
queRes = GetLessonUid().query()
print('>>> return: %s' % queRes)
getJes = GetLessonUid().esLessonUid(queRes, getJesList)
print('>>> getJesList=%s' % getJesList)
print('>>> lessonUid num=%s' % len(getJesList))

OssVedioRec().searchVideo(getJesList)
# OssVedioRec().ScreenShotInterface(getJesList)
OssVedioRec().getAllFileLen(sucMP3, "mp3")
OssVedioRec().getAllFileLen(sucMP4, "mp4")

















