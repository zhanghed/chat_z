from tkinter import *
import time


class Win(object):
    def __init__(self):
        self.win = Tk()
        self.win.title('测试')
        self.win.iconbitmap('favicon.ico')
        self.win.resizable(0, 0)

        # 位置居中
        self.c_x = (self.win.winfo_screenwidth()-500)/2
        self.c_y = (self.win.winfo_screenheight()-500)/2
        self.win.geometry("%dx%d+%d+%d" % (500, 500, self.c_x, self.c_y))

        # 消息列表
        self.frame_1 = Frame(width=380, height=270, bg='white')
        self.frame_1.grid(row=0, column=0, padx=5, pady=5)
        self.frame_1.grid_propagate(0)
        self.mes_list = Text(self.frame_1, width=53, height=20,
                             bd=0, padx=5, pady=5, state=DISABLED)
        self.mes_list.grid(row=0, column=0)

        # 信息输入框
        self.frame_2 = Frame(width=380, height=130, bg='white')
        self.frame_2.grid(row=1, column=0, padx=5, pady=5)
        self.frame_2.grid_propagate(0)
        self.mes_txt = Text(self.frame_2, width=53,
                            height=9, bd=0, padx=5, pady=5)
        self.mes_txt.grid()

        # 好友列表
        self.frame_3 = Frame(width=100, height=490, bg='white')
        self.frame_3.grid(row=0, column=1, rowspan=3, padx=5, pady=5)
        self.frame_3.grid_propagate(0)
        self.friend_list = Text(self.frame_3, width=13,
                                height=37, bd=0, padx=5, pady=5)
        self.friend_list.grid()

        # 发送按钮
        self.frame_11 = Frame(width=380, height=70, bg='white')
        self.frame_11.grid(row=2, column=0, padx=5, pady=5)
        self.frame_11.grid_propagate(0)
        self.mes_send = Button(
            self.frame_11, text=('发送'), command=self.fun_send)
        self.mes_send.grid()

    def fun_send(self):
        # 发送消息
        t = '我: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n'
        self.mes_list["state"] = NORMAL
        self.mes_list.insert(END, t)
        self.mes_list.insert(END, self.mes_txt.get('0.0', END))
        self.mes_txt.delete('0.0', END)
        self.mes_list["state"] = DISABLED


if __name__ == "__main__":

    win = Win().win
    win.mainloop()
