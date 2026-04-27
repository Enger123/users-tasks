import sqlite3

conn_tasks = sqlite3.connect("tasks.db", check_same_thread=False)
cur_tasks = conn_tasks.cursor()
cur_tasks.execute("""CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    title text,
    done INTEGER,
    user_id INTEGER
)""")

conn_users = sqlite3.connect("users.db", check_same_thread=False)
cur_users = conn_users.cursor()
cur_users.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text,
    password text
)""")