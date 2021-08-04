#!/usr/bin/env python
# coding=utf8

from mq_http_sdk.mq_client import *
from mq_http_sdk.mq_producer import *


class mymq(object):
    def common(self):
        # 初始化 client
        mq_client = MQClient(
            # 设置HTTP接入域名（此处以公共云生产环境为例）
            "*",
            # AccessKey 阿里云身份验证，在阿里云服务器管理控制台创建
            "*",
            # SecretKey 阿里云身份验证，在阿里云服务器管理控制台创建
            "*"
        )
        return mq_client

    def sendmq(self, lesuid):
        mqclient = self.common()
        # 所属的 Topic
        topic_name = "*"
        # Topic所属实例ID，默认实例为空None
        instance_id = ""
        producer = mqclient.get_producer(instance_id, topic_name)
        # 循环发布多条消息
        msg_count = 1
        try:
            for i in range(msg_count):
                msg = TopicMessage(
                    # 消息内容
                    json.dumps(
                        {"businessType": 2, "delayTime": 32942, "duration": 40, "expectLessonEndTime": 1599642599984,
                         "firstChannel": "tencent2", "lessonEndTime": int(round(time.time() * 1000)),
                         "lessonStartTime": 1599640232926,
                         "lessonType": "regular-lesson", "lessonUID": lesuid,
                         "newLesson": 'true',
                         "shouldEndTime": 1599642600000, "shouldStartTime": 1599640200000, "studentId": [1001774031],
                         "teacherId": 7725371, "version": 1}),
                    # 消息标签
                    "lesson-end"
                )
                re_msg = producer.publish_message(msg)
                print("Publish Message Succeed. MessageID:%s, BodyMD5:%s" % (
                    re_msg.message_id, re_msg.message_body_md5))
        except MQExceptionBase as e:
            if e.type == "TopicNotExist":
                print("Topic not exist, please create it.")
                sys.exit(1)
            print("Publish Message Fail. Exception:%s" % e)


mymq().sendmq('761a4396399642c2b8f7b3e2ea7c3c5b')
