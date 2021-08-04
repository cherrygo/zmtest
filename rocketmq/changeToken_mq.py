#!/usr/bin/python
# coding=utf8

import threading
from mq_http_sdk.mq_client import *
from mq_http_sdk.mq_producer import *
import time

#uat
class changeTokenMQ(object):
    def common(self):
        # 初始化 client
        mq_client = MQClient(
            "*",
            "*",
            "*"
        )
        return mq_client

    def sendmq(self):
        mqclient = self.common()
        topic_name = "*"
        instance_id = ""
        producer = mqclient.get_producer(instance_id, topic_name)
        msg_count = 1
        try:
            for i in range(msg_count):
                msg = TopicMessage(
                    # 消息内容
                    json.dumps({"appCode": "kid", "bizType": "1vn", "channel": "agora",
                                "lessonUid": "5ba4890cbf124c15a4cbf637577154d0", "time": 1604991594422,
                                "useToken": True}),
                    # 消息标签
                    # "lesson-start"
                )
                re_msg = producer.publish_message(msg)
                print("Publish Message Succeed. MessageID:%s, BodyMD5:%s" % (
                    re_msg.message_id, re_msg.message_body_md5))
        except MQExceptionBase as e:
            if e.type == "TopicNotExist":
                print("Topic not exist, please create it.")
                sys.exit(1)
            print("Publish Message Fail. Exception:%s" % e)


changeTokenMQ().sendmq()
