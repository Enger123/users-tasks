from fastapi import HTTPException
from typing import List
from models import Task, NewTask, User, NewUser
from database import cur_tasks, cur_users, conn_tasks, conn_users

def get_tasks() -> List[Task]:
    cur_tasks.execute("SELECT * FROM tasks")
    tasks = cur_tasks.fetchall()
    return [Task(id=t[0], title=t[1], done=bool(t[2]), user_id=t[3]) for t in tasks]

def get_task_id(id: int) -> Task:
    cur_tasks.execute("SELECT * FROM tasks WHERE id = ?", (id, ))
    task = cur_tasks.fetchone()
    if not task:
        raise HTTPException(status_code=404, detail='Not found with this id')
    return Task(id=task[0], title=task[1], done=bool(task[2]), user_id=task[3])

def add_task(newtask: NewTask) -> Task:
    cur_tasks.execute("INSERT INTO tasks (title, done, user_id) VALUES (?, ?, ?)", (newtask.title, 0, newtask.user_id))
    conn_tasks.commit()
    new_id = cur_tasks.lastrowid
    return Task(id=new_id, title=newtask.title.capitalize(), done=False, user_id=newtask.user_id)

def get_users() -> List[User]:
    cur_users.execute("SELECT * FROM users")
    users = cur_users.fetchall()
    return [User(id=u[0], username=u[1]) for u in users]

def add_user(newuser: NewUser) -> User:
    cur_users.execute("INSERT INTO users (name, password) VALUES (?, ?)", (newuser.username, newuser.password))
    conn_users.commit()
    new_id = cur_users.lastrowid
    return User(id=new_id, username=newuser.username)
