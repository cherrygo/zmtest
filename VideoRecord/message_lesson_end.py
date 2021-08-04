#!/usr/bin/env python
# coding=utf8

import time
import message_record_mq


def end(lessonUid, bu, channel):
    if (0 == bu):
        topic = "*"
    else:
        topic = "*"
    body = {
        "businessType": bu,
        "firstChannel": channel,
        "lessonEndTime": int(round(time.time() * 1000)),
        "lessonUID": lessonUid,
        "lessonType": "regular-lesson"
    }
    message_record_mq.send(topic, 'lesson-end', body)


def end_mkl(lessonUid):
    body = {
        "lessonUID": lessonUid,
        "duration": 60
    }
    message_record_mq.send_mkl('*', 'lesson_end', body)


if __name__ == '__main__':
    # for i in range(1, 5):
    #     lesuid = '7ab8b624d85141b495d15edc6c0a2869' + '-' + '1vn' + str(i)
    #     end(lesuid, 0, 'agora')
        # end_mkl('mkl-3')
    lesuid = 'b4b156fa97ce40c288128d6607080aa1-1v12'
    end(lesuid, 1, 'agora')