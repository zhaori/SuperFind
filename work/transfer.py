from tkinter.filedialog import asksaveasfile, askopenfile
from config.setting import select_task_file, favorite_file
from tkinter.messagebox import showerror


def export_task(option=None):
    if option == "export":
        file = favorite_file
    else:
        file = select_task_file
    save_file = asksaveasfile(initialfile=file, filetypes=[("JSON Document", ".json")], title='保存为')
    try:
        save_file.write(open(file, 'r', encoding='utf-8').read())
    except AttributeError:
        showerror('导出任务', '导出失败')


def import_task(option=None):
    if option == "import":
        file = favorite_file
    else:
        file = select_task_file
    open_file = askopenfile(mode='r', filetypes=[("JSON Document", ".json")], title='打开文件')
    try:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(open_file.read())
    except AttributeError:
        showerror('导入任务', '导入失败')


if __name__ == "__main__":
    # export_task()
    import_task()
