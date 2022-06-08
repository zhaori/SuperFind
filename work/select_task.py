import json
from _tkinter import TclError
from tkinter.messagebox import showinfo

from fuzzywuzzy import fuzz
from ttkbootstrap import Window, Button, StringVar, Combobox, Entry
from ttkbootstrap.tooltip import ToolTip

from work.Chooseplan import SaveTask
from setting import filter_intensity, select_task_file
from setting import task_db, ico
from lib.sqlite import *


class SelectTask(object):
    def __init__(self):
        self.db = SaveTask(task_db)
        self.root = Window(title='加载任务',
                           iconphoto=ico,
                           themename='cosmo',
                           resizable=(False, False))
        self.style = "primary"
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        width = 260
        height = 260
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        comvalue = StringVar()
        self.combox_list = Combobox(self.root, textvariable=comvalue, state='readonly', bootstyle=self.style)
        self.combox_data = None
        self.search_task_var = StringVar()
        self.search_task = Entry(self.root, textvariable=self.search_task_var, font=('宋体', 12))
        ToolTip(self.search_task, text='当搜索框搜索内容不存在时，获得所有任务')
        self.search_task_btn = Button(self.root, text='搜索', bootstyle=self.style, command=self._search_task)
        self.search_task_ok = Button(self.root, text='确定', bootstyle='success', command=self._select_task)

    def _combox_handle(self, *args):
        handle_data = self.combox_list.get()
        ToolTip(self.combox_list, text=handle_data)
        return handle_data

    def _select_task(self, *args):
        # self.db.query_all('task', 'task_name', self.combox_list.get())
        select_db_data = str_to_tuple(self.db.query_all('task', 'task_name', self.combox_list.get()))
        data_json = {
            "task_id": select_db_data[0],
            'task_name': select_db_data[1],
            "task_path": select_db_data[2],
            "begin_time": select_db_data[3],
            "end_time": select_db_data[4],
            "loop_time": select_db_data[5]
        }
        try:
            with open(select_task_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(data_json, indent=4, ensure_ascii=False))
            showinfo('任务选择', f'任务选择成功，任务名为{select_db_data[1]}')
            self.root.quit()
        except:
            pass

    def _search_task(self, *args):
        search_task_data = []
        search_tuple = [list_to_str(n) for n in self.db.query('task_name')]
        for i in [list_to_str(n) for n in self.db.query('task_name')]:
            if filter_intensity < fuzz.partial_ratio(i, self.search_task.get()) <= 100:
                search_task_data.append(i)
        if search_task_data is None:
            self.combox_data = tuple(search_tuple)
        else:
            self.combox_data = tuple(search_task_data)

        self.combox_list["values"] = tuple(search_tuple)
        try:
            self.combox_list.current(0)
        except TclError:
            self.combox_list["values"] = tuple(search_tuple)

        self.combox_list.bind("<<ComboboxSelected>>", self._combox_handle)
        self.combox_list.place(relx=0.23, rely=0.32, relwidth=0.56)

    def win(self):
        self.search_task.place(relx=0.129, rely=0.06, relwidth=0.55, relheight=0.12)
        self.search_task_btn.place(relx=0.68, rely=0.06, relwidth=0.25, relheight=0.12)
        self.search_task_ok.place(relx=0.34, rely=0.66, relwidth=0.35, relheight=0.15)

        self.root.mainloop()

    # def run(self):
    #     self._win()
    #     self.root.mainloop()


if __name__ == '__main__':
    SelectTask().win()
