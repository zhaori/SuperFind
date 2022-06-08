import os
from time import strftime, localtime, time
import json

import redis.exceptions

from config.server import *
from searchEngine.findDocument import file_info
from lib.sqlite import *
from lib.redisDB import RedisServer

# cache_db = RedisServer(redis_host, redis_port, db=file_db)
get_now_time = strftime('%Y%m%d', localtime(time()))

with open(r"./data/TaskDB.json", 'r', encoding='utf-8') as f:
    open_task_file = f.read()

get_task_data = json.loads(open_task_file)
begin_time = get_task_data['begin_time']
end_time = get_task_data['end_time']
task_path = get_task_data['task_path']

# db = SQLiteDB(db_table, db_mode, db_sql, path=r".\data\Cache.db")
# search_data_result = db.supersql(f"select filename, path from cache where path like '%{os.path.basename(task_path)}%'")


# 从数据库读取文件，再从硬盘读取文件，判断文件是否存在
# database_data = set()
# for d in search_data_result:
#     database_data.add(os.path.join(d[1], d[0]))

# now_search_data = set()
# for root, dirs, names in os.walk(task_path):
#     for name in names:
#         now_search_data.add(os.path.join(root, name))


class NewFindData(object):
    def __init__(self):
        self.db = SQLiteDB(db_table, db_mode, db_sql, path=r".\data\Cache.db")
        self.cache_db = RedisServer(redis_host, redis_port, db=file_db)
        search_data_result = self.db.supersql(f"select filename, path from cache where path like '%{os.path.basename(task_path)}%'")
        self.database_db = set(os.path.join(d[1], d[0]) for d in search_data_result)
        self.disk_db = set()
        for root, dirs, names in os.walk(task_path):
            for name in names:
                self.disk_db.add(os.path.join(root, name))



    def _get_different_new_set(self):
        # 取差集，即，如果现在硬盘上的文件存在，但数据库里不存在的话，便视为被修改、增加
        return self.disk_db.difference(self.database_db)

    def _get_different_del_set(self):
        # 取差集，即，如果现在硬盘上的文件不存在，但数据库里存在的话，便视为被删除
        return self.database_db.difference(self.disk_db)

    def get_get_data(self, data):
        if data:
            for i in data:
                self.cache_db.delete(file_info(i)['filename'])
                self.cache_db.push(file_info(i)['filename'], file_info(i))
                self.db.insert(file_info(i))
        else:
            return None

    def main(self):
        self.get_get_data(self._get_different_new_set())
        self.get_get_data(self._get_different_del_set())
        try:
            self.cache_db.save()
        except redis.exceptions.ResponseError:
            pass
        self.db.com_clone()


if __name__ == "__main__":
    NewFindData().main()
# 取差集，即，如果现在硬盘上的文件存在，但数据库里不存在的话，便视为被修改、增加
# get_different_new_set = now_search_data.difference(database_data)
# 取差集，即，如果现在硬盘上的文件不存在，但数据库里存在的话，便视为被删除
# get_different_del_set = database_data.difference(now_search_data)
# if get_different_new_set:
#     for i in get_different_new_set:
#         cache_db.delete(file_info(i)['filename'])
#         cache_db.push(file_info(i)['filename'], file_info(i))
#         db.insert(file_info(i))
# elif get_different_del_set:
#     for i in get_different_new_set:
#         cache_db.delete(file_info(i)['filename'])
#         cache_db.push(file_info(i)['filename'], file_info(i))
#         db.insert(file_info(i))
# db.com_clone()
# db.delete('path', re.sub(r"\\","/", str(search_data_result[0]).strip("('',)")))
# data_set = set()
# for s in search_data_result:
# print(str(s).strip("('',)"))
# print(re.sub(r"\\", r"\/", str(s).strip("('',)")))
#     data_set.add(str(s).strip("('',)"))
# for i in data_set:
#     print(i)
#     db.delete('path', i)
# print(data_set)
# db.com_clone()
# find(task_path)
# create_thread(db.insert, getfileinfo())
"""

"""
