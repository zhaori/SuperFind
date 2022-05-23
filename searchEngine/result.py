import redis

from config.server import redis_host, redis_port

suffix_db = redis.StrictRedis(redis_host, redis_port, decode_responses=True, db=0, max_connections=10)
filename_db = redis.StrictRedis(redis_host, redis_port, decode_responses=True, db=1, max_connections=10)


def get_list_data(name):
    # 获取redis 列表数据
    list_count = filename_db.llen(name)
    for index in range(list_count):
        yield eval(filename_db.lindex(name, index))


if __name__ == "__main__":
    pass
