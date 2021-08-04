#!/usr/bin/env python
# coding=utf8

import time
import message_record_mq



def start_redundant(lessonUid, bu, channel, realLessonUid, audioUid, videoUid, video2Uid,singleStreamUid, layout, cluster, workerIp,options = {}):
    if (0 == bu):
        topic = "*"
    else:
        topic = "*"
    body = {
        "businessType": bu,
        "duration": 120,
        "firstChannel": channel,
        "lessonStartTime": int(round(time.time() * 1000)),
        # "lessonStartTime":1617863920600,
        "lessonUID": lessonUid,
        "lessonType": "regular-lesson",
        #旁听课参数
        "excellentTeacherLesson": True
    }
    # 竖屏课参数
    if None != layout:
        body['actualScreen'] = layout
    recordParams = body['recordParams'] = {
        'key': 'wXGIypUQh30qz5rv'
    }
    # 冗余录制参数
    if None != realLessonUid and len(realLessonUid) > 0 and lessonUid != realLessonUid:
        recordParams['type'] = 1
        recordParams['realLessonUid'] = realLessonUid
        recordParams['parentLessonUid'] = realLessonUid
        recordParams['channelUidMap'] = {
            'audio': audioUid,
            'video': videoUid,
            'singleStream': singleStreamUid,
            'video2': video2Uid
        }
    # 重试的录制请求
    if None != cluster and len(cluster) > 0:
        recordParams['recommendEnv'] = cluster
    #指定worker ip
    if None != workerIp and len(workerIp) > 0:
        recordParams['workerIp'] = workerIp
    # 1vN暑期课堂
    if None != options:
        if 'req001' in options:
            recordParams['req001'] = options['req001']
        if 'userInfos' in options:
            body['recordUserInfos'] = options['userInfos']

    message_record_mq.send(topic, 'lesson-start', body)



# 正常录制
def start(lessonUid, bu, channel):
    start_redundant(lessonUid, bu, channel, None, None, None, None, None)


# 营销直播课
def start_mkl(lessonUid):
    body = {
        "lessonUID": lessonUid,
        "duration": 60,
        "actualStartTime": int(round(time.time() * 1000))
    }
    message_record_mq.send_mkl('*', 'lesson_start', body)

#1vN课堂
def start_req001(env, lessonUid, studentIds, teacherIds, options=None):
    if 'fat' == env:
        topic = '*'
    elif 'uat' == env:
        topic = '*'

    body = {
        'lessonUid': lessonUid,
        'lessonType': 2,
        'lessonMode': 3
    }
    if not None == studentIds:
        studentList = []
        for studentId in studentIds:
            studentList.append({'userId': studentId, 'position': 'student'})
        body['studentList'] = studentList
    if not None == teacherIds:
        teacherList = []
        for teacherId in teacherIds:
            teacherList.append({'userId': teacherId, 'position': 'teacher'})
        body['teacherList'] = teacherList
    recordParams = body['recordParams'] = {
        'key': 'wXGIypUQh30qz5rv'
    }

    if None != options:
        if 'realLessonUid' in options:
            realLessonUid = options['realLessonUid']
            if lessonUid != realLessonUid:
                recordParams['type'] = 1
                recordParams['realLessonUid'] = realLessonUid
                recordParams['parentLessonUid'] = realLessonUid
        if 'channelUidMap' in options:
            recordParams['channelUidMap'] = options['channelUidMap']
        if 'cluster' in options:
            recordParams['recommendEnv'] = options['cluster']
        if 'workerIp' in options:
            recordParams['workerIp'] = options['workerIp']

    message_record_mq.sendToApp('11159', topic, 'lesson_start', body, env)



if __name__ == '__main__':
    # start_mkl('mkl-3')
    # layout = vertical
    # #cluster ='VPC'
    bu = 1
    for i in range(2,3):
        lesuid = 'b4b156fa97ce40c288128d6607080aa1' + '-' + '1v1' + str(i)
        audioUid = 1 + i
        videoUid = 2 + i
        singleStreamUid = 3 + i
        if bu == 1:
            start_redundant(lesuid, bu, 'agora', 'b4b156fa97ce40c288128d6607080aa1', audioUid,
                            videoUid, singleStreamUid,None,None, None, None)
        else:
            video2Uid = 4 + i
            start_redundant(lesuid, bu, 'agora', '326259edc4fd4a56a1f035d5066df0b2', audioUid,
                            videoUid, singleStreamUid,video2Uid, None, None, None,
                            options={'req001': True})

    # start_req001('fat','a14ed8f97e88d7baa61ebffe8381974d-1vn1',['1557581454','1557581460','1557581461','1557581464','1557581470'],['1557580954'],
    #              {'realLessonUid': 'a14ed8f97e88d7baa61ebffe8381974d',"channelUidMap":{"audio":11,"video":22}})

