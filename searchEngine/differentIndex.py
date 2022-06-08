import os
import time
from threading import Thread

from config.server import *
from searchEngine.RefreshFilters import refreshFilter
from lib.redisDB import RedisServer
from lib.sqlite import SQLiteDB

cache_db = RedisServer(redis_host, redis_port, db=file_db)


class createIndex(object):
    def __init__(self):
        self.cache_db = SQLiteDB(table=db_table, path=db)
        # self.file_redis = RedisServer(redis_host, redis_port, db=file_db)
        self.filter_list = refreshFilter().get_data()['all']
        self.suffix_list = []
        self.new_suffix = []
        self.new_file = []
        self.new_id = []
        self.new_path = []
        self.new_size = []
        self.new_ctime = []
        self.new_mtime = []

    def collect(self):
        for id, suffix, file, path, size, create_time, update_time in zip(self.cache_db.search_sql('id'),
                                                                          self.cache_db.search_sql('suffix'),
                                                                          self.cache_db.search_sql('filename'),
                                                                          self.cache_db.search_sql('path'),
                                                                          self.cache_db.search_sql("size"),
                                                                          self.cache_db.search_sql('create_time'),
                                                                          self.cache_db.search_sql('update_time')):
            self.new_id.append(str(id).strip("(',')"))
            self.new_suffix.append(str(suffix).strip("(',')"))
            self.new_file.append(str(file).strip("(',')"))
            self.new_path.append(str(path).strip("(',')"))
            self.new_size.append(str(size).strip("(',')"))
            self.new_ctime.append(str(create_time).strip("(',')"))
            self.new_mtime.append(str(update_time).strip("(',')"))

    def _zip_data(self) -> zip:
        return zip(self.new_id, self.new_suffix, self.new_file, self.new_path, self.new_size, self.new_ctime,
                   self.new_mtime)

    def filename_collect(self):
        for id, suffix, file, path, size, create_time, update_time in self._zip_data():
            if os.path.splitext(file)[1][1:] in self.filter_list:
                data = {
                    "indexID": id,
                    "suffix": suffix,
                    "filename": file,
                    "path": path,
                    "size": size,
                    "create_time": create_time,
                    "update_time": update_time
                }
                cache_db.push(file, data)
            else:
                continue


def RefreshIndex():
    new_index = createIndex()
    new_index.collect()
    Thread(target=new_index.filename_collect).start()
    cache_db.save()


if __name__ == "__main__":
    a = time.time()
    RefreshIndex()
    # new_index.suffix_collect()
    # new_index.filename_collect()
    print(time.time() - a)
