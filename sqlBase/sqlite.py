import sqlite3
from io import StringIO


class SQLiteDB(object):

    def __init__(self, table=None, mode=None, sql=None, path=None):
        self.table = table  # 表名
        self.mode = mode  # 插入表
        self.sql = sql  # 插入数据
        self.dbpath = path  # 数据库存储路径

        try:
            self.con = sqlite3.connect(self.dbpath, timeout=1)
            self.cur = self.con.cursor()
        except sqlite3.OperationalError:
            raise '未找到SQLite数据库或者无法打开'

    def com_clone(self):
        # 提交事务及关闭数据库连接
        self.con.commit()
        self.con.close()

    def new_sql(self):
        # 数据库创建、插入表
        # md是model.py里的模板
        self.cur.execute(self.mode)
        self.con.commit()
        # 捕获SQLite数据库 table datafile already exists

    def insert(self, add_data: dict):
        """
        增添数据
        这里将提交事务及关闭数据库连接的方法另写为com_clone
        如果是往数据库批量写入数据，如外部结构是for循环，能够极大提高数据存储效率
        经测试，往数据库写入2108条记录，1.0176119804382324
        """
        # cn = self.con.cursor()
        self.cur.execute(self.sql, add_data)

    def delete(self, element):
        # 删除表里的某一项数据table,element
        # with sqlite3.connect(self.dbpath):
        self.cur.execute(f"delete from {self.table} where {element}")

    def delete_table(self, table_name):
        # 删除表
        with sqlite3.connect(self.dbpath) as con:
            con.execute(f"drop table {table_name}")

    def tables(self):
        # 查询表
        # sqlite_sequence是SQLite数据库一张隐含的表，表字段就是数据库里所有的表名称
        with sqlite3.connect(self.dbpath) as con:
            sql_table = con.execute("select name from sqlite_sequence")
            return sql_table.fetchall()

    def search_key(self, table_name):
        # 查表字段
        with sqlite3.connect(self.dbpath) as con:
            k = con.execute(f'select * from {table_name}')
            key_name_list = [data[0] for data in k.description]
            return key_name_list

    def search_sql(self, query):
        # query 输入查询的字段，多个字段用,分开，如 'name, password, arg'
        # 查询数据
        with sqlite3.connect(self.dbpath) as con:
            sql_data = con.execute(
                f"select {query} from {self.table}")
        return sql_data.fetchall()

    def search_sql_id(self, id, query=None):
        # query 输入查询的字段，多个字段用,分开，如 'name, password, arg'
        # 查询数据
        if query is None:
            query = '*'
        with sqlite3.connect(self.dbpath) as con:
            sql_data = con.execute(
                f"select {query} from {self.table} where id={id}")
        return sql_data.fetchall()

    def update(self, table, value, data, id):
        # 更新数据
        with sqlite3.connect(self.dbpath) as con:
            con.execute(f"update {table} set {value} = '{data}' where id = {id}")
            # con.execute('update pwd set username = "zzg" where id = 1')


class memoryDB(object):
    def __init__(self, table, mode, sql, path):
        self.table = table
        self.mode = mode
        self.sql = sql
        self.dbpath = path
        self.con = sqlite3.connect(":memory:")

    def new_table(self):
        try:
            self.con.execute(self.mode)
            self.con.commit()
        except sqlite3.OperationalError:
            pass

    def insert(self, add_data: dict):
        self.con.execute(self.sql, add_data)

    def tables(self):
        self.con.execute(f"select * from {self.table}").fetchall()

    def save(self):
        self.tables()
        str_buffer = StringIO()
        for line in self.con.iterdump():
            str_buffer.write('%s\n' % line)
        self.con.close()
        con_file = sqlite3.connect(self.dbpath)
        cur_file = con_file.cursor()
        # 执行内存数据库脚本
        cur_file.executescript(str_buffer.getvalue())
        cur_file.close()


'''class memoryDB(object):
    def __init__(self, table, mode, sql, path):
        self.table = table
        self.mode = mode
        self.sql = sql
        self.db = path
        self.con = sqlite3.connect(":memory:")
        self.cur = self.con.cursor()
        self.memory = StringIO()

    def memory_script(self, data: list):
        self.cur.execute(self.mode)
        for i in data:
            self.cur.execute(self.sql, i)
    """def get_script(self):
        self.cur.execute(f"select * from {self.table}")
        self.cur.fetchall()"""

    def new(self):
        self.cur.execute(f"select * from {self.table}")
        self.cur.fetchall()

        for line in self.con.iterdump():
            self.memory.write('%s\n' % line)
        self.cur.close()
        con_file = sqlite3.connect(self.db)
        cur_file = con_file.cursor()
        # 执行内存数据库脚本
        cur_file.executescript(self.memory.getvalue())
        cur_file.close()
'''

"""def memory_db(table, mode, sql, data: dict, db):
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute(mode)
    cur.execute(sql, data)
    cur.execute(f"select * from {table}")
    cur.fetchall()
    str_buffer = StringIO()
    for line in con.iterdump():
        str_buffer.write('%s\n' % line)
    cur.close()
    con_file = sqlite3.connect(db)
    cur_file = con_file.cursor()
    # 执行内存数据库脚本
    cur_file.executescript(str_buffer.getvalue())
    cur_file.close()"""


def str_to_tuple(n):
    # 这个函数是处理从数据库读取字段后将列表格式转化为元祖用于读取
    return tuple(eval(str(n).strip('[]')))


def list_to_str(n):
    # 适用于[('xxxxxxx',), ('xxxxx',),]
    return str(n).strip('()')[:-1].strip(" '' ")
