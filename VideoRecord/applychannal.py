# #!/usr/bin/env python
# # coding=utf8

import websocket
import thread
import time
import json
from threading import Timer, Event, Thread


class HeartbeatThread(Thread):
    def __init__(self, event, ws):
        super(HeartbeatThread, self).__init__()
        self.event = event
        self.ws = ws

    def run(self):
        while 1:
            # 发送ping包
            self.ws.send('2')
            self.event.wait(timeout=2)

def on_open(ws):
    def run(*args):
        ws.send(json.dumps(['change channel', {"switchChannel": "zego"}]))
        time.sleep(1)

    thread.start_new_thread(run, ())

def on_message(ws, message):
    print(message)

def on_emit(ws):
    # 创建心跳线程
    event = Event()
    heartbeat = HeartbeatThread(event, ws)
    heartbeat.start()
    while 1:
        content = input("input: ")
        # 发送信息
        # 4: engine.io message
        # 2: socket.io event
        # chat message event message
        ws.send('42["change channel","{"switchChannel":"zego"}"]')
        time.sleep(.2)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")


if __name__ == '__main__':
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        'wss://*/socket.io/?lessonUID=f84434fad00c45fea1352645e9ebf09c&mobile=11100001111&userId=1001772883&name=%E8%A3%95%E5%BB%B6%E8%80%81%E5%B8%88&duration=45&roleName=%E8%80%81%E5%B8%88&role=watcher&token=ST-8690dd8c602e49518bd5813daa73c979&clientVersion=kpc-3.3.0&channel=agora%2Czego&userAgent=Mozilla%2F5.0%20(Windows%20NT%206.1%3B%20WOW64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20kids-tch-client%2F3.3.0%20Chrome%2F78.0.3904.130%20Electron%2F7.3.3%20Safari%2F537.36&lessonType=regular-lesson&ability=upStairs%2CbatchGivegood%2CshareScreen&EIO=3&transport=websocket',
        on_error=on_error,
        on_close=on_close)
    ws.on_open = on_open
    t = Timer(3, on_emit, args=(ws,))
    t.start()
    ws.run_forever(ping_interval=60, ping_timeout=5)
