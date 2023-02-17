from tkinter import *


root = Tk()
root.title('测试')
root.geometry('500x500')
root.config(background="#6fb765")
root.iconbitmap('b/favicon.ico')
root.resizable(0,0)
screen_width = (root.winfo_screenwidth()-500)/2
screen_height = (root.winfo_screenheight()-1.2*500)/2
gm_str = "%dx%d+%d+%d" % (500, 500, screen_width, screen_height)
root.geometry(gm_str)


root.mainloop()
