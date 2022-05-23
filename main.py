from tkinter import Tk, Button, Frame, StringVar, Menu, CENTER, S, END, Entry
from tkinter.ttk import Combobox, Treeview, Scrollbar

from fuzzywuzzy import fuzz

from callbacklib.getData import *
from lib.tkcalendar import begin_time
from searchEngine.RefreshFilters import refreshFilter
from searchEngine.result import get_list_data, filename_db
from setting import filter_intensity
from setting import ico


def calender_process():
    Process(target=begin_time).start()


class ApplicationUI(Frame):
    # 这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master)
        super().__init__(master, **kw)
        self.master.title(APP_TITLE)
        self.master.iconbitmap(ico)
        screenwidth = self.master.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.master.winfo_screenheight()  # 屏幕高度
        width = 1115
        height = 587
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.textvariable = None
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.Frame1 = Frame(self.top, bg="AliceBlue")
        self.Frame1.place(relx=0, rely=-0.014, relwidth=0.998, relheight=1.01)

        self.VScroll1 = Scrollbar(self.Frame1, orient='vertical')
        self.VScroll1.place(relx=0.618, rely=0.175, relwidth=0.015, relheight=0.811)

        self.search = Button(self.Frame1, text='搜索', command=self.search_cmd, bg="#87CEEB",
                             highlightthickness=1, activebackground='#40E0D0')  # style='search.TButton'
        self.search.place(relx=0.74, rely=0.067, relwidth=0.09, relheight=0.056)

        comvalue = StringVar()
        self.combox_list = Combobox(self.Frame1, textvariable=comvalue, state='readonly')
        self.combox_list["values"] = ("索引设置", "文本文件", "图像文件", "音频文件", "视频文件", "压缩文件", "可执行文件")
        self.combox_list.current(0)
        self.combox_list.bind("<<ComboboxSelected>>", self.combox_handle)
        self.combox_list.place(relx=0.85, rely=0.066, relwidth=0.09, relheight=0.056)

        self.menus = Menu(self.master)  # 在window上创建一个菜单栏menus
        self.num2 = Menu(self.menus, tearoff=0, font=('宋体', 10))  # 在menus上面创建一个选项栏num
        self.menus.add_cascade(label='文件', menu=self.num2)
        self.num2.add_command(label='创建计划', command=calender_process)
        self.num2.add_command(label='导入计划', command=None)
        self.num2.add_command(label='导出计划', command=None)
        self.num2.add_separator()
        self.num2.add_command(label='启动服务器', command=start_redis)
        self.num2.add_command(label='重启服务器', command=restart_redis)
        self.num2.add_command(label='验证服务器', command=check_redis)
        self.master.config(menu=self.menus)

        self.num3 = Menu(self.menus, tearoff=0, font=('宋体', 10))
        self.menus.add_cascade(label='选项', menu=self.num3)
        self.num3.add_command(label='建立本地缓存', command=localFile_Cmd)
        self.num3.add_command(label='建立文件索引', command=localIndex_Cmd)
        self.num3.add_command(label='清除本地缓存', command=cleanCache)
        self.num3.add_command(label='清除本地索引', command=cleanIndex)
        self.master.config(menu=self.menus)

        self.num4 = Menu(self.menus, tearoff=0, font=('宋体', 10))
        self.menus.add_cascade(label='收藏夹', menu=self.num4)
        self.num4.add_command(label='加入收藏夹', command=None)
        self.num4.add_command(label='查看收藏夹', command=None)

        self.num = Menu(self.menus, tearoff=0, font=('宋体', 10))
        self.menus.add_cascade(label='关于', menu=self.num)
        self.num.add_command(label='设置', command=option_Cmd)
        self.num.add_command(label='Github', command=None)
        self.num.add_command(label='许可协议', command=None)
        self.num.add_command(label='使用说明', command=None)
        self.master.config(menu=self.menus)

        columns = ['文件名', '所在路径', '文件后缀名', '创建时间', '修改时间', '文件大小']
        self.table = Treeview(
            master=self.master,  # 父容器
            height=30,  # 表格显示的行数,height行
            columns=columns,  # 显示的列
            show='headings',  # 隐藏首列
        )

        # 排序 引用 https://blog.csdn.net/sinat_27382047/article/details/80161637
        def treeview_sort_column(tv, col, reverse):  # Treeview、列名、排列方式
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            l.sort(reverse=reverse)  # 排序方式
            for index, (val, k) in enumerate(l):  # 根据排序后索引移动
                tv.move(k, '', index)
            tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

        for col in columns:  # 给所有标题加（循环上边的“手工”）
            self.table.heading(col, text=col, command=lambda _col=col: treeview_sort_column(self.table, _col, False))

        self.table.heading('文件名', text='文件名', anchor=CENTER)  # 定义表头
        self.table.heading('所在路径', text='所在路径', anchor=CENTER)
        self.table.heading('文件后缀名', text='文件后缀名', anchor=CENTER)
        self.table.heading('创建时间', text='创建时间', anchor=CENTER)
        self.table.heading('修改时间', text='修改时间', anchor=CENTER)
        self.table.heading('文件大小', text='文件大小', anchor=CENTER)

        self.table.column('文件名', width=20, minwidth=30, anchor=S)  # 定义列
        self.table.column('所在路径', width=250, minwidth=100, anchor=S)
        self.table.column('文件后缀名', width=10, minwidth=10, anchor=S)
        self.table.column('创建时间', width=10, minwidth=10, anchor=S)
        self.table.column('修改时间', width=10, minwidth=10, anchor=S)
        self.table.column('文件大小', width=10, minwidth=10, anchor=S)
        self.table.place(relx=0.05, rely=0.164, relwidth=0.89, relheight=0.818)

        self.Text1Var = StringVar(value='')
        self.Text1 = Entry(self.Frame1, textvariable=self.Text1Var, font=('宋体', 12))
        self.Text1.place(relx=0.113, rely=0.067, relwidth=0.6, relheight=0.058)


