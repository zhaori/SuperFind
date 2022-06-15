from fuzzywuzzy import fuzz
from ttkbootstrap import Window, Button, Menu, StringVar, Entry, Combobox, Treeview, Scrollbar
from ttkbootstrap.constants import *

from callbacklib.getData import *
from searchEngine.RefreshFilters import refreshFilter
from searchEngine.result import get_list_data, filename_db
from config.setting import filter_intensity, ico


class AppGUI(object):
    def __init__(self) -> None:
        self.root = Window(
            title=APP_TITLE,
            iconphoto=ico,
            themename="cosmo",
            resizable=(False, False)  # 设置窗口是否可以更改大小
        )
        screenwidth = self.root.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.root.winfo_screenheight()  # 屏幕高度
        width = 1115
        height = 587
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def _win(self):
        # 菜单栏menus
        self.menus = Menu(self.root)
        self.num2 = Menu(self.menus, tearoff=0, activeborderwidth=4)
        self.menus.add_cascade(label='文件', menu=self.num2)
        self.num2.add_command(label='创建计划', command=new_work)
        self.num2.add_command(label='选择计划', command=select_work)
        self.num2.add_command(label='清空计划', command=delete_work)
        self.num2.add_separator()
        self.num2.add_command(label='导入计划', command=importTask)
        self.num2.add_command(label='导出计划', command=export)
        self.num2.add_separator()
        self.num2.add_command(label='启动服务器', command=start_index_server)
        self.root.config(menu=self.menus)

        self.num3 = Menu(self.menus, tearoff=0, activeborderwidth=4)
        self.menus.add_cascade(label='选项', menu=self.num3)
        self.num3.add_command(label='建立本地缓存', command=localfile_cmd)
        self.num3.add_command(label='建立文件索引', command=localIndex_cmd)
        self.num3.add_command(label='清除本地缓存', command=cleanCache)
        self.num3.add_command(label='清除本地索引', command=cleanIndex)
        self.num3.add_separator()
        self.num3.add_command(label='启动自动任务', command=auto_work)
        self.num3.add_command(label='重启本程序', command=auto_work)
        self.root.config(menu=self.menus)

        self.num4 = Menu(self.menus, tearoff=0, activeborderwidth=4)
        self.menus.add_cascade(label='收藏夹', menu=self.num4)
        self.num4.add_command(label='管理收藏夹', command=manage_favorite)

        self.num5 = Menu(self.menus, tearoff=0, activeborderwidth=4)
        self.menus.add_cascade(label='关于', menu=self.num5)
        self.num5.add_command(label='设置', command=option_cmd)
        self.num5.add_command(label='Github', command=open_github)
        self.num5.add_command(label='许可协议', command=open_license)
        # self.num5.add_command(label='使用说明', command=None)
        self.root.config(menu=self.menus)

        # 搜索框
        self.TextVar = StringVar(value='')
        self.Text = Entry(self.root, textvariable=self.TextVar, font=('黑体', 12))
        self.Text.place(relx=0.183, rely=0.05, relwidth=0.4, relheight=0.08)

        self.search = Button(self.root, text='搜索', command=self.search_cmd, bootstyle=PRIMARY)
        self.search.place(relx=0.62, rely=0.05, relwidth=0.09, relheight=0.08)

        # 搜索设置
        comvalue = StringVar()
        self.combox_list = Combobox(self.root, textvariable=comvalue, state='readonly', bootstyle='success')
        self.combox_list["values"] = ("文本文件", "图像文件", "音频文件", "视频文件", "压缩文件", "可执行文件")
        self.combox_list.current(0)
        self.combox_list.bind("<<ComboboxSelected>>", self._combox_handle)
        self.combox_list.place(relx=0.75, rely=0.062, relwidth=0.09)

        columns = ['文件名', '所在路径', '文件后缀名', '创建时间', '修改时间', '文件大小']
        xscroll = Scrollbar(self.root, orient=HORIZONTAL)
        self.table = Treeview(
            master=self.root,  # 父容器
            height=30,  # 表格显示的行数,height行
            columns=columns,  # 显示的列
            show='headings',  # 隐藏首列
            xscrollcommand=xscroll.set,
        )

        def treeview_sort_column(tv, col, reverse):  # Treeview、列名、排列方式
            sort_list = [(tv.set(k, col), k) for k in tv.get_children('')]
            sort_list.sort(reverse=reverse)  # 排序方式
            for index, (val, k) in enumerate(sort_list):  # 根据排序后索引移动
                tv.move(k, '', index)
            tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

        for col in columns:  # 给所有标题加（循环上边的“手工”）
            self.table.heading(col, text=col, command=lambda _col=col: treeview_sort_column(self.table, _col, False))

        self.table.heading('文件名', text='文件名', anchor=CENTER)  # 定义表头
        self.table.heading('所在路径', text='所在路径', anchor=CENTER)
        self.table.heading('文件后缀名', text='文件后缀名', anchor=CENTER)
        self.table.heading('创建时间', text='创建时间', anchor=CENTER)
        self.table.heading('修改时间', text='修改时间', anchor=CENTER)
        self.table.heading('文件大小', text='文件大小(KB)', anchor=CENTER)

        self.table.column('文件名', width=20, minwidth=30, anchor=S)  # 定义列
        self.table.column('所在路径', width=250, minwidth=100, anchor=S)
        self.table.column('文件后缀名', width=10, minwidth=10, anchor=S)
        self.table.column('创建时间', width=10, minwidth=10, anchor=S)
        self.table.column('修改时间', width=10, minwidth=10, anchor=S)
        self.table.column('文件大小', width=10, minwidth=10, anchor=S)
        self.table.place(relx=0.05, rely=0.164, relwidth=0.89, relheight=0.818)

    # 功能实现区
    def _combox_handle(self, *args):
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

    def right_button(self, event):
        root_file = None
        for i in self.table.selection():
            _text = self.table.item(i, "values")
            root_file = os.path.join(_text[1], _text[0])

        g = GetData(root_file)
        menuBar = Menu(self.root, tearoff=0, activeborderwidth=3)
        menuBar.add_command(label='加入到收藏夹', command=g.add_favorite)
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

    def search_cmd(self, event=None):
        x = self.table.get_children()
        for item in x:
            self.table.delete(item)
        get_text = self.Text.get()
        for _ in filename_db.keys():
            if filter_intensity <= fuzz.partial_ratio(_, get_text) <= 100:
                for i in get_list_data(_):
                    if i.get('suffix') in self._combox_handle():
                        self.table.insert('', END, values=[i.get('filename'), i.get('path'), i.get('suffix'),
                                                           i.get("create_time"), i.get("update_time"), i.get("size")])
        self.table.bind('<Button-3>', self.right_button)  # 右键单击
        self.table.bind('<Double-1>', self.open_file)  # 左键双击

    def run(self):
        self._win()
        self.root.mainloop()


if __name__ == "__main__":
    AppGUI().run()
