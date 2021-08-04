# -*- encoding:UTF-8 -*-

import os
import sys
import string
import psutil
import signal
import chardet
import shutil,os

#蒋utf8解码为gbk格式
reload(sys)
sys.setdefaultencoding('gbk')


#杀进程
# print os.getpid()
def getAllPid():
    pid_dict = {}
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        pid_dict[pid] =p.name()
        # print("pid-%d,pname-%s" %(pid,p.name()))
    return pid_dict


def kill(pid):
    try:
        kill_pid = os.kill(pid, signal.SIGABRT)
        print u'已杀死pid为%s的进程' %pid
        # print u'已杀死pidName为%s的进程,　返回值是:%s' % (pidName, kill_pid)
    except Exception as e:
        print u'没有如此进程!!!'




if __name__ == '__main__':
    dic = getAllPid()
    for t in dic.keys():
        if dic[t].decode("GB2312") == u"掌门1对1辅导.exe":
            kill(t)
        if dic[t] == u"DeviceTest.exe":
            kill(t)





