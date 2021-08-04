#!/usr/bin/env python
# coding=utf8

import time


import message_media_mq
import kafka
import json


def submit():
    topic = "AVS_MEDIA_PROCESS_IN_FAT"
    tag = "submit_job"
    body = {"bu":"bu1v1","jobId":"123456","pipelineId":"abcdef","version":"1.0.0",
    "storage":{"storage1":{"type":"oss","region":0,"bucket":"*","accessKey":"*","secretKey":"*"}},
    "notify":[{"type":"rest_template","url":"http://*/fake/callback"}],
    "input":{"in1":{"type":2,"storage":{"type":"ref","ref":"storage1"},"key":"f00930e3cf8c42cc8dc9182f34ebb7be/audio.mp3"},"in2":{"type":2,"storage":{"type":"ref","ref":"storage1"},"key":"4a685504c7074b2d8c5e96596ad2391a/audio.mp3"},"in3":{"type":2,"storage":{"type":"ref","ref":"storage1"},"key":"d946abbb2b184bc6aa759afa1abd6da7/audio.mp3"}},
    "pipeline":[{"type":"allInput","input":[{"type":0,"ref":"in2"},{"type":0,"ref":"in1"},{"type":0,"ref":"in3"}],"output":[{"name":"output1"},{"name":"output2"},{"name":"output3"}]},{"type":"firstInput","input":[{"type":0,"ref":"output1"}],"output":[{"name":"output11","remote":{"storage":{"type":"ref","ref":"storage1","bucket":"*"},"key":"tmp/abcdef/outpu3.mp3"},"result":True}]},{"type":"firstInput","input":[{"type":0,"ref":"output3"}],"output":[{"name":"output22","remote":{"storage":{"type":"ref","ref":"storage1","bucket":"*"},"key":"tmp/abcdef/outpu4.mp3"},"result":True}]}]}
    
    message_media_mq.sendAmp(topic, tag, body)

def submit_kafka():
    body = {"jobId": "cherry1459",
            "templateId": "8e749f32-244e-456f-9a16-612561aaa9ab",
            "templateParams": {
            "ak": "LTAI4GFT2TccZm8qqb6xvBzb",
            "sk": "vGd5gKudmBldM2THjVkkPa0E34qy86",
            "in1": "https://*/35b7cbe1c7294b3bb8a44b8cd5d3be37/audio.mp4",
            "in2": "f00930e3cf8c42cc8dc9182f34ebb7be/audio.mp3",
            "in3": "4a685504c7074b2d8c5e96596ad2391a/audio.mp3",
            "in4": "https://*/35b7cbe1c7294b3bb8a44b8cd5d3be37/audio.mp4",
            "in5": "d946abbb2b184bc6aa759afa1abd6da7/audio.mp3",
            "in6": "cherry",
            "in7": "d946abbb2b184bc6aa759afa1abd6da7"
        }
            }
    producer = kafka.KafkaProducer(
        bootstrap_servers=['vpc-fat-7.zmaxis.com:9092'],
        # bootstrap_servers = ['172.31.117.188:9092'],
        # bootstrap_servers=['172.21.40.84:9092'],
        value_serializer=lambda v: json.dumps(v).encode())
    future = producer.send(
        'avs-media-process-submit-job-fat',
        # "avs-media-process-submit-job-uat",
        # "avs-media-process-submit-job-pro",
        value=body
    )
    result = future.get(timeout=10)
    print(result)




if __name__ == '__main__' :
    submit_kafka()
