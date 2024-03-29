import hashlib
from time import strftime, localtime
from tkinter.messagebox import showinfo, showerror
import webbrowser
from pyperclip import copy

from config.server import redis_host, redis_port, suffix_db, file_db
from searchEngine.differentIndex import RefreshIndex
from searchEngine.findDocument import *
from config.setting import APP_TITLE, select_task_file, task_db
from lib.redisDB import RedisServer
from work.transfer import export_task, import_task
from work.autotask import NewFindData
from work.Chooseplan import SaveTask, AddFavorite
from work.favorites import Favorites
from tkcalendar import Calendar


class GetData(object):
    def __init__(self, data):
        self.data = data

    def copy_absolute(self):
        copy(self.data)

    def open_path(self):
        folder = self.data[0:-len(os.path.basename(self.data))]
        os.startfile(folder)

    def delete_file(self):
        try:
            os.remove(self.data)
        except FileNotFoundError as e:
            showerror("FileNotFoundError", str(e))

    def get_attribute(self):
        file_size = os.stat(self.data).st_size // 1024
        ctime = strftime('%Y.%m.%d.%X', localtime(os.stat(self.data).st_ctime))
        mtime = strftime('%Y.%m.%d.%X', localtime(os.stat(self.data).st_mtime))
        showinfo("文件属性",
                 f"文件名：{os.path.basename(self.data)} \n\n"
                 f"文件大小：{file_size}  单位：KB \n"
                 f"创建日期：{ctime} \n"
                 f"修改日期：{mtime} \n"
                 f"文件哈希值：{hashlib.md5(self.data.encode('utf8')).hexdigest()}")

    def add_favorite(self):
        f = AddFavorite()
        f.insert(file_info(self.data))
        f.submit()


def manage_favorite():
    Favorites().run()


def start_work():
    Calendar().run()


def about_Cmd():
    showinfo("关于&说明", "关于：\n"
                      "作者：皮得狠 \n"
                      "Github：https://github.com/zhaori")


def start_index_server():
    def _start():
        os.system('start /B indexDB.exe')
        localIndex_cmd()

    Thread(target=_start).start()


def option_cmd(event=None):
    def _option():
        os.system(r"start /B Notepad2.exe ./config/setting.py")

    Thread(target=_option).start()


def localfile_cmd(data=search_list):
    try:
        create_thread(function=find, data=data)
        cache_db()
        showinfo('提示', '本地缓存已成功创建')
    except Exception as e:
        showerror("ERROR", str(e))


def localIndex_cmd():
    try:
        t = Thread(target=RefreshIndex)
        t.setDaemon(True)
        t.start()
        showinfo('提示', '本地索引已成功创建')
    except Exception as e:
        showerror("ERROR", str(e))


def cleanCache():
    try:
        os.remove(db)
    except FileNotFoundError:
        showerror(APP_TITLE, "没在data文件夹中找到cache.db数据库")

    showinfo(APP_TITLE, "本地缓存清除成功")


def cleanIndex():
    try:
        RedisServer(redis_host, redis_port, suffix_db).clean()
        RedisServer(redis_host, redis_port, file_db).clean()
        showinfo(APP_TITLE, "索引清除成功")
    except Exception as e:
        showerror(APP_TITLE, str(e))


def new_work():
    def run():
        os.system('start /B tkcalendar.exe')

    Thread(target=run).start()


def auto_work():
    t = Thread(target=NewFindData().mainloop)
    t.setDaemon(True)
    t.start()


def restart():
    print(__file__)


def select_work():
    def run():
        os.system("start /B select_task.exe")
    Thread(target=run).start()


def delete_work():
    def run():
        mytaskdb = SaveTask(task_db)
        try:
            os.remove(select_task_file)
        except FileNotFoundError:
            pass
        finally:
            mytaskdb.delete('task')
            mytaskdb.submit()

    Thread(target=run).start()


def export():
    # 导出任务
    Thread(target=export_task).start()


def importTask():
    Thread(target=import_task).start()


def open_github():
    def url_from_github():
        webbrowser.open("https://github.com/zhaori")

    Thread(target=url_from_github).start()


def open_license():
    def run():
        os.system("start /B Notepad2.exe LICENSE")

    def run2():
        os.system("start /B Notepad2.exe LICENSE996_CN")

    thread_list = [Thread(target=run), Thread(target=run2)]
    for i in thread_list:
        i.start()
    for i in thread_list:
        i.join()


if __name__ == "__main__":
    restart()
