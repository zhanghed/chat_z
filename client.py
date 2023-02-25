import socket
import threading
import subprocess
import queue
from tkinter import *
import time
import os
import re


class Win():  # 窗体
    def __init__(self):
        self.win = Tk()
        self.win.title('测试')
        self.win.resizable(0, 0)
        self.c_x = (self.win.winfo_screenwidth()-500)/2  # 位置居中
        self.c_y = (self.win.winfo_screenheight()-500)/2
        self.win.geometry("%dx%d+%d+%d" % (500, 500, self.c_x, self.c_y))
        self.frame_1 = Frame(width=380, height=270, bg='white')  # 消息列表
        self.frame_1.grid(row=0, column=0, padx=5, pady=5)
        self.frame_1.grid_propagate(0)
        self.mes_list = Text(self.frame_1, width=53, height=20,
                             bd=0, padx=5, pady=5, state=DISABLED)
        self.mes_list.grid(row=0, column=0)
        self.frame_2 = Frame(width=380, height=130, bg='white')  # 信息输入框
        self.frame_2.grid(row=1, column=0, padx=5, pady=5)
        self.frame_2.grid_propagate(0)
        self.mes_txt = Text(self.frame_2, width=53,
                            height=9, bd=0, padx=5, pady=5)
        self.mes_txt.grid()
        self.frame_3 = Frame(width=100, height=490, bg='white')  # 好友列表
        self.frame_3.grid(row=0, column=1, rowspan=3, padx=5, pady=5)
        self.frame_3.grid_propagate(0)
        self.friend_list = Text(self.frame_3, width=13,
                                height=37, bd=0, padx=5, pady=5)
        self.friend_list.grid()
        self.frame_11 = Frame(width=380, height=70, bg='white')  # 发送按钮
        self.frame_11.grid(row=2, column=0, padx=5, pady=5)
        self.frame_11.grid_propagate(0)
        self.mes_send = Button(
            self.frame_11, text=('发送'), command=self.fun_send)
        self.mes_send.grid()

    def fun_send(self):  # 发送消息
        t = '自己: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n'
        self.mes_list["state"] = NORMAL
        messages.put({"client":server, "data": self.mes_txt.get('0.0', END)})
        # self.mes_list.insert(END, t)
        # self.mes_list.insert(END, self.mes_txt.get('0.0', END))
        # self.mes_txt.delete('0.0', END)
        self.mes_list["state"] = DISABLED



class Send_thread(threading.Thread):  # 发送线程
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)

    def run(self):
        while True:
            if not messages.empty():
                data = messages.get_nowait()
                if server:
                    server.send(bytes(str(data).encode('utf-8')))


class Recv_thread(threading.Thread):  # 接收线程
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)

    def run(self):
        while True:
            data = server.recv(1024).decode('utf-8')
            if data != '':
                print(data)


def get_server():  # 获取服务
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = os.popen('ipconfig').read()
    ip = re.search(r'以太网:[\d\D]+?IPv4.*?:\s([\d.]*?)\n', s).group(1)
    cmd = subprocess.run(["arp", "-a"], capture_output=True,
                         universal_newlines=True)
    c = str(cmd).split(",")[3].replace(
        "stdout='", "").replace("\\n", "\n").split("接口:")
    for i in c:
        if i.find(str(ip)) > 0:
            ips = re.findall(
                r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', i)
    for i in ips:
        try:
            server.connect((i, 9090))
            print(server)
            return server
        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":  # 主线程
    messages = queue.Queue()
    server = get_server()
    Send_thread("Send_thread").start()
    Recv_thread("Recv_thread").start()
    win = Win().win
    win.mainloop()
