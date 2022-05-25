import sqlite3
from tkinter import filedialog

from ttkbootstrap import Window, Button, StringVar, Combobox, Label, Entry, IntVar
from ttkbootstrap.tooltip import ToolTip

from lib.Chooseplan import SaveTask
from setting import ico, task_db


class Calendar(object):
    def __init__(self):
        self.db = SaveTask(task_db)
        try:
            self.db.database_init()
        except sqlite3.OperationalError:
            pass
        self.root = Window(title='计划时间',
                           themename='cosmo',
                           iconphoto=ico,
                           resizable=(False, False))
        self.style = "primary"
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        width = 360
        height = 460
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        self.var_begin_var = IntVar(value=20220520)  # 开始日期
        self.var_begin = Entry(self.root, textvariable=self.var_begin_var, font=('宋体', 12))

        self.var_end_var = IntVar(value=20220521)  # 结束日期
        self.var_end = Entry(self.root, textvariable=self.var_end_var, font=('宋体', 12))

        self.auto_time_var = IntVar(value=3)  # 间隔循环时间 单位为秒
        self.auto_time = Entry(self.root, textvariable=self.auto_time_var, font=('宋体', 12))

        self.time_unit_var = StringVar()
        self.time_unit_list = Combobox(self.root, textvariable=self.time_unit_var, state='readonly',
                                       bootstyle=self.style)

        self.textVar = StringVar(value='查找D盘')
        self.text = Entry(self.root, textvariable=self.textVar, font=('宋体', 12))

        self.taskvar = StringVar()
        self.task = Entry(self.root, textvariable=self.taskvar, font=('宋体', 12))
        self.path_text = None

    def _get_begin(self):
        return self.var_begin.get()

    def _get_end(self):
        return self.var_end.get()

    def _get_name(self):
        return self.text.get()

    def _get_time(self, *args):
        return self.auto_time.get()

    def _get_path(self):
        p = filedialog.askdirectory()
        self.path_text = p
        return self.taskvar.set(p)

    def _get_path_text(self):
        return self.task.get()

    def _work_name(self):
        Label(text='任务名', bootstyle=self.style).place(relx=0.1, rely=0.05)

        self.text.place(relx=0.28, rely=0.03, relwidth=0.46, relheight=0.09)

    def _set_time(self):
        Label(text='开始时间', bootstyle=self.style).place(relx=0.08, rely=0.2)
        self.var_begin.place(relx=0.28, rely=0.18, relwidth=0.46, relheight=0.09)

        ToolTip(self.var_begin, text='只能输入数字，小时分钟秒的顺序填写，例如：132003代表的是下午1点20分03秒')

        Label(text='结束时间', bootstyle=self.style).place(relx=0.08, rely=0.35)
        self.var_end.place(relx=0.28, rely=0.33, relwidth=0.46, relheight=0.09)

        Label(text='循环间隔', bootstyle=self.style).place(relx=0.08, rely=0.5)
        Label(text='秒', bootstyle=self.style).place(relx=0.78, rely=0.5)
        self.auto_time.place(relx=0.28, rely=0.48, relwidth=0.46, relheight=0.09)

        Label(text='检索目标', bootstyle=self.style).place(relx=0.08, rely=0.65)
        task_btn = Button(self.root, text='选择', bootstyle=self.style, command=self._get_path)
        task_btn.place(relx=0.78, rely=0.64, relwidth=0.2)
        self.task.place(relx=0.28, rely=0.63, relwidth=0.46, relheight=0.09)

    def _get_all_data(self):
        data = {
            "task_name": self._get_name(),
            "task_path": self.path_text,
            "begin_time": self._get_begin(),
            "end_time": self._get_end(),
            "loop_time": self._get_time(),
        }
        self.root.destroy()
        self.db.insert(data, 'task')
        self.db.submit('task')
        # return data['task_path']

        # return json.dumps(data, indent=4, ensure_ascii=False)

    def _generate(self):
        gen_btn = Button(self.root, text='生成任务', command=self._get_all_data, bootstyle='success')
        gen_btn.place(relx=0.38, rely=0.83, relwidth=0.25)

    def run(self):
        self._work_name()
        self._set_time()
        self._generate()
        self.root.mainloop()


if __name__ == "__main__":
    Calendar().run()
