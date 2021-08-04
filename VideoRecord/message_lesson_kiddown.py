import message_record_mq

def sendmq(lessonuid):
    topic = "*"
    body = {"type":"down","userId":1426704877,"time":1611716603875,"lessonUID":lessonuid}
    message_record_mq.send(topic, '', body)

if __name__ == '__main__' :
    sendmq('f6f3b5fb5a6b420c8fffd039b4d64ea3')
