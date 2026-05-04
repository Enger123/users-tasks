import sqlite3

conn = sqlite3.connect("app.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    title text,
    done INTEGER,
    user_id INTEGER,
    created_at TEXT
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text,
    password text,
    created_at TEXT
)""")