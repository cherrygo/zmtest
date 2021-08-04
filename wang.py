# coding:utf8
from tkinter import *
from tkinter import ttk

# Create an instance
win = Tk()
win.title("zmg tool")
win.geometry('400x400')
# create a Label
lb1 = Label(win, text="env", font="tahoma 12 normal")
lb1.grid(column=0, row=0, padx=8, pady=4)

def show_select_1():
    print("post_command: show_select")
    print(value.get())

# Define tkinter data type
data = ["fat", "uat"]
value = StringVar()
# Create a combobox, and tighter it to value
cbx_1 = ttk.Combobox(win, width=12, height=8, textvariable=value, postcommand=show_select_1)
cbx_1.grid(column=1, row=0)
# add data to combobox
cbx_1["values"] = data


Label1 = Label(win, text='courseId',font="tahoma 12 normal").grid(row=1, column=0)
v1 = StringVar()
e1 = Entry(win, textvariable=v1)  # Entry 是 Tkinter 用来接收字符串等输入的控件.
e1.grid(row=1, column=1, padx=10, pady=5)  # 设置输入框显示的位置，以及长和宽属性

def show():
    print("courseId:%s" % e1.get())  # 获取用户输入的信息

Button(win, text='start', width=10, command=show) \
    .grid(row=2, column=4, sticky=W, padx=10, pady=5)

win.mainloop()
