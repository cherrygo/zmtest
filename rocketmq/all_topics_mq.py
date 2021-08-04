#!/usr/bin/env python
# coding=utf8

from mq_http_sdk.mq_client import *
from mq_http_sdk.mq_producer import *


topics = {'avs_record_snapshot_HZ_VPC':'screenshot-end'}

class mymq(object):
    def common(self):
        mq_client = MQClient(
            "*",
            "*",
            "*"
        )
        return mq_client

    def sendmq(self, lesuid, topic, tag):
        mqclient = self.common()
        topic_name = topic
        instance_id = ""
        producer = mqclient.get_producer(instance_id, topic_name)
        msg_count = 1
        try:
            for i in range(msg_count):
                msg = TopicMessage(
                    # 消息内容
                    json.dumps({"studentId": [1001774031], "firstChannel": "zego", "duration": 6,
                                "shouldStartTime": 1599464400000,
                                "shouldEndTime": 1599464760000, "lessonUID": lesuid,
                                "expectLessonEndTime": 1599464233322, "delayTime": 0, "businessType": 1,
                                "teacherId ": 7725371, "switchChannel": "agora",
                                "lessonType": "test-lesson", "lessonStartTime": int(round(time.time() * 1000))}),
                    # 消息标签
                    tag
                )
                re_msg = producer.publish_message(msg)
                print("Publish Message Succeed. MessageID:%s, BodyMD5:%s" % (
                    re_msg.message_id, re_msg.message_body_md5))
        except MQExceptionBase as e:
            if e.type == "TopicNotExist":
                print("Topic not exist, please create it.")
                sys.exit(1)
            print("Publish Message Fail. Exception:%s" % e)


for key in topics:
    mymq().sendmq('216ce8524f934c798d0a212bffc4190c', key, topics[key])
