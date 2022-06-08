from setting import ico
from ttkbootstrap import Window, Button, Treeview, Scrollbar
from ttkbootstrap.constants import *

from setting import ico
from work.Chooseplan import AddFavorite


class Favorites(object):
    def __init__(self):
        self.root = Window(title='收藏夹',
                           themename='cosmo',
                           iconphoto=ico,
                           resizable=(False, False))
        self.style = "primary"
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        width = 560
        height = 460
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.del_file = None
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.table = Treeview(
            master=self.root,  # 父容器
            height=30,  # 表格显示的行数,height行
            columns=['文件名', '路径'],  # 显示的列
            show='headings',  # 隐藏首列
            xscrollcommand=Scrollbar(self.root, orient=HORIZONTAL).set,
        )

    def _get_data(self):
        for i in AddFavorite('../data/Favorites.json').search():
            self.table.insert('', END, values=(i['filename'], i['path']))

    def select(self, event=None):
        # 单击项目时触发
        for i in self.table.selection():
            _text = self.table.item(i, "values")
            self.del_file = _text[0]

    def _del_data(self):
        AddFavorite('../data/Favorites.json').delete('filename', self.del_file)
        self.del_btn.after(1000, self.null_data)

    def null_data(self):
        for i in self.table.get_children():
            self.table.delete(i)
        self._get_data()

    def _win(self):
        # self.edit_btn = Button(self.root, text='编辑', command=None, bootstyle=PRIMARY)
        self.del_btn = Button(self.root, text='删除', command=self._del_data, bootstyle=PRIMARY)
        # self.edit_btn.place(relx=0.76, rely=0.05, relwidth=0.19, relheight=0.08)
        self.del_btn.place(relx=0.76, rely=0.2, relwidth=0.19, relheight=0.08)

        self.table.heading('文件名', text='文件名', anchor=CENTER)  # 定义表头
        self.table.heading('路径', text='路径', anchor=CENTER)  # 定义表头
        self.table.column('文件名', width=30, minwidth=20, anchor=S)  # 定义列
        self.table.column('路径', width=80, minwidth=70, anchor=S)  # 定义列
        self.table.bind('<Double-1>', self.select)
        self.table.place(relx=0.05, rely=0.05, relwidth=0.65, relheight=0.918)

    def run(self):
        self._get_data()
        self._win()
        self.root.mainloop()


if __name__ == "__main__":
    Favorites().run()
