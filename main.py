from fastapi import FastAPI
import uvicorn, crud
from typing import List, Optional
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

#PUT TASKS
@app.put("/tasks/{id}", response_model=Task)
def change_task(id: int, newtask: NewTask) -> Task:
    return crud.change_task(id, newtask)

#DELETE TASKS
@app.delete("/tasks/{id}", response_model=List[Task])
def delete_task(id: int) -> List[Task]:
    return crud.delete_task(id)

#GET USERS
@app.get("/users", response_model=List[User])
def get_users() -> List[User]:
    return crud.get_users()

#GET USERS ID
@app.get("/users/{id}", response_model=User)
def get_user_id(id: int) -> User:
    return crud.get_user_id(id)

#POST USERS
@app.post("/users", response_model=User)
def add_user(newuser: NewUser) -> User:
    return crud.add_user(newuser)

#GET USERS ID TASK
@app.get("/users/{id}/tasks", response_model=List[Task])
def get_user_task(id: int) -> List[Task]:
    return crud.get_user_task(id)

@app.patch("/tasks/{id}/done", response_model=Task)
def change_done(id: int) -> Task:
    return crud.change_done(id)

@app.get("/tasks_user", response_model=List[Task])
def show_tasks(user_id: Optional[int] = None) -> List[Task]:
    return crud.show_tasks(user_id)

@app.get("/tasks_user_done", response_model=List[Task])
def show_filtered_task(user_id: Optional[int] = None, done: Optional[int|bool] = None) -> List[Task]:
    return crud.show_filtered_task(user_id, done)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)