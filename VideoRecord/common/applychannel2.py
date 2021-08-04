# #!/usr/bin/env python
# # coding=utf8
import socketio

class HeartbeatThread(object):
    def create_client(self):
        sio = socketio.Client()
        @sio.event
        def connect():
            print('connection established')
            sio.connect(
                'wss://10-111-238-190.zmlearn.com:1338/socket.io/?lessonUID=f84434fad00c45fea1352645e9ebf09c&mobile=11100001111&userId=1001772883&name=%E8%A3%95%E5%BB%B6%E8%80%81%E5%B8%88&duration=45&roleName=%E8%80%81%E5%B8%88&role=watcher&token=ST-8690dd8c602e49518bd5813daa73c979&clientVersion=kpc-3.3.0&channel=agora%2Czego&userAgent=Mozilla%2F5.0%20(Windows%20NT%206.1%3B%20WOW64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20kids-tch-client%2F3.3.0%20Chrome%2F78.0.3904.130%20Electron%2F7.3.3%20Safari%2F537.36&lessonType=regular-lesson&ability=upStairs%2CbatchGivegood%2CshareScreen&EIO=3&transport=websocket')
            print('my sid is', sio.sid)
            sio.wait(3)
            sio.emit('change channel', {"switchChannel": "zego"})

        @sio.on('serve')
        def on_message(data):
            print('client received a message!', data)

        @sio.event
        def my_event(sid, data):
            # handle the message
            return "OK", 123

        @sio.event
        def connect_error():
            print("The connection failed!")
            sio.disconnect()

        @sio.event
        def disconnect():
            print('disconnected from server')
            sio.disconnect()

        sio.connect(
            'wss://10-111-238-190.zmlearn.com:1338/socket.io/?lessonUID=f84434fad00c45fea1352645e9ebf09c&mobile=11100001111&userId=1001772883&name=%E8%A3%95%E5%BB%B6%E8%80%81%E5%B8%88&duration=45&roleName=%E8%80%81%E5%B8%88&role=watcher&token=ST-8690dd8c602e49518bd5813daa73c979&clientVersion=kpc-3.3.0&channel=agora%2Czego&userAgent=Mozilla%2F5.0%20(Windows%20NT%206.1%3B%20WOW64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20kids-tch-client%2F3.3.0%20Chrome%2F78.0.3904.130%20Electron%2F7.3.3%20Safari%2F537.36&lessonType=regular-lesson&ability=upStairs%2CbatchGivegood%2CshareScreen&EIO=3&transport=websocket'),
        # sio.wait(3)

HeartbeatThread().create_client()
