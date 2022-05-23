import json
import os

from ttkbootstrap import Window, Button, StringVar, Combobox, Label, Entry, IntVar
from ttkbootstrap.tooltip import ToolTip

from setting import ico


class fileJSON(object):
    # noinspection PyPep8Naming
    def __init__(self, json_file, data=None):
        self.json_file = json_file

        if os.path.isfile(self.json_file) is False:
            with open(json_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(data, indent=4, ensure_ascii=False))

    def upgrade_value(self, root, value):
        """
        root: 预更改的键
        value：预更改的值
        """
        if os.path.isfile(self.json_file) is True:
            with open(self.json_file, 'r', encoding="utf-8") as f:
                data_json = dict(json.loads(f.read()))
            data_json[root] = value
            with open(self.json_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(data_json, indent=4, ensure_ascii=False))

    def read_time(self, root):
        if os.path.isfile(self.json_file) is True:
            with open(self.json_file, 'r', encoding="utf-8") as f:
                data_json = dict(json.loads(f.read()))
        return data_json[root]


def create_json(file, key, value):
    fileJSON(file).upgrade_value(key, value)


class Calendar(object):
    def __init__(self):
        self.root = Window(title='计划时间',
                           themename='cosmo',
                           iconphoto=ico,
                           resizable=(False, False))
        self.style = "primary"
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        width = 360
        height = 360
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

    def _get_begin(self):
        return self.var_begin.get()

    def _get_end(self):
        return self.var_end.get()

    def _get_name(self):
        return self.text.get()

    def _get_time(self, *args):
        return str(self.auto_time.get())

    def _work_name(self):
        Label(text='任务名', bootstyle=self.style).place(relx=0.1, rely=0.06)

        self.text.place(relx=0.28, rely=0.05, relwidth=0.46, relheight=0.09)

    def _set_time(self):
        Label(text='开始时间', bootstyle=self.style).place(relx=0.08, rely=0.27)
        self.var_begin.place(relx=0.28, rely=0.25, relwidth=0.46, relheight=0.09)

        ToolTip(self.var_begin, text='只能输入数字，小时分钟秒的顺序填写，例如：132003代表的是下午1点20分03秒')

        Label(text='结束时间', bootstyle=self.style).place(relx=0.08, rely=0.47)
        self.var_end.place(relx=0.28, rely=0.45, relwidth=0.46, relheight=0.09)

        Label(text='循环间隔', bootstyle=self.style).place(relx=0.08, rely=0.67)
        Label(text='秒', bootstyle=self.style).place(relx=0.78, rely=0.67)
        self.auto_time.place(relx=0.28, rely=0.65, relwidth=0.46, relheight=0.09)

    def _get_all_data(self):
        data = {
            "work_name": self._get_name(),
            "begin_time": self._get_begin(),
            "end_time": self._get_end(),
            "loop_time": self._get_time(),
        }
        self.root.destroy()
        return dict(data)
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
