#!/usr/bin/env python
# coding=utf8

from mq_http_sdk.mq_exception import MQExceptionBase
from mq_http_sdk.mq_consumer import *
from mq_http_sdk.mq_client import *

def _consume():
    mq_client = MQClient(
        "*",
        "*",
        "*"
    )
    topic_name = "AVS_MEDIA_PROCESS_OUT_FAT"
    group_id = "GID_AVS_MEDIA_PROCESS_FAT"
    consumer = mq_client.get_consumer("", topic_name, group_id)
    wait_seconds = 1
    # 一次最多消费3条(最多可设置为16条)
    batch = 1
    print(("%sConsume And Ak Message From Topic%s\nTopicName:%s\nMQConsumer:%s\nWaitSeconds:%s\n" \
           % (10 * "=", 10 * "=", topic_name, group_id, wait_seconds)))
    while True:
        try:
            # 长轮询消费消息
            recv_msgs = consumer.consume_message(batch, wait_seconds)
            for msg in recv_msgs:
                print(("Receive, MessageId: %s\nMessageBodyMD5: %s \
                                  \nMessageTag: %s\nConsumedTimes: %s \
                                  \nPublishTime: %s\nBody: %s \
                                  \nNextConsumeTime: %s \
                                  \nReceiptHandle: %s \
                                  \nProperties: %s\n" % \
                       (msg.message_id, msg.message_body_md5,
                        msg.message_tag, msg.consumed_times,
                        msg.publish_time, msg.message_body,
                        msg.next_consume_time, msg.receipt_handle, msg.properties)))
                print(msg.get_property("哈哈哈"))
        except MQExceptionBase as e:
            if e.type == "MessageNotExist":
                print(("No new message! RequestId: %s" % e.req_id))
                continue

            print(("Consume Message Fail! Exception:%s\n" % e))
            time.sleep(2)
            continue

        # msg.next_consume_time前若不确认消息消费成功，则消息会重复消费
        # 消息句柄有时间戳，同一条消息每次消费拿到的都不一样
        try:
            receipt_handle_list = [msg.receipt_handle for msg in recv_msgs]
            consumer.ack_message(receipt_handle_list)
            print(("Ak %s Message Succeed.\n\n" % len(receipt_handle_list)))
        except MQExceptionBase as e:
            print(("\nAk Message Fail! Exception:%s" % e))
            # 某些消息的句柄可能超时了会导致确认不成功
            if e.sub_errors:
                for sub_error in e.sub_errors:
                    print(("\tErrorHandle:%s,ErrorCode:%s,ErrorMsg:%s" % \
                           (sub_error["ReceiptHandle"], sub_error["ErrorCode"], sub_error["ErrorMessage"])))


if __name__ == '__main__':
    _consume()