#!/usr/bin/env python
# coding=utf8

from mq_http_sdk.mq_client import *
from mq_http_sdk.mq_producer import *


def _send(ak, sec, topic, tag, body):
    # 初始化 client
    mq_client = MQClient(
        # 设置HTTP接入域名（此处以公共云生产环境为例）
        "*",
         ak, sec
    )

    producer = mq_client.get_producer("", topic)
    print("%sPublish Message To %s\nTopicName:%s\n" % (10 * "=", 10 * "=", topic))
    try:
        msg = TopicMessage(
            # 消息内容
            json.dumps(body),
            # 消息标签
            tag
        )
        re_msg = producer.publish_message(msg)
        print("Publish Message Succeed. MessageID:%s, BodyMD5:%s" % (re_msg.message_id, re_msg.message_body_md5))
    except MQExceptionBase as e:
        if e.type == "TopicNotExist":
            print("Topic not exist, please create it.")
            sys.exit(1)
        print("Publish Message Fail. Exception:%s" % e)


def send(topic, tag, body):
    _send("*", "*", topic, tag, body)
    

