from tkinter import *
import time


class Win():
    def __init__(self):
        self.win = Tk()
        self.width = 500
        self.height = 500
        self.screen_width = self.win.winfo_screenwidth()
        self.screen_height = self.win.winfo_screenheight()
        self.center_x = (self.screen_width-self.width)/2
        self.center_y = (self.screen_height-self.height)/2
        self.win.geometry("%dx%d+%d+%d" %
                          (self.width, self.height, self.center_x, self.center_y))
        self.win.title('测试')
        self.win.iconbitmap('a/favicon.ico')
        self.win.resizable(0, 0)
        self.frame_top = Frame(width=380, height=270, bg='white')
        self.frame_top.grid(row=0, column=0, padx=5, pady=5)
        self.frame_top.grid_propagate(0)
        self.frame_center = Frame(width=380, height=130, bg='white')
        self.frame_center.grid(row=1, column=0, padx=5, pady=5)
        self.frame_center.grid_propagate(0)
        self.frame_right = Frame(width=170, height=400, bg='white')
        self.frame_right.grid(row=0, column=1, rowspan=3, padx=4, pady=5)
        self.frame_right.grid_propagate(0)
        self.frame_bottom = Frame(width=380, height=20)
        self.frame_bottom.grid(row=2, column=0)
        self.frame_bottom.grid_propagate(0)
        self.button_sendmsg = Button(self.frame_bottom, text=('发送'), command=self.send_message)
        self.button_sendmsg.grid(sticky=E)
        self.message = Text(self.frame_top)
        self.message.grid()
        self.input = Text(self.frame_center)
        self.input.grid()

    def send_message(self):
        msgcontent = '我: ' + \
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n'
        self.message.insert(END, msgcontent, 'green')
        self.message.insert(END, self.input.get('0.0', END))
        self.input.delete('0.0', END)



if __name__=="__main__":
    win=Win().win
    win.mainloop()
