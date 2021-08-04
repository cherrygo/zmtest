from elasticsearch import Elasticsearch

def getBody(startTime, endTime):
    doc = {
        "query": {
            "bool": {
                "must": [
                    {
                        "bool":{
                            "should":[
                                {"match_phrase":{"event_id":"join_room_success"}},
                                {"match_phrase":{"event_id":"local_video"}},
                                {"match_phrase":{"event_id":"local_audio"}},
                                {"match_phrase":{"event_id":"remote_video"}},
                                {"match_phrase":{"event_id":"remote_audio"}},
                                {"match_phrase":{"event_id":"first_video_open_time"}},
                                {"match_phrase":{"event_id":"first_audio_open_time"}}
                            ],
                            "minimum_should_match":1
                        }
                    },
                    {
                        "match_phrase": {
                            "namespace": {"query":"avs"}
                        }
                    },
                    {
                        "range": {
                            '@timestamp': {
                                "gt": "{}".format(startTime),
                                "lt": "{}".format(endTime),
                                "time_zone": "Asia/Shanghai"
                            }
                        }
                    }
                ]
            }
        }
    }
    return doc

fat_server = ['*']
pro_server = ['*','*','*']
es = Elasticsearch(fat_server)
stats = {}
queryData = es.search(index='track_event-*', body=getBody('2020-02-11T03:33:06', '2020-02-11T15:33:06'), size=2000, scroll = '30s')
total_num = queryData.get('hits').get('total')
if isinstance(total_num, dict):
    total_num = total_num.get('value')
current_num = 0
while True:
    hits = queryData.get('hits').get('hits')
    current_num += len(hits)
    for hit in hits:
        source = hit['_source']
        channel_name = source['channel_name']
        c_source = source['c_source']
        sdk_version = source['sdk_version']
        event_id = source['event_id']
        event_value = float(source['event_value'])
        stat = stats.get(event_id)
        if not stat:
            stat = stats[event_id] = {}
        channel_stat = stat.get(channel_name)
        if not channel_stat:
            channel_stat = stat[channel_name] = {}
        pf_stat = channel_stat.get(c_source)
        if not pf_stat:
            pf_stat = channel_stat[c_source] = {}
        version_stat = pf_stat.get(sdk_version)
        if not version_stat:
            version_stat = pf_stat[sdk_version] = [0, 0.0]
        version_stat[0] += 1
        version_stat[1] += event_value
    print('process: %u/%u'% (current_num, total_num))
    sid = queryData['_scroll_id']
    if current_num < total_num:
        queryData = es.scroll(scroll_id=sid, scroll='30s')
    else:
        break
for event_id in stats:
    stat = stats[event_id]
    for channel in stat:
        channel_stat = stat[channel]
        for c_source in channel_stat:
            pf_stat = channel_stat[c_source]
            for version in pf_stat:
                version_stat = pf_stat[version]
                version_stat[1] = version_stat[1] / version_stat[0]
                pf_stat[version] = version_stat[1]
print(total_num, stats)
