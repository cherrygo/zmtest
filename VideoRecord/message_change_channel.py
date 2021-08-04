#!/usr/bin/env python
# coding=utf8

import time
import message_record_mq

def change_redundant(lessonUid, bu, channel, realLessonUid, audioUid, videoUid, singleStreamUid):
    if (0 == bu):
        topic = "*
    else:
        topic = "*"
    body = {
        "businessType": bu,
        "switchChannel": channel,
        "lessonUID": lessonUid
    }
    recordParams = body['recordParams'] = {
        'key': 'wXGIypUQh30qz5rv'
    }
    if None != realLessonUid and len(realLessonUid) > 0 and lessonUid != realLessonUid:
        recordParams['type'] = 1
        recordParams['realLessonUid'] = realLessonUid
        recordParams['parentLessonUid'] = realLessonUid
        recordParams['channelUidMap'] = {
            'audio': audioUid,
            'video': videoUid,
            'singleStream': singleStreamUid
        }

    message_record_mq.send(topic, 'change-channel', body)

def change(lessonUid, bu, channel):
    change_redundant(lessonUid, bu, channel, None, None, None, None)


if __name__ == '__main__' :
    change_redundant('e1e699e8514f4adcb821a6fdea0fa01b-1v12', 1, 'zmrtc', 'e1e699e8514f4adcb821a6fdea0fa01b', 21,25,23)
