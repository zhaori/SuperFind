"""
数据库的配置文件
"""
from pathlib import Path

# sqlite
db = Path.joinpath(Path(__file__).parent.parent, r".\data\Cache.db")
db_table = "cache"
db_mode = f"""
    create table {db_table}(
        [id] integer PRIMARY KEY AUTOINCREMENT,
        suffix varchar(10),
        filename varchar(120),
        path varchar(120),
        size text,
        ModificationDate integer(12)
    )
"""
db_sql = f"""
    insert into {db_table} (
        suffix, filename, path, size, ModificationDate
    ) values (:suffix, :filename, :path, :size, :ModificationDate)
"""

# redis 配置
redis_host = '127.0.0.1'
redis_port = 6379

# redis指定数据库存放
suffix_db = 0
file_db = 1
