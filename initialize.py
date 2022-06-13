from config.server import db, db_mode
from config.setting import select_task_file
from lib.sqlite import SQLiteDB
import os
import sqlite3

task_mode = f"""
                create table task (
                    [task_id] integer PRIMARY KEY AUTOINCREMENT,
                    task_name varchar(10),
                    task_path varchar(32),
                    begin_time varchar(8),
                    end_time varchar(8),
                    loop_time varchar(10)
                )
                 """

db_db = SQLiteDB(None, None, None, db)
try:
    db_db.submitSQL(db_mode)
    db_db.submitSQL(task_mode)
except sqlite3.OperationalError:
    pass
finally:
    db_db.com_clone()

os.system(f"type nul > {select_task_file}")
