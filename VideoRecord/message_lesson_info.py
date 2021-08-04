#!/usr/bin/env python
# coding=utf8

import message_record_mq

def send(lessonUid):
    topic = "*"
    body = {
        "data": {
            "lesUid": lessonUid,
            "studentId": 0,
            "studentPhoneNo": "0",
            "teacherId": 0,
            "teacherPhoneNo": "0"
        }
    }
    message_record_mq.send(topic, 'lesson-info', body)

if __name__ == '__main__' :
    send('6337ac56e2c742909ffaeffb0f91a8c6')
