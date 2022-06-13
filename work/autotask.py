import os
from time import strftime, localtime, time, sleep
import json

from redis import exceptions

from config.server import *
from config.setting import select_task_file, task_db
from searchEngine.findDocument import file_info
from lib.sqlite import *
from lib.redisDB import RedisServer


class NewFindData(object):
    def __init__(self):
        self.get_now_time = strftime('%Y%m%d', localtime(time()))
        with open(select_task_file, 'r', encoding='utf-8') as f:
            open_task_file = f.read()
        try:
            self.get_task_data = json.loads(open_task_file)
            self.begin_time = self.get_task_data['begin_time']
            self.end_time = self.get_task_data['end_time']
            self.task_path = self.get_task_data['task_path']
        except json.decoder.JSONDecodeError:
            # 当读取到了一个空的TaskDb.json文件，不应该报错，而是忽略
            pass

        self.db = SQLiteDB(db_table, db_mode, db_sql, path=task_db)
        self.cache_db = RedisServer(redis_host, redis_port, db=file_db)
        search_data_result = self.db.supersql(
            f"select filename, path from cache where path like '%{os.path.basename(self.task_path)}%'")
        self.database_db = set(os.path.join(d[1], d[0]) for d in search_data_result)
        self.disk_db = set()
        for root, dirs, names in os.walk(self.task_path):
            for name in names:
                self.disk_db.add(os.path.join(root, name))

    # def _get_different_new_set(self):
    #     # 取差集，即，如果现在硬盘上的文件存在，但数据库里不存在的话，便视为被修改、增加
    #     return self.disk_db.difference(self.database_db)
    #
    # def _get_different_del_set(self):
    #     # 取差集，即，如果现在硬盘上的文件不存在，但数据库里存在的话，便视为被删除
    #     return self.database_db.difference(self.disk_db)

    def get_get_data(self, data):
        if data:
            for i in data:
                self.cache_db.delete(file_info(i)['filename'])
            for i in data:
                self.cache_db.push(file_info(i)['filename'], file_info(i))
                self.db.insert(file_info(i))
        else:
            return None

    def mainloop(self):
        # self.get_get_data(self._get_different_new_set())
        # self.get_get_data(self._get_different_del_set())
        while 1:
            try:
                self.cache_db.save()
            except exceptions.ResponseError:
                pass
            self.db.com_clone()
            sleep(3)


if __name__ == "__main__":
    NewFindData().mainloop()