class Application(ApplicationUI):
    # 这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        ApplicationUI.__init__(self, master)
        self.file = None

    def right_button(self, event):
        root_file = None
        for i in self.table.selection():
            _text = self.table.item(i, "values")
            root_file = os.path.join(_text[1], _text[0])

        g = GetData(root_file)
        menuBar = Menu(self.master, tearoff=0)
        menuBar.add_command(label='复制绝对路径', command=g.copy_absolute)
        menuBar.add_command(label='打开文件位置', command=g.open_path)
        menuBar.add_command(label='删除文件', command=g.delete_file)
        menuBar.add_command(label='查看文件属性', command=g.get_attribute)
        menuBar.post(event.x_root, event.y_root)

    def select(self, event=None) -> str:
        # 单击项目时触发
        for i in self.table.selection():
            _text = self.table.item(i, "values")
            root_file = os.path.join(_text[1], _text[0])
            return root_file

    def open_file(self, event=None):
        _file = None
        for i in self.table.selection():
            _text = self.table.item(i, "values")
            _file = os.path.join(_text[1], _text[0])
        os.startfile(_file)

    def combox_handle(self, *args):
        get_refresh = refreshFilter().get_data()
        if self.combox_list.get() == "音频文件":
            return get_refresh['audio']

        elif self.combox_list.get() == "压缩文件":
            return get_refresh['compressed']

        elif self.combox_list.get() == "文本文件":
            return get_refresh['document']

        elif self.combox_list.get() == "可执行文件":
            return get_refresh['executable']

        elif self.combox_list.get() == "图像文件":
            return get_refresh['picture']

        elif self.combox_list.get() == "视频文件":
            return get_refresh['video']

        else:
            return get_refresh['all']

    def search_cmd(self, event=None):
        x = self.table.get_children()
        for item in x:
            self.table.delete(item)
        get_text = self.Text1.get()
        for _ in filename_db.keys():
            if filter_intensity <= fuzz.partial_ratio(_, get_text) <= 100:
                for i in get_list_data(_):
                    if i.get('suffix') in self.combox_handle():
                        self.table.insert('', END, values=[i.get('filename'), i.get('path'), i.get('suffix')])

        # self.table.bind('<Button-1>', self.left_button)  # 左键单击
        self.table.bind('<Button-3>', self.right_button)  # 右键单击
        self.table.bind('<Double-1>', self.open_file)  # 左键双击

    def add_favorites(self):
        print(self.select())


"""
事件	代码	备注
鼠标左键单击按下	1/Button-1/ButtonPress-1	 
鼠标左键单击松开	ButtonRelease-1	 
鼠标右键单击	3	 
鼠标左键双击	Double-1/Double-Button-1	 
鼠标右键双击	Double-3	 
鼠标滚轮单击	2	 
鼠标滚轮双击	Double-2	 
鼠标移动	B1-Motion	 
鼠标移动到区域	Enter	 
鼠标离开区域	Leave	 
获得键盘焦点	FocusIn	 
失去键盘焦点	FocusOut	 
键盘事件	Key	 
回车键	Return	 
控件尺寸变	Configure
"""


def mainUI():
    top = Tk()
    Application(top).mainloop()
    try:
        top.destroy()
    except:
        pass


if __name__ == "__main__":
    mainUI()
