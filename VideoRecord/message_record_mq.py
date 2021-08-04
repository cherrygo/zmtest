#!/usr/bin/env python
# coding=utf8

from mq_http_sdk.mq_client import *
from mq_http_sdk.mq_producer import *


accounts = {
    'fat': {
        '11159': {'ak': '*', 'sk': '*'},
        '12723': {'ak': '*', 'sk': '*'}
    },
    'uat': {
        '12723': {'ak': '*', 'sk': '*'}
    },
    'pro': {
        '12723': {'ak': '*', 'sk': '*'}
    }
}


def _send(ak, sec, topic, tag, body, env='fat'):
    endpoint = "*"
    if 'uat' == env:
        endpoint = "*"
    # 初始化 client
    mq_client = MQClient(
        # 设置HTTP接入域名（此处以公共云生产环境为例）
        endpoint,
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


def send_mkl(topic, tag, body):
    _send("*", "*", topic, tag, body)


def send(topic, tag, body):
    _send("*", "*", topic, tag, body)
    


def sendToApp(appId, topic, tag, body, env):
    account = accounts[env][appId]
    _send(account['ak'], account['sk'], topic, tag, body, env=env)

