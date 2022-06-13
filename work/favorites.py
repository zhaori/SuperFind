from ttkbootstrap import Window, Button, Treeview, Scrollbar
from tkinter.messagebox import showinfo
from ttkbootstrap.constants import *
from work.transfer import *
from config.setting import ico, favorite_file
from work.Chooseplan import AddFavorite
import pyperclip
from ctypes import windll


class Favorites(object):
    def __init__(self):
        self.root = Window(title='收藏夹(双击选择表格项目)',
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
        self.select_file = None
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.table = Treeview(
            master=self.root,  # 父容器
            height=30,  # 表格显示的行数,height行
            columns=['文件名', '路径'],  # 显示的列
            show='headings',  # 隐藏首列
            xscrollcommand=Scrollbar(self.root, orient=HORIZONTAL).set,
        )

    def _get_data(self):
        for i in AddFavorite(favorite_file).search():
            self.table.insert('', END, values=(i['filename'], i['path']))

    def select(self, event=None):
        # 单击项目时触发
        for i in self.table.selection():
            _text = self.table.item(i, "values")
            self.select_file = _text[0]

    def _del_data(self):
        favorite_db = AddFavorite(favorite_file)
        favorite_db.delete('filename', self.select_file)
        favorite_db.submit()
        self.del_btn.after(1000, self.null_data)

    def null_data(self):
        # 清空表格内数据
        for i in self.table.get_children():
            self.table.delete(i)
        self._get_data()

    def _export_file(self):
        export_task("export")

    def _import_file(self):
        import_task("import")
        self.import_btn.after(1000, self._get_data)

    def _get_clipboard(self):
        if windll.user32.OpenClipboard(None):  # 打开剪切板
            windll.user32.EmptyClipboard()  # 清空剪切板
            windll.user32.CloseClipboard()  # 关闭剪切板
        try:
            pyperclip.copy(self.select_file)
            showinfo('', '已成功读取到剪切板')
            self.root.destroy()
        except Exception as e:
            showerror('错误', str(e))

    def _win(self):
        self.del_btn = Button(self.root, text='删除', command=self._del_data, bootstyle=DANGER)
        self.load_btn = Button(self.root, text="载入", command=self._get_clipboard, bootstyle=PRIMARY)
        self.import_btn = Button(self.root, text='导入', command=self._import_file, bootstyle=SUCCESS)
        self.export_btn = Button(self.root, text='导出', command=self._export_file, bootstyle=SUCCESS)
        self.del_btn.place(relx=0.76, rely=0.05, relwidth=0.19, relheight=0.08)
        self.load_btn.place(relx=0.76, rely=0.2, relwidth=0.19, relheight=0.08)
        self.import_btn.place(relx=0.76, rely=0.35, relwidth=0.19, relheight=0.08)
        self.export_btn.place(relx=0.76, rely=0.5, relwidth=0.19, relheight=0.08)

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
