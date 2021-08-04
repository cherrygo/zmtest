# -*- encoding:UTF-8 -*-
import wx
import sys
import string
import psutil
import signal
import chardet
import shutil, os

reload(sys)
sys.setdefaultencoding('gbk')


# app = wx.App()
# win = wx.Frame(None,title = "zm操作", size=(410,335))
# win.Show()
# loadButton = wx.Button(win, label = '强杀客户端',pos = (75,30),size = (80,25))
# saveButton = wx.Button(win, label = '清除日志',pos = (200,30),size = (80,25))
# app.MainLoop()
class InsertFrame(wx.Frame):

    def __init__(self, parent, id):

        wx.Frame.__init__(self, parent, id, 'Frame with button', size=(500, 300))
        panel = wx.Panel(self)
        button2 = wx.Button(panel, label="关闭客户端进程", pos=(100, 10), size=(100, 50))
        button = wx.Button(panel, label="清除日志", pos=(200, 10), size=(100, 50))
        self.Bind(wx.EVT_BUTTON, self.goKill, button2)
        self.Bind(wx.EVT_BUTTON, self.del_file, button)

    # 杀进程
    def getAllPid(self):
        pid_dict = {}
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            pid_dict[pid] = p.name()
            # print pid_dict
        return pid_dict

    def kill(self, pid):
        try:
            kill_pid = os.kill(pid, signal.SIGABRT)
            print u'已杀死pid为%s的进程' % pid
            # print u'已杀死pidName为%s的进程,　返回值是:%s' % (pidName, kill_pid)
        except Exception as e:
            print u'没有如此进程!!!'

    def goKill(self, event):
        dic = self.getAllPid()
        for t in dic.keys():
            if dic[t].decode("GB2312") == u"掌门1对1辅导.exe":
                self.kill(t)
            if dic[t] == u"DeviceTest.exe":
                self.kill(t)

    CUR_PATH = r'C:\Users\Administrator\AppData\Roaming\ZMLearnData'

    def del_file(self, event):
        ls = os.listdir(self.CUR_PATH)
        for i in ls:
            c_path = os.path.join(self.CUR_PATH, i)
            print c_path;
            if os.path.isdir(c_path):
                self.del_file_fun(c_path)
            else:
                os.remove(c_path)

    def del_file_fun(self, path):
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                self.del_file(c_path)
            else:
                os.remove(c_path)


if __name__ == '__main__':
    app = wx.App()
    frame = InsertFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
