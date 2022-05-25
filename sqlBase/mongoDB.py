import os

import pymongo


class MongodbServer(object):
    def __init__(self, host, port):
        # url_info = 'mongodb://{}:{}@{}:{}/{}'.format(db_name, db_password, host, port, db)
        try:
            self.server = pymongo.MongoClient(host, port, serverSelectionTimeoutMS=3000, socketTimeoutMS=3000)
        except:
            os.system('server restart mongodb')

    def insert(self, db, table, data):
        """
        :return: 插入单个数据
        """
        try:
            db_table = self.server[db][table]
            db_table.insert_one(data)
        except ValueError:
            raise ValueError

    def insert_list(self, db, table, data):
        """

        :param table:
        :param data:
        :return: 插入多条数据，以列表或者元组形式可迭代
        """
        try:
            db_table = self.server[db][table]
            db_table.insert(data)
        except ValueError:
            raise ValueError

    def search(self, data, table, key):
        """
        :param key: 格式例如：{"_id": 0, "username": 1},0为不查询，1为查询
        :return:
        """
        db_table = self.server[data][table]
        return [k for k in db_table.find({}, key)]

    def search_one(self, data, table, value):
        db_table = self.server[data][table]
        return db_table.find_one({}, value)

    def update(self, db, table, old, new):
        """
        old = {"username": "皮得狠1", "phone": "123456"}
        new = {"$set": {"username": "皮得狠1", "phone": "123456789"}}
        mycol.update_many(old, new)
        :param value:
        :return:
        """
        db_table = self.server[db][table]
        db_table.update_many(old, new)

    def delete(self, db, table, data):
        pass


if __name__ == "__main__":
    pass
    """
    data = {
        'username': 'pdh666',
        'password': ha_hash('666666'),
        'phone': '135xxxxxxx0410',
        'wx': '135xxxxxxx0410',
        'email': '1111@qq.com',
        'address': '四川成都市',
        'True_information': {
            'name': '皮得狠',
            'gender': '男',
            'age': '100',
            'nationality': '中华人民共和国',
            'ethnic_group': '汉',
            'id_address': ha_hash('四川省南充市'),
            'Identity_number': ha_hash('11132119906177111')

        }

    }
    """
    """
    from Lib.config.db_config import *

    db = Mongodb_server(host, port)
    name = db.search("User", "sys_info", {"_id": 0, "username": 1, "email": 1})
    for i in name:
        if i["username"] == "客户":
            print(type(i["email"]))
    """
