#!/usr/bin/python
# coding=utf8

import threading
from mq_http_sdk.mq_client import *
from mq_http_sdk.mq_producer import *
import time

num = 0
threads = []


class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def common(self):
        # 初始化 client
        mq_client = MQClient(
            "*",
            "*",
            "*"
        )
        return mq_client

    def sendmq(self, lesuid):
        mqclient = self.common()
        # topic_name = "*"
        topic_name = "*"
        instance_id = ""
        producer = mqclient.get_producer(instance_id, topic_name)
        msg_count = 1
        try:
            for i in range(msg_count):
                msg = TopicMessage(
                    # 消息内容
                    json.dumps({"studentId": [1326368550], "firstChannel": "agora", "duration": 6,
                                "shouldStartTime": 1599464400000,
                                "shouldEndTime": 1599464760000, "lessonUID": lesuid,
                                "expectLessonEndTime": 1599464233322, "delayTime": 0, "businessType": 1,
                                "teacherId ": 173,
                                "lessonType": "test-lesson", "lessonStartTime": int(round(time.time()*1000))}),
                    # 消息标签
                    # "lesson-start"
                    "drill-start"
                )
                re_msg = producer.publish_message(msg)
                print("Publish Message Succeed. MessageID:%s, BodyMD5:%s" % (
                    re_msg.message_id, re_msg.message_body_md5))
                time.sleep(30)
                msg = TopicMessage(
                    # 消息内容
                    json.dumps(
                        {"businessType": 1, "delayTime": 32942, "duration": 40, "expectLessonEndTime": 1599642599984,
                         "firstChannel": "agora", "lessonEndTime": int(round(time.time()*1000)), "lessonStartTime": 1599640232926,
                         "lessonType": "regular-lesson", "lessonUID": lesuid,
                         "newLesson": 'true',
                         "shouldEndTime": 1599642600000, "shouldStartTime": 1599640200000, "studentId": [21368631],
                         "teacherId": 656413, "version": 1}),
                    # 消息标签
                    # "lesson-end"
                    "drill-end"
                )
                re_msg = producer.publish_message(msg)
                print("Publish Message Succeed. MessageID:%s, BodyMD5:%s" % (
                    re_msg.message_id, re_msg.message_body_md5))
        except MQExceptionBase as e:
            if e.type == "TopicNotExist":
                print("Topic not exist, please create it.")
                sys.exit(1)
            print("Publish Message Fail. Exception:%s" % e)

    def setlessonuid(self, scens):
        rnum = str(self.threadID)
        time_now = time.strftime("%H%M%S")
        final_now = rnum + 'wang' + time_now + scens
        return final_now


    def run(self):
        print "Starting " + self.name
        newlesuid = self.setlessonuid('agoracloud')
        print 'lesuid-----%s' % newlesuid
        self.sendmq(newlesuid)


#创建新线程
for i in range(1,3, 1):
    thread = myThread(i, "thread" + str(i))
    thread.start()
    threads.append(thread)

# 等待所有线程完成
for t in threads:
    t.join()
print "Exiting Main Thread"

