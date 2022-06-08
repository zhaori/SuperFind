from tkinter.filedialog import asksaveasfile, askopenfile
from setting import select_task_file


def export_task():
    save_file = asksaveasfile(initialfile='TaskDB.json', filetypes=[("JSON Document", ".json")], title='保存为')
    save_file.write(open(select_task_file, 'r', encoding='utf-8').read())


def import_task():
    open_file = askopenfile(mode='r', filetypes=[("JSON Document", ".json")], title='打开任务文件')
    with open(select_task_file, 'w', encoding='utf-8') as f:
        f.write(open_file.read())


if __name__ == "__main__":
    # export_task()
    import_task()
