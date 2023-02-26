import socket
import threading
import subprocess
from tkinter import *
import os
import re


class Win():  # 窗体
    def __init__(self):
        # 界面
        win = self.fun_win()
        self.win = win[0]
        self.mes_list = win[1]
        self.mes_txt = win[2]
        self.friend_list = win[3]
        # 服务
        self.get_server()
        # 接收线程
        threading.Thread(target=self.recv_thread).start()

    def fun_win(self):  # 界面
        win = Tk()
        win.title('Tkker')
        win.resizable(0, 0)
        # 位置居中
        c_x = (win.winfo_screenwidth()-500)/2
        c_y = (win.winfo_screenheight()-500)/2
        win.geometry("%dx%d+%d+%d" % (500, 500, c_x, c_y))
        # 消息列表
        frame_1 = Frame(width=380, height=270, bg='white')
        frame_1.grid(row=0, column=0, padx=5, pady=5)
        frame_1.grid_propagate(0)
        mes_list = Text(frame_1, width=53, height=20,
                        bd=0, padx=5, pady=5, state=DISABLED)
        mes_list.grid(row=0, column=0)
        # 信息输入框
        frame_2 = Frame(width=380, height=130, bg='white')
        frame_2.grid(row=1, column=0, padx=5, pady=5)
        frame_2.grid_propagate(0)
        mes_txt = Text(frame_2, width=53,
                       height=9, bd=0, padx=5, pady=5)
        mes_txt.grid()
        # 好友列表
        frame_3 = Frame(width=100, height=490, bg='white')
        frame_3.grid(row=0, column=1, rowspan=3, padx=5, pady=5)
        frame_3.grid_propagate(0)
        friend_list = Text(frame_3, width=13,
                           height=37, bd=0, padx=5, pady=5)
        friend_list.grid()
        # 发送按钮
        frame_11 = Frame(width=380, height=70, bg='white')
        frame_11.grid(row=2, column=0, padx=5, pady=5)
        frame_11.grid_propagate(0)
        mes_send = Button(frame_11, text=('发送'), command=self.fun_send)
        mes_send.grid()
        return (win, mes_list, mes_txt, friend_list)

    def fun_send(self):  # 发送消息
        self.mes_list["state"] = NORMAL
        data = self.mes_txt.get('0.0', END)
        if self.server:
            self.server.send(str(data).encode('utf-8'))
        self.mes_txt.delete('0.0', END)
        self.mes_list["state"] = DISABLED

    def recv_thread(self):  # 接收线程
        while True:
            data = self.server.recv(1024).decode('utf-8')
            data = eval(data)
            if self.ip == data["addr"][0]:
                addr = "自己"
            else:
                addr = data["addr"][0]
            self.mes_list["state"] = NORMAL
            self.mes_list.insert(END, addr+":"+"\n")
            self.mes_list.insert(END, data["data"])
            self.mes_list["state"] = DISABLED

    def get_server(self):  # 获取服务
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = os.popen('ipconfig').read()
        self.ip = re.search(r'以太网:[\d\D]+?IPv4.*?:\s([\d.]*?)\n', s).group(1)
        cmd = subprocess.run(["arp", "-a"], capture_output=True,
                             universal_newlines=True)
        c = str(cmd).split(",")[3].replace(
            "stdout='", "").replace("\\n", "\n").split("接口:")
        for i in c:
            if i.find(str(self.ip)) > 0:
                ips = re.findall(
                    r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', i)
        for i in ips:
            try:
                self.server.connect((i, 9090))
                print(self.server)
                break
            except Exception as e:
                print(e)
                continue


if __name__ == "__main__":  # 主线程
    win = Win().win
    win.mainloop()
