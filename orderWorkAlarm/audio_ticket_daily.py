#!/usr/bin/python3
 
#-------------------------------------------------------------------------------
# Name: audio_ticket_daily
# Author: lu.xie
# Created: 4/13/2019
#-------------------------------------------------------------------------------

import pymysql
import time
import sys
import json
import urllib.request
from collections import OrderedDict
from decimal import Decimal
import datetime

## 定义一个字段，将keywords写到字典里
def read_keywords_into_dict():
    dict = {}
    fr = open('keywords.txt', 'r') 
    for line in fr.readlines():
        line = line.strip() 
        dict[line] = [0,0,Decimal(0)]
    fr.close()
    return dict

## 合并看不到+看不见，合并听不到+听不见，并排序
def merge_keys(dict):
    dict["看不到+看不见"] = [dict["看不到"][0]+dict["看不见"][0], dict["看不到"][1],dict["看不到"][2]+dict["看不见"][2]]
    dict["听不到+听不见"] = [dict["听不到"][0]+dict["听不见"][0], dict["听不到"][1],dict["听不到"][2]+dict["听不见"][2]]
    dict.pop("看不到")
    dict.pop("看不见")
    dict.pop("听不到")
    dict.pop("听不见")
    sort = sorted(dict.items(), key = lambda item:item[1][2], reverse = True)
    return sort

## 这是根据字段和时间获取工单占比
def get_tickets_count_by_keyword(keyword,time):
    data = (0,0,0.0)
    sql_cmd = 'SELECT t1.cant_hear_tickets,t2.total_tickets,round(t1.cant_hear_tickets/t2.total_tickets * 100, 2) FROM (SELECT count(DISTINCT ticket_id) AS cant_hear_tickets FROM audio_tickets_detail WHERE updatetime BETWEEN \'' + time + '\' AND \'' + time + ' 23:59:59\' AND message_page LIKE concat(\'%\',\'' + keyword +'\',\'%\')) t1, (SELECT count(DISTINCT ticket_id) AS total_tickets FROM audio_tickets_detail WHERE updatetime BETWEEN \'' + time + '\' AND \'' + time + ' 23:59:59\')t2'
    try:
        db = pymysql.connect("test.db.zmaxis.com","forge","Zhangmen1dui1","forge")
        cursor = db.cursor()
        cursor.execute(sql_cmd)
        data = cursor.fetchone()
        cursor.close()
        db.close()
    except:
        print ("Error: unable to fetch data") 
    finally:
        return data

## 获取当前日期
def get_datetime():
    date = time.strftime("%Y-%m-%d", time.localtime())
    return date

## 发消息给钉钉机器人
def report_to_robot(file_name):
    ## 这是工单分类群的机器人
    robot_url = "https://*/robot/send?access_token=4f4951df8e18e78774aec052010cb4cab5410d4057280514049e45eb7c952409"
    ## 这是音视频测试组的机器人 
    #robot_url = "https://*/robot/send?access_token=f7470228af6da790c7880bf4c757791deeb45b209795d560f64131def1f78c1a"
    headers = {'Content-type': 'application/json'}
    
    with open(file_name, 'r') as fr:
        temp = fr.read().strip()

    today = datetime.date.today()
    yesterday = str(today - datetime.timedelta(days=1))
    temp = "Hello! 这是" + yesterday + "的日报！\n"+temp
    data = {"msgtype":"text", "text": {"content": temp}}  
    data = json.dumps(data)   
    data = bytes(data, encoding = "utf-8")
    request = urllib.request.Request(robot_url, headers=headers, data=data) 
    response = urllib.request.urlopen(request) 

## 读取关键字文件并生成日报
def main():
    file_name = get_datetime() + ".txt"
    fw = open(file_name, 'a')
    dict = read_keywords_into_dict()
    total = 0
    for key in dict:
        result = get_tickets_count_by_keyword(key,get_datetime())
        dict[key] = [result[0],result[1],result[2]]
        total = result[1]
    sort = merge_keys(dict)
    fw.write("工单总数: " + str(total) + "\n")
    for item in sort:
        fw.write(item[0] + ": " + str(item[1][0]) + " 占比: " + str(item[1][2])+"%\n")
        
    fw.close()
    report_to_robot(file_name)
    
if __name__ == "__main__":
    sys.exit(main())

