from tkinter import *
from tkinter.font import Font
from tkinter.ttk import *

from setting import ico


class Application_ui(Frame):
    # 这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master)
        super().__init__(master, **kw)
        self.master.iconbitmap(ico)
        self.master.title('收藏文件夹')
        screenwidth = self.master.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.master.winfo_screenheight()  # 屏幕高度
        width = 532
        height = 427
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.Text1 = Entry(self.top, textvariable=StringVar(value=''), font=('宋体', 10))
        self.Text1.place(relx=0.135, rely=0.037, relwidth=0.648, relheight=0.096)

        self.style.configure('Label1.TLabel', anchor='w', font=('宋体', 10))
        self.Label1 = Label(self.top, text='添加备注', style='Label1.TLabel')
        self.Label1.place(relx=0.015, rely=0.056, relwidth=0.107, relheight=0.059)

        self.List1 = Listbox(self.top, listvariable=StringVar(value=''), font=Font(font=('宋体', 9)))
        self.List1.place(relx=0., rely=0.15, relwidth=0.784, relheight=0.824)

        self.style.configure('Command1.TButton', font=('宋体', 9))
        self.Command1 = Button(self.top, text='添加', command=self.Command1_Cmd, style='Command1.TButton')
        self.Command1.place(relx=0.812, rely=0.037, relwidth=0.167, relheight=0.096)

        self.style.configure('Command2.TButton', font=('宋体', 9))
        self.Command2 = Button(self.top, text='删除', command=self.Command2_Cmd, style='Command2.TButton')
        self.Command2.place(relx=0.812, rely=0.225, relwidth=0.167, relheight=0.096)

        self.style.configure('Command3.TButton', font=('宋体', 9))
        self.Command3 = Button(self.top, text='刷新', command=self.Command3_Cmd, style='Command3.TButton')
        self.Command3.place(relx=0.812, rely=0.431, relwidth=0.167, relheight=0.096)


class Application(Application_ui):
    # 这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)

    def Command1_Cmd(self, event=None):
        # TODO, Please finish the function here!
        pass

    def Command2_Cmd(self, event=None):
        # TODO, Please finish the function here!
        pass

    def Command3_Cmd(self, event=None):
        # TODO, Please finish the function here!
        pass


if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()
    try:
        top.destroy()
    except:
        pass
