#!/usr/bin/env python
# coding=utf8

import message_media_mq


def submit():
    body = {
        "jobId": "cherryi1140",
        "templateId": "8e749f32-244e-456f-9a16-612561aaa9ab",
        "templateParams": {
            "ak": "LTAI4GFT2TccZm8qqb6xvBzb",
            "sk": "vGd5gKudmBldM2THjVkkPa0E34qy86",
            "in1": "https://zm-chat-lessons.cn-hangzhou.oss.aliyuncs.com/35b7cbe1c7294b3bb8a44b8cd5d3be37/audio.mp4",
            "in2": "https://zm-chat-lessons.cn-hangzhou.oss.aliyuncs.com/35b7cbe1c7294b3bb8a44b8cd5d3be37/audio.mp4",
            "in3": "4a685504c7074b2d8c5e96596ad2391a/audio.mp3",
            "in4": "https://zm-chat-lessons.cn-hangzhou.oss.aliyuncs.com/35b7cbe1c7294b3bb8a44b8cd5d3be37/audio.mp4",
            "in5": "d946abbb2b184bc6aa759afa1abd6da7/audio.mp3",
            "in6": "cherry",
            "in7": "d946abbb2b184bc6aa759afa1abd6da7"
        
        }

    }
    message_media_mq.send('*', 'submit_job', body)


if __name__ == '__main__':
        submit()

