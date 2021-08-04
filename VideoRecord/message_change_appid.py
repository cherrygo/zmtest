#!/usr/bin/env python
# coding=utf8

import message_record_mq

def sendmq(lessonuid):
    topic = "*"
    body = {"appCode": "kid", "bizType": "1vn", "channel": "agora",
            "lessonUid": lessonuid, "useToken": "true"}
    message_record_mq.send(topic, '', body)

if __name__ == '__main__' :
    sendmq('f6f3b5fb5a6b420c8fffd039b4d64ea3')
