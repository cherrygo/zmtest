# coding:utf8

import elasticsearch
import json
from elasticsearch import Elasticsearch
import time
import datetime
import pandas as pd
import csv

index_name = 'track_event-*'
es = Elasticsearch(hosts='*', port='*', timeout=15000)

join_room_success = [0,0]
local_audio = [0,0]
local_video = [0,0]
remote_video = [0,0]
remote_audio = [0,0]
first_video_open_time = [0,0]
first_audio_open_time = [0,0]
remote_video_frozen = [0,0]

class GetEsResource(object):
    def __init__(self):
        pass

    def query(self):
       que= {
           "size":5000,
           "query":{"bool":{"must":[{"query_string":{"query":"event_id:join_room_success and event_id:local_audio and event_id:local_video and event_id:remote_video and event_id:remote_audio and event_id:first_video_open_time and event_id:first_audio_open_time","analyze_wildcard":"true","default_field":"*"}},{"match_phrase":{"namespace":{"query":"avs"}}},{"match_phrase":{"lesson_uid":{"query":"0c5816d8c06a415bbb267f0dfe4b49c5"}}},{"match_phrase":{"channel_name":{"query":"agora"}}},{"match_phrase":{"c_source":{"query":"pc"}}},{"range":{"server_time":{"gte":1578946563271,"lte":1578989763271,"format":"epoch_millis"}}}]
                              }}}

       return que


# 埋点结果数据
    def essdkRes(self, qu):
        res = es.search(
            index=index_name,
            body=qu)
        print "hit-----------" , res['hits']['hits']
        for hit in res['hits']['hits']:
            joinRoomList = hit['_source']['event_id']
            if joinRoomList == "join_room_success":
                joinRoomSuc = hit['_source']['event_value']
                join_room_success[0] += 1
                join_room_success[1] += int(joinRoomSuc)
            if joinRoomList == "local_audio":
                localAudio = hit['_source']['event_value']
                local_audio[0] += 1
                local_audio[1] += int(localAudio)
            if joinRoomList == "local_video":
                localVideo = hit['_source']['event_value']
                local_video[0] += 1
                local_video[1] += int(localVideo)
            if joinRoomList == "remote_video":
                remoteVideo = hit['_source']['event_value']
                remote_video[0] += 1
                remote_video[1] += int(remoteVideo)
            if joinRoomList == "remote_audio":
                remoteAudio = hit['_source']['event_value']
                remote_audio[0] += 1
                remote_audio[1] += int(remoteAudio)
            if joinRoomList == "first_video_open_time":
                firstVideoOpenTime = hit['_source']['event_value']
                first_video_open_time[0] += 1
                first_video_open_time[1] += int(firstVideoOpenTime)
            if joinRoomList == "first_audio_open_time":
                firstAudioOpenTime = hit['_source']['event_value']
                first_audio_open_time[0] += 1
                first_audio_open_time[1] += int(firstAudioOpenTime)
        if first_video_open_time[1] != 0:
           first_video_open_time[1] = int(first_video_open_time[1]) / first_video_open_time[0]
        else:
            first_video_open_time ==[0,0]
        if first_audio_open_time[1] !=0:
           first_audio_open_time[1] = int(first_audio_open_time[1]) / first_audio_open_time[0]
        else:
            first_audio_open_time ==[0,0]
        if remote_audio[1] != 0:
            remote_audio[1] = int(remote_audio[1]) / remote_audio[0]
        else:
            remote_audio ==[0,0]
        if remote_video[1] !=0:
           remote_video[1] = int(remote_video[1]) / remote_video[0]
        else:
            remote_video ==[0,0]
        if local_video[1] != 0:
           local_video[1] = int(local_video[1]) / local_video[0]
        else:
           local_video == [0,0]
        if local_audio[1] != 0:
           local_audio[1] = int(local_audio[1]) / local_audio[0]
        else:
           local_video == [0,0]
        if join_room_success[1] !=0:
           join_room_success[1] = int(join_room_success[1]) /join_room_success[0]
        else:
            join_room_success[0,0]
        print "first_video_open_time:", first_video_open_time
        print "first_audio_open_time:", first_audio_open_time
        print "remote_audio:", remote_audio
        print "remote_video:", remote_video
        print "local_video:", local_video
        print "local_audio:", local_audio
        print "join_room_success:", join_room_success

        # dataframe = pd.DataFrame({'join_room_success': join_room_success, 'local_audio': local_audio,'local_video':local_video})
        # dataframe.to_csv(r"E:\testwwwww.csv", index=False, sep=',')

        # header = ['join_room_success', 'local_audio','local_video']
        # csvfile = open('E:/test.csv', 'wt')
        # writer = csv.writer(csvfile, delimiter=',')
        # writer.writerow(header)
        # csvfile.write('\n'.join(join_room_success)+'\n')
        # csvfile.write('\n'.join(local_audio)+'\n')
        # csvfile.write('\n'.join(local_video))

parme = GetEsResource().query()
re =  GetEsResource().essdkRes(parme)









