#!/usr/bin/env python
# coding=utf8
import json

import msgpack as msgpack
from kafka import KafkaConsumer
import kafka
from pykafka import KafkaClient


def submit_consume():
    consumer = KafkaConsumer('*',
                             bootstrap_servers=['*'])

    print(type(consumer))
    for message in consumer:
        print("%s:%d:%d: key=%s value=%s" % (
            message.topic, message.partition,
            message.offset, message.key, message.value
        ))

    # client = KafkaClient(hosts="vpc-fat-7.zmaxis.com:9092")
    # print(client.topics)
    # topic = client.topics['avs-media-process-notify-fat']
    # consumer = topic.get_balanced_consumer('MY_GROUP1', auto_commit_enable=True, auto_commit_interval_ms=3000)
    # print("dsadddssdsdsd"+type(consumer))
    # for message in consumer:
    #     if message is not None:
    #         print(message.offset, message.value)

if __name__ == '__main__' :
    submit_consume()