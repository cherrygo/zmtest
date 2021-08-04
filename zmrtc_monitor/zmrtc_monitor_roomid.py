#!/usr/bin/env python
# coding=utf8

import requests
import datetime as dt
from datetime import datetime


class monitor(object):

   def __init__(self):
        pass

    #后台监控系统登录
   def login(self):
        url = 'http://*/api/account/login'
        head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
        }
        payload ={
            "username": "123456", "password": "zmrtc"
        }
        response = requests.post(url,json=payload,headers=head)
        return response.json()['data']['token']

   #公用header
   def header(self):
        token = self.login()
        hr = {
            "Authorization":"Bearer"+" "+token,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
        }
        return hr


    # 获取所有roomid
   def select(self):
        h = self.header()
        url = 'http://*/api/rooms?pageIndex=1&pageSize=20&startDatetime=2021-02-19%2000%3A00%3A00&endDatetime=2021-02-19%2023%3A59%3A59'
        response = requests.get(url,headers=h)
        roomlist = response.json()['data']['rooms']
        list = []
        for r in roomlist:
            list.append(r['roomId'])
        return list

   #获取码率
   def media_Bit_pub1(self):
       h = self.header()
       rooms = self.select()
       audioError = []
       videoError = []
       for r in rooms:
           url = 'http://*/api/rooms/%s/publish/%s-pub2/data?subUid=%s-pub1&timeSlot=0' %(r,r[0:7],r[0:7])
           response = requests.get(url,headers=h)
           audio = response.json()['data']['pubABitrateCalculatedData']
           video = response.json()['data']['pubVBitrateCalculatedData']
           subAudio = response.json()['data']['subABitrateCalculatedData']
           subVideo = response.json()['data']['subVBitrateCalculatedData']
           if audio:
               audioSum = int(sum(audio)/len(audio))
               if audioSum < 10000:
                  audioError.append(audioSum)
               if audioError:
                  sum(audioError)
                  print 'pub1音频异常数量========' % sum(audioError)
           else :
               print "%s audio is none" % r

           if video:
               videoSum = sum(video) / len(video)
               if videoSum < 200000:
                   videoError.append(videoSum)
               if videoError:
                  sum(videoError)
                  print 'pub1视频异常数量========' % sum(videoError)
           else:
               print "%s video is none" % r



   def media_Bit_pub2(self):
       h = self.header()
       rooms = self.select()
       audioError = []
       videoError = []
       for r in rooms:
           url ='http://*/api/rooms/%s/publish/%s-pub1/data?subUid=%s-pub2&timeSlot=0' %(r,r[0:7],r[0:7])
           response = requests.get(url, headers=h)
           audio = response.json()['data']['pubABitrateCalculatedData']
           video = response.json()['data']['pubVBitrateCalculatedData']
           if audio:
               audioSum = int(sum(audio)/len(audio))
               if audioSum < 10000:
                  audioError.append(audioSum)
               if audioError:
                  sum(audioError)
                  print 'pub2音频异常数量========' % sum(audioError)
           else :
               print "%s audio is none" % r

           if video:
               videoSum = sum(video) / len(video)
               if videoSum < 200000:
                   videoError.append(videoSum)
               if videoError:
                  sum(videoError)
                  print 'pub2视频异常数量========' % sum(videoError)
           else:
               print "%s video is none" % r

# monitor().select()
monitor().media_Bit_pub1()
monitor().media_Bit_pub2()
