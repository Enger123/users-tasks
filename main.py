from fastapi import FastAPI
import uvicorn, crud
from typing import List
from models import Task, NewTask, User, NewUser

app = FastAPI()

#GET TASKS
@app.get("/tasks", response_model=List[Task])
def get_tasks() -> List[Task]:
    return crud.get_tasks()

#GET TASK ID
@app.get("/tasks/{id}", response_model=Task)
def get_task_id(id: int) -> Task:
    return crud.get_task_id(id)

#POST TASKS
@app.post("/tasks", response_model=Task)
def add_task(newtask: NewTask) -> Task:
    return crud.add_task(newtask)

#GET USERS
@app.get("/users", response_model=List[User])
def get_users() -> List[User]:
    return crud.get_users()

#POST USERS
@app.post("/users", response_model=User)
def add_user(newuser: NewUser) -> User:
    return crud.add_user(newuser)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)