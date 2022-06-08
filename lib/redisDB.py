import redis


class RedisServer(object):

    def __init__(self, host=None, port=None, db=None, max_connection=None):
        self.host = host
        self.port = port
        if max_connection is None:
            self.max = 10
        self.r = redis.StrictRedis(self.host, self.port, decode_responses=True, db=db,
                                   max_connections=self.max)

    def key_in_data(self, key_set):
        """
        检查key是否是数据库里唯一存在
        return: True为存在，False 为不存在
        """
        return self.r.exists(key_set)

    def set(self, key, value, nx=None):
        """
        key: str
        return: 插入单条记录
        """
        self.r.set(key, value, nx)

    def set_all(self, value: dict):
        """
        批量插入数据
        """
        if type(value) != dict:
            raise Exception('The type only dict or json')
        else:
            return self.r.mset(value)

    def push(self, name, value):
        self.r.lpush(name, value)

    def delete(self, key):
        self.r.delete(key)

    def search(self, key):
        return eval(self.r.get(key))

    def key(self):
        # 返回所有键（所有数据库）
        all_key = []
        for i in range(0, self.max):
            all_key.append(redis.StrictRedis(host=self.host, port=self.port, decode_responses=True, db=i).keys())
        return all_key

    def update(self, old, new):
        """
        更新单条数据,根据key更新值
        """
        self.r.getset(old, new)

    def save(self):
        """
        内存数据本地持久化
        """
        self.r.save()

    def clean(self):
        """
        清除内存数据
        """
        self.r.flushall()


if __name__ == "__main__":
    r = RedisServer('127.0.0.1', 6379, db=0)
    r.clean()
    # r.set("data", data)
    # r.save()
    # dd = r.search("data")
    # for i in dd.keys():
    #    print(i)
    # print(list(data.keys())[0])
    # r.flush()
    # r.update('name', 'zg')
