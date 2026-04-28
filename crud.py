from fastapi import HTTPException
from typing import List
from models import Task, NewTask, User, NewUser
from database import cur, conn

def get_tasks() -> List[Task]:
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    return [Task(id=t[0], title=t[1], done=bool(t[2]), user_id=t[3]) for t in tasks]

def get_task_id(id: int) -> Task:
    cur.execute("SELECT * FROM tasks WHERE id = ?", (id, ))
    task = cur.fetchone()
    if not task:
        raise HTTPException(status_code=404, detail='Not found with this id')
    return Task(id=task[0], title=task[1], done=bool(task[2]), user_id=task[3])

def add_task(newtask: NewTask) -> Task:
    cur.execute("SELECT id FROM users WHERE id = ?", (newtask.user_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="User not found")
    cur.execute("INSERT INTO tasks (title, done, user_id) VALUES (?, ?, ?)", (newtask.title, 0, newtask.user_id))
    conn.commit()
    new_id = cur.lastrowid
    return Task(id=new_id, title=newtask.title, done=False, user_id=newtask.user_id)

def change_task(id: int, newtask: NewTask) -> Task:
    cur.execute("UPDATE tasks SET title = ?, done = ?, user_id = ? WHERE id = ?", (newtask.title, int(newtask.done), newtask.user_id, id))
    conn.commit()
    cur.execute("SELECT * FROM tasks WHERE id = ?", (id, ))
    t = cur.fetchone()
    if not t:
        raise HTTPException(status_code=404, detail='Nothing found')
    return Task(id=t[0], title=t[1], done=bool(t[2]), user_id=t[3])

def delete_task(id: int) -> List[Task]:
    cur.execute("DELETE FROM tasks WHERE id = ?", (id, ))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail='Task not found')
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    return [Task(id=t[0], title=t[1], done=bool(t[2]), user_id=t[3]) for t in tasks]

def get_users() -> List[User]:
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    return [User(id=u[0], username=u[1]) for u in users]

def get_user_id(id: int) -> User:
    cur.execute("SELECT id, name FROM users WHERE id = ?", (id, ))
    user_info = cur.fetchone()
    if not user_info:
        raise HTTPException(status_code=404, detail='Nothing found')
    return User(id=user_info[0], username=user_info[1])

def add_user(newuser: NewUser) -> User:
    cur.execute("INSERT INTO users (name, password) VALUES (?, ?)", (newuser.username, newuser.password))
    conn.commit()
    new_id = cur.lastrowid
    return User(id=new_id, username=newuser.username)

def get_user_task(user_id: int) -> List[Task]:
    cur.execute("SELECT id FROM users WHERE id = ?", (user_id, ))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail='User not found')
    cur.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id, ))
    tasks = cur.fetchall()
    return [Task(id=t[0], title=t[1], done=bool(t[2]), user_id=t[3]) for t in tasks]
