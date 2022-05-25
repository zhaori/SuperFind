import hashlib
import os
from time import strftime, localtime
from tkinter.messagebox import showinfo, showerror
import webbrowser

from pyperclip import copy

from config.server import redis_host, redis_port, suffix_db, file_db
from searchEngine.differentIndex import RefreshIndex
from searchEngine.findDocument import *
from setting import APP_TITLE
from sqlBase.redisDB import RedisServer


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


def about_Cmd():
    showinfo("关于&说明", "关于：\n"
                      "作者：皮得狠 \n"
                      "Github：https://github.com/zhaori")


def start_index_server():
    def _start():
        os.system('indexDB.exe')
        localIndex_cmd()

    Thread(target=_start).start()


def option_cmd(event=None):
    def _option():
        os.system(r"Notepad2.exe setting.py")

    Thread(target=_option).start()


def localfile_cmd():
    try:
        create_thread(function=find, data=search_list)
        cache_db()
        showinfo('提示', '本地缓存已成功创建')
    except Exception as e:
        showerror("ERROR", str(e))


def localIndex_cmd():
    try:
        Thread(target=RefreshIndex).start()
        showinfo('提示', '本地索引已成功创建')
    except Exception as e:
        pass


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
        os.system(r"D:\PyVenv\SuperFind\Scripts\python.exe "
                  r"C:\Users\14715\OneDrive\code\Python\exploitation\SuperFind\lib\tkcalendar.py")

    Thread(target=run).start()


def select_work():
    def run():
        os.system(r"D:\PyVenv\SuperFind\Scripts\python.exe "
                  r".\lib\select_task.py")

    Thread(target=run).start()


def open_github():
    def url_from_github():
        webbrowser.open("https://github.com/zhaori")

    Thread(target=url_from_github).start()
