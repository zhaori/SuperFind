import sqlite3
from datetime import datetime
from os import popen, path, stat
from threading import Thread

from config.server import db_table, db_mode, db
from setting import search_list

files_list = []


def file_info(file: str) -> dict:
    # 构建一个存入数据库的数据格式 字典
    try:
        info = {
            "suffix": path.splitext(file)[1][1:],
            "filename": path.basename(file),
            "path": path.dirname(file),
            "size": path.getsize(file),
            "ModificationDate": datetime.fromtimestamp(stat(file).st_mtime).strftime('%Y%m%d%H%M')
        }
        return info
    except OSError:
        pass


def find(root):
    for f in popen(f'dir /a:-d /s /b {root}'):
        if str(path.basename(str(f).strip('\n'))).find('.') != 0:
            files_list.append(file_info(str(f).strip('\n')))


def create_thread(function, data: list):
    """
    :param function: 运行函数
    :param data: 可迭代数组
    :return: 创建多线程任务
    """
    # 在生命周期里，files_list变量为公告变量且值会一直存在
    if files_list is not None:
        files_list.clear()

    thread_list = [Thread(target=function, args=(d,)) for d in data]
    for p in thread_list:
        p.start()
    for p in thread_list:
        p.join()


def cache_db():
    # 如果db文件已存在，先删除再重新建立索引
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(f'drop table if exists {db_table}')
    cur.execute(db_mode)
    con.commit()

    # 下方是处理数据列表中存在为None的情况
    while None in files_list:
        files_list.remove(None)

    for ff in files_list:
        cur.execute(f"""
       insert into {db_table} (
            suffix, filename, path, size, ModificationDate
        ) values (:suffix, :filename, :path, :size, :ModificationDate)
    """, (ff.get("suffix"), ff.get("filename"), ff.get("path"), ff.get("size"), ff.get("ModificationDate")))
    con.commit()
    con.close()


if __name__ == "__main__":
    # find(r'D:\我的文件')

    # a = time.time()
    create_thread(function=find, data=search_list)
    cache_db()
    print(files_list)
    # # db = MongodbServer()
    # # db.insert_list('Cache', 'ALL', files_list) # 25.59869408607483
    # cache_db()
    # print(time.time() - a)
