from fastapi import HTTPException
from typing import List, Optional
from models import Task, NewTask, User, NewUser
from database import cur, conn
from datetime import datetime

def check_user(newtask: NewTask):
    cur.execute("SELECT id FROM users WHERE id = ?", (newtask.user_id, ))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="User not found")

def fetch_tasks() -> List[Task]:
    tasks = cur.fetchall()  # 3
    return [Task(id=t[0], title=t[1], done=bool(t[2]), user_id=t[3], created=t[4]) for t in tasks]

def fetch_task(task) -> Task:
    return Task(id=task[0], title=task[1], done=bool(task[2]), user_id=task[3], created=task[4])

def get_tasks(user_id: Optional[int] = None, done: Optional[bool] = None, sort: str = None, limit: Optional[int] = None, title: Optional[str] = None) -> List[Task]:
    query = "SELECT * FROM tasks" #1
    filters = []
    params = []
    order = None
    if user_id is not None:
        filters.append("user_id = ?")
        params.append(user_id)
    if done is not None:
        filters.append("done = ?")
        params.append(int(done))
    if title:
        filters.append("title LIKE ?")
        params.append(f"%{title}%")
    if filters:
        query += ' WHERE ' + ' AND '.join(filters) #2
    if sort in ('asc', 'desc'):
        if sort == 'asc':
            order = 'ASC'
        elif sort == 'desc':
            order = 'DESC'
        query += f" ORDER BY id {order}"
    if limit is not None:
        query += f" LIMIT ?"
        params.append(limit)
    cur.execute(query, tuple(params))
    return fetch_tasks()

def get_task_id(id: int) -> Task:
    cur.execute("SELECT * FROM tasks WHERE id = ?", (id, ))
    task = cur.fetchone()
    if not task:
        raise HTTPException(status_code=404, detail='Nothing found with this id')
    return fetch_task(task)

def add_task(newtask: NewTask) -> Task:
    check_user(newtask)
    cur.execute("INSERT INTO tasks (title, done, user_id, created_at) VALUES (?, ?, ?, ?)", (newtask.title, 0, newtask.user_id, datetime.now()))
    conn.commit()
    new_id = cur.lastrowid
    return Task(id=new_id, title=newtask.title, done=False, user_id=newtask.user_id, created=str(datetime.now()))

def change_task(id: int, newtask: NewTask) -> Task:
    check_user(newtask)
    cur.execute("UPDATE tasks SET title = ?, user_id = ? WHERE id = ?", (newtask.title, newtask.user_id, id))
    conn.commit()
    cur.execute("SELECT * FROM tasks WHERE id = ?", (id, ))
    t = cur.fetchone()
    if not t:
        raise HTTPException(status_code=404, detail='Nothing found with this id')
    return fetch_task(t)

def delete_task(id: int) -> List[Task]:
    cur.execute("DELETE FROM tasks WHERE id = ?", (id, ))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail='Task not found')
    cur.execute("SELECT * FROM tasks")
    return fetch_tasks()

def get_users() -> List[User]:
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    return [User(id=u[0], username=u[1], created=u[3]) for u in users]

def get_user_id(id: int) -> User:
    cur.execute("SELECT id, name, created_at FROM users WHERE id = ?", (id, ))
    user_info = cur.fetchone()
    if not user_info:
        raise HTTPException(status_code=404, detail='Nothing found')
    return User(id=user_info[0], username=user_info[1], created=user_info[2])

def add_user(newuser: NewUser) -> User:
    cur.execute("SELECT name FROM users WHERE name = ?", (newuser.username, ))
    if cur.fetchone():
        raise HTTPException(status_code=400, detail='There is a user with this username')
    cur.execute("INSERT INTO users (name, password, created_at) VALUES (?, ?, ?)", (newuser.username, newuser.password, datetime.now()))
    conn.commit()
    new_id = cur.lastrowid
    return User(id=new_id, username=newuser.username, created=str(datetime.now()))

def get_user_task(user_id: int, done: Optional[bool] = None) -> List[Task]:
    cur.execute("SELECT id FROM users WHERE id = ?", (user_id, ))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail='User not found')
    if done is None:
        cur.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id, ))
    else:
        cur.execute("SELECT * FROM tasks WHERE user_id = ? AND done = ?", (user_id, int(done)))
    return fetch_tasks()

def change_done(id: int) -> Task:
    cur.execute("SELECT id, done FROM tasks WHERE id = ?", (id, ))
    task = cur.fetchone()
    if not task:
        raise HTTPException(status_code=404, detail='Nothing found with this id')
    new_done = 1 if task[1] == 0 else 0
    cur.execute("UPDATE tasks SET done = ? WHERE id = ?", (new_done, id))
    conn.commit()
    cur.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    task = cur.fetchone()
    return fetch_task(task)


