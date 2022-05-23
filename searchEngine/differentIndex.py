import os
import time
from threading import Thread

from config.server import *
from searchEngine.RefreshFilters import refreshFilter
from sqlBase.redisDB import RedisServer
from sqlBase.sqlite import SQLiteDB


class createIndex(object):
    def __init__(self):
        self.cache_db = SQLiteDB(table=db_table, path=db)
        self.file_redis = RedisServer(redis_host, redis_port, db=file_db)
        self.filter_list = refreshFilter().get_data()['all']
        self.suffix_list = []
        self.new_suffix = []
        self.new_file = []
        self.new_id = []
        self.new_path = []

    def collect(self):
        for id, suffix, file, path in zip(self.cache_db.search_sql('id'), self.cache_db.search_sql('suffix'),
                                          self.cache_db.search_sql('filename'),
                                          self.cache_db.search_sql('path')):
            self.new_id.append(str(id).strip("(',')"))
            self.new_suffix.append(str(suffix).strip("(',')"))
            self.new_file.append(str(file).strip("(',')"))
            self.new_path.append(str(path).strip("(',')"))

    def _zip_data(self) -> zip:
        return zip(self.new_id, self.new_suffix, self.new_file, self.new_path)

    def filename_collect(self):
        for id, suffix, file, path in self._zip_data():
            if os.path.splitext(file)[1][1:] in self.filter_list:
                data = {
                    "indexID": id,
                    "suffix": suffix,
                    "filename": file,
                    "path": path
                }
                self.file_redis.push(file, data)
            else:
                continue


def RefreshIndex():
    new_index = createIndex()
    new_index.collect()
    _thread = Thread(target=new_index.filename_collect)
    _thread.start()


if __name__ == "__main__":
    a = time.time()
    RefreshIndex()
    # new_index.suffix_collect()
    # new_index.filename_collect()
    print(time.time() - a)