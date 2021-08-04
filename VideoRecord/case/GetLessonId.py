# coding:utf8

import elasticsearch
import json
from elasticsearch import Elasticsearch
import time
import datetime

index_name = 'elk-info-*'
es = Elasticsearch(hosts='10.31.53.185', port='9200', timeout=15000)


# end_Time ='2019-09-04T13:00:00.000Z'
# start_Time ='2019-09-04T11:00:00.000Z'


class GetLessonUid(object):
    def __init__(self):
        pass

    def query(self):
        que = {
        "size":500,
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            'appid': 10708
                        }
                    },
                    {
                        "range": {
                            # "@timestamp": {
                            #     "lte": '2019-09-04T13:00:00.000Z',
                            #     "gte": '2019-09-04T11:00:00.000Z'
                            #
                            # }
                            "@timestamp": {
                                "lte": 'now',
                                "gte": 'now-2h'

                            }
                        }
                    },
                    # {
                    #     "term":
                    #         {
                    #             "message": "agora"
                    #         }
                    # },
                    {
                        "term":
                            {
                                "message": "finish"
                            }
                    },
                    {
                        "match":
                            {
                                "class": "com.zhangmen.avs.record.worker.manager.PostUploadManager"
                            }
                    }
                ]
            }
        }
        }
        return que

# 录制的课程
    def esLessonUid(self, qu, getJesList):
        res = es.search(
            index=index_name,
            body=qu)
        for hit in res['hits']['hits']:
            resJson = json.loads(hit['_source']['message'][7:])
            getJes = resJson['lessonUid']
            getJesList.append(getJes)

 # 上下台的课程
    def es1vnLessonUid(self,qu, getJesList,get1vnLessonUidJesList):
        res = es.search(
            index=index_name,
            body=qu)
        for hit in res['hits']['hits']:
            resJson = json.loads(hit['_source']['message'][7:])
            getJes = resJson['businessType']
            if resJson['onstageMap'] == None or resJson['offstageMap'] == None:
                continue
            if 0 != getJes:
                continue
            print "resjson =%s" % resJson
            get1vnLessonUidJes = resJson['lessonUid']
            get1vnLessonUidJesList.append(get1vnLessonUidJes)











