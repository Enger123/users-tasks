from fastapi import HTTPException
from typing import List, Optional
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
    cur.execute("SELECT id FROM users WHERE id = ?", (newtask.user_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail='User not found')
    cur.execute("UPDATE tasks SET title = ?, user_id = ? WHERE id = ?", (newtask.title, newtask.user_id, id))
    conn.commit()
    cur.execute("SELECT * FROM tasks WHERE id = ?", (id, ))
    t = cur.fetchone()
    if not t:
        raise HTTPException(status_code=404, detail='Nothing found with this id')
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
    cur.execute("SELECT name FROM users WHERE name = ?", (newuser.username, ))
    if cur.fetchone():
        raise HTTPException(status_code=404, detail='There is a user with this username')
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

def change_done(id: int) -> Task:
    cur.execute("SELECT id, done FROM tasks WHERE id = ?", (id, ))
    task = cur.fetchone()
    if not task:
        raise HTTPException(status_code=404, detail='Nothing found with this id')
    new_done = 1 if task[1] == 0 else 0
    cur.execute("UPDATE tasks SET done = ? WHERE id = ?", (new_done, id))
    cur.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    task = cur.fetchone()
    return Task(id=task[0], title=task[1], done=bool(task[2]), user_id=task[3])

def show_tasks(user_id: Optional[int] = None) -> List[Task]:
    if user_id is None:
        cur.execute("SELECT * FROM tasks")
        tasks = cur.fetchall()
        return [Task(id=t[0], title=t[1], done=bool(t[2]), user_id=t[3]) for t in tasks]
    cur.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id, ))
    tasks = cur.fetchall()
    return [Task(id=t[0], title=t[1], done=bool(t[2]), user_id=t[3]) for t in tasks]

def check_user_id(user_id: int):
    cur.execute("SELECT id FROM users WHERE id = ?", (user_id, ))
    user = cur.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

def show_filtered_task(user_id: Optional[int] = None, done: Optional[bool] = None) -> List[Task]:
    if user_id is None and done is None:
        cur.execute("SELECT * FROM tasks")
        tasks = cur.fetchall()
        return [Task(id=t[0], title=t[1], done=bool(t[2]), user_id=t[3]) for t in tasks]
    elif user_id is not None and done is None:
        check_user_id(user_id)
        cur.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id, ))
        tasks = cur.fetchall()
        return [Task(id=t[0], title=t[1], done=bool(t[2]), user_id=t[3]) for t in tasks]
    elif user_id is None and done is not None:
        cur.execute("SELECT * FROM tasks WHERE done = ?", (int(done),))
        tasks = cur.fetchall()
        return [Task(id=t[0], title=t[1], done=bool(t[2]), user_id=t[3]) for t in tasks]
    check_user_id(user_id)
    cur.execute("SELECT * FROM tasks WHERE user_id = ? AND done = ?", (user_id, int(done)))
    tasks = cur.fetchall()
    return [Task(id=t[0], title=t[1], done=bool(t[2]), user_id=t[3]) for t in tasks]
