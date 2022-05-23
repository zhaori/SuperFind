# import sqlite3
from config.server import db
from lib.tkcalendar import Calendar
from sqlBase.sqlite import SQLiteDB

db_table = "plan"
db_mode = f"""
    create table {db_table}(
        [plan_id] integer PRIMARY KEY AUTOINCREMENT,
        work_name varchar(10),
        begin_time varchar(8),
        end_time varchar(8),
        loop_time varchar(10)
    )
"""
db_sql = f"""
    insert into {db_table} (
        work_name, begin_time, end_time, loop_time
    ) values (:work_name, :begin_time, :end_time, :loop_time)
"""
get_db = SQLiteDB(db_table, db_mode, db_sql, db)
# get_db.insert(Calendar().run())
print(type(dict(Calendar().run())))
# get_db.com_clone()
