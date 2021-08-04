#coding:utf8

import requests
import datetime
import time
import subprocess
import json
from itertools import groupby
from operator import itemgetter
from WonderfulVideoModel import WonderfulVideoModel
from GetLessonId import GetLessonUid

onOffNum = []


class OssWonderfulVideoRec(object):
    def __init__(self):
        pass


    def searchWonderfulVideo(self):
        for of in onOffNum:
            for index in range(0,of.values()[0][0][1]):
                url = 'https://zm-chat-lessons.oss-cn-hangzhou-internal.aliyuncs.com/%s/awesome/%s/0_%s.mp4' % (of.keys(),of.values()[0][0][0],index)
                r = requests.head(url)
                if r.status_code == 200:
                    print ('oss WonderfulVideo mp4 success. lessonUid= %s 、uid= %s' % (of.keys(),of.values()[0][0][0]))
                else:
                    print ('\033[1;35m oss WonderfulVideo mp4 file is null ! lessonUid= %s 、uid= %s \033[0m' % (of.keys(),of.values()[0][0][0]))




    def queryParam(self,lessonuid):
        for les in lessonuid:
            url = 'http://10.81.56.54:8093/task?lessonUid=%s&env=fat' % les
            r = requests.get(url)
            users = r.json()['data']['userInfos']
            onstageMapValue = r.json()['data']['onstageMap']
            offstageMapValue = r.json()['data']['offstageMap']
            addUsers = []
            for key in onstageMapValue:
                for key2 in offstageMapValue:
                    while key == key2:
                        lesOnOffNum = []
                        value = onstageMapValue[key]
                        value2 = offstageMapValue[key]
                        upDownTime = []
                        addles = []
                        for item in users:
                            userid = item.get('userId')
                            role = item.get('role')
                            if key == userid and role != "teacher":
                                uid = item.get('uid')
                                lesOnOffNum.append((uid, len(value)))
                                onOffNum.append({les: lesOnOffNum})
                                print onOffNum
                            else:
                                print 'userId and uid not same'
                        for index in range(len(value)):
                            time = value[index]
                            time2 = value2[index]
                            upDownTime.append((time, time2))
                        addUsers.append([{'uid': uid, 'upDownTimes': upDownTime}])
                    addles.append([{'lessonUid': les, 'users': addUsers}])
                    print "addles %s" % addles
                    break


    def upTimeLen(self, lesid):
        for les in lesid:
            url = 'http://10.81.56.54:8093/task?lessonUid=%s&env=fat' % les
            r = requests.get(url)
            users = r.json()['data']['userInfos']
            onstageMapValue = r.json()['data']['onstageMap']
            offstageMapValue = r.json()['data']['offstageMap']
            addUsers = []
            for key in onstageMapValue:
                value = onstageMapValue[key]
                value2 = offstageMapValue[key]
                upDownTime = []
                addles = []
                uid = 0
                for item in users:
                    userid = item.get('userId')
                    if userid == key:
                        uid = item.get('uid')
                        break;
                for index in range(len(value)):
                    time = value[index]
                    time2 = value2[index]
                    upDownTime.append((time, time2))
                addUsers.append([{'uid': uid, 'upDownTimes': upDownTime}])
            addles.append([{'lessonUid': les, 'users': addUsers}])
            print "addles %s" % addles



    def getMp4Len(self):
        for of in onOffNum:
            for index in range(0, of.values()[0][0][1]):
                url = 'https://zm-chat-lessons.oss-cn-hangzhou-internal.aliyuncs.com/%s/awesome/%s/0_%s.mp4' % (of.keys(), of.values()[0][0][0], index)
                commandMP4 = ["ffprobe.exe", "-loglevel", "quiet", "-print_format", "json", "-show_format",
                                   "-show_streams",
                                   "-i",url]
                resultMP4 = subprocess.Popen(commandMP4, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                outMP4 = resultMP4.stdout.read()
                tempMP4 = outMP4.decode('gbk').encode('utf-8')
                dataMP4 = float(json.loads(tempMP4)["format"]['duration'])
                fanTime = self.upTimeLen()
                finalNum = dataMP4 - fanTime
                print finalNum



getJesList = []
get1vnLessonUidJesList = []
print('>>> start! ')
queRes = GetLessonUid().query()
resList = GetLessonUid().es1vnLessonUid(queRes,getJesList,get1vnLessonUidJesList)
print('>>> get1vnLessonUidJesList=%s' % get1vnLessonUidJesList)
print('>>> 1vnLessonUid num=%s' % len(get1vnLessonUidJesList))
OssWonderfulVideoRec().queryParam(get1vnLessonUidJesList)
# OssWonderfulVideoRec().searchWonderfulVideo()
# OssWonderfulVideoRec().upTimeLen(get1vnLessonUidJesList)
# OssPartVedioRec().getMp4Len()
# OssPartVedioRec().is_odd()
