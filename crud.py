from fastapi import HTTPException
from typing import List, Optional
from auth import hash_password
from models import Task, NewTask, User, NewUser, UpdateTask
from database import cur, conn
from datetime import datetime

def fetch_tasks() -> List[Task]:
    tasks = cur.fetchall()  # 3
    return [Task(id=t[0], title=t[1], done=bool(t[2]), user_id=t[3], created=t[4]) for t in tasks]

def fetch_task(task) -> Task:
    return Task(id=task[0], title=task[1], done=bool(task[2]), user_id=task[3], created=task[4])

def get_tasks(current_user: User, done: Optional[bool] = None, sort: str = None, limit: Optional[int] = None, title: Optional[str] = None) -> List[Task]:
    query = "SELECT * FROM tasks" #1
    filters = []
    params = []
    order = None
    filters.append("user_id = ?")
    params.append(current_user.id)
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

def get_task_id(id: int, current_user: User) -> Task:
    cur.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", (id, current_user.id))
    task = cur.fetchone()
    if not task:
        raise HTTPException(status_code=404, detail='Nothing found with this id')
    return fetch_task(task)

def add_task(newtask: NewTask, current_user: User) -> Task:
    cur.execute("INSERT INTO tasks (title, done, user_id, created_at) VALUES (?, ?, ?, ?)", (newtask.title, 0, current_user.id, datetime.now()))
    conn.commit()

    new_id = cur.lastrowid
    return Task(id=new_id, title=newtask.title, done=False, user_id=current_user.id, created=str(datetime.now()))

def change_task(id: int,  newtask: UpdateTask, current_user: User) -> Task:
    cur.execute("UPDATE tasks SET title = ? WHERE id = ? and user_id = ?", (newtask.title, id, current_user.id))
    conn.commit()
    cur.execute("SELECT * FROM tasks WHERE id = ?", (id, ))
    t = cur.fetchone()
    if not t:
        raise HTTPException(status_code=404, detail='Nothing found with this id')
    return fetch_task(t)

def delete_task(id: int, current_user: User) -> List[Task]:
    cur.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (id, current_user.id))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail='Task not found')
    cur.execute("SELECT * FROM tasks WHERE user_id = ?", (current_user.id, ))
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
    cur.execute("INSERT INTO users (name, hashed_password, created_at) VALUES (?, ?, ?)", (newuser.username, hash_password(newuser.password), datetime.now()))
    conn.commit()
    new_id = cur.lastrowid
    return User(id=new_id, username=newuser.username, created=str(datetime.now()))

def get_user_task(current_user: User, done: Optional[bool] = None) -> List[Task]:
    if done is None:
        cur.execute("SELECT * FROM tasks WHERE user_id = ?", (current_user.id, ))
    else:
        cur.execute("SELECT * FROM tasks WHERE user_id = ? AND done = ?", (current_user.id, int(done)))
    return fetch_tasks()

def change_done(id: int, current_user: User) -> Task:
    cur.execute("SELECT done FROM tasks WHERE id = ? AND user_id = ?", (id, current_user.id))
    task = cur.fetchone()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    new_done = 1 if task[0] == 0 else 0
    cur.execute("UPDATE tasks SET done = ? WHERE id = ? AND user_id = ?", (new_done, id, current_user.id))
    conn.commit()
    cur.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", (id, current_user.id))
    changed_task = cur.fetchone()
    return fetch_task(changed_task)

def get_user_by_username(username) -> User:
    cur.execute("SELECT id, name, created_at FROM users WHERE name = ?", (username, ))
    user = cur.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return User(id=user[0], username=user[1], created=user[2])

def profile(current_user: User):
    return current_user

def my_tasks(current_user: User) -> List[Task]:
    cur.execute("SELECT * FROM tasks WHERE user_id = ?", (current_user.id, ))
    return fetch_tasks()

def completed_tasks(current_user: User) -> List[Task]:
    cur.execute("SELECT * FROM tasks WHERE user_id = ? AND done = ?", (current_user.id, 1))
    return fetch_tasks()



