from lib.sqlite import *
from tinydb import TinyDB, Query


class SaveTask(object):

    def __init__(self, db_name):
        self.db_name = db_name
        self.task_table = 'task'
        self.task_mode = f"""
                    create table {self.task_table}(
                        [task_id] integer PRIMARY KEY AUTOINCREMENT,
                        task_name varchar(10),
                        task_path varchar(32),
                        begin_time varchar(8),
                        end_time varchar(8),
                        loop_time varchar(10)
                    )
                     """
        self.task_sql = f"""
                    insert into {self.task_table} (
                       task_name, task_path, begin_time, end_time, loop_time
                    ) values (:task_name, :task_path, :begin_time, :end_time, :loop_time)
                     """

        self.task_db = SQLiteDB(self.task_table, self.task_mode, self.task_sql, self.db_name)

    def insert(self, data):
        self.task_db.insert(data)

    def delete(self, table):
        self.task_db.null_table(table)

    def delete_data(self, key, value):
        self.task_db.delete(key, value)

    def query(self, exp):
        return self.task_db.search_sql(exp)

    def query_all(self, table, key, value):
        return self.task_db.search_key_all(table, key, value)

    def query_joint(self, exp):
        return self.task_db.search_id(exp, 'task_id')

    def submit(self):
        self.task_db.com_clone()


class AddFavorite(object):
    def __init__(self, favorite_db='./data/Favorites.json'):
        self.favorite_table = 'favorites'
        self.favorite_db = favorite_db
        self.json_db = TinyDB(self.favorite_db)
        self.db_query = Query()
        try:
            self.table = self.json_db.table('favorite')
        except:
            pass

    def insert(self, data):
        self.table.insert(data)

    def query(self, key, value):
        return self.table.search(self.db_query[key] == f'{value}')

    def search(self):
        return self.table.all()

    def delete(self, key, value):
        self.table.remove(self.db_query[key] == f'{value}')

    def submit(self):
        self.json_db.close()


if __name__ == "__main__":
    db = AddFavorite('../data/Favorites.json')
    # db.insert({"task_id": int(4)})
    db.query('filename','docx')
    # db.submit()
    # print(db.query_joint('task_name="查找E盘"'))
