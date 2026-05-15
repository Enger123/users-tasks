from fastapi import FastAPI
from fastapi.params import Depends
import crud
from typing import List, Optional

import auth
from models import Task, NewTask, User, NewUser, UpdateTask, Token
from fastapi.security import OAuth2PasswordRequestForm
from auth import get_current_user
app = FastAPI()

#GET TASKS
@app.get("/tasks", response_model=List[Task])
def get_tasks(current_user: User = Depends(get_current_user), done: Optional[bool] = None, sort: str = None, limit: Optional[int] = None, title: Optional[str] = None) -> List[Task]:
    return crud.get_tasks(current_user, done, sort, limit, title)

#GET TASK ID
@app.get("/tasks/{id}", response_model=Task)
def get_task_id(id: int, current_user: User=Depends(get_current_user)) -> Task:
    return crud.get_task_id(id, current_user)

#POST TASKS
@app.post("/tasks", response_model=Task)
async def add_task(newtask: NewTask, current_user: User=Depends(get_current_user)) -> Task:
    return crud.add_task(newtask, current_user)

#PUT TASKS
@app.put("/tasks/{id}", response_model=Task)
def change_task(id: int, newtask: UpdateTask, current_user: User=Depends(get_current_user)) -> Task:
    return crud.change_task(id, newtask, current_user)

#DELETE TASKS
@app.delete("/tasks/{id}", response_model=List[Task])
def delete_task(id: int, current_user: User=Depends(get_current_user)) -> List[Task]:
    return crud.delete_task(id, current_user)

#GET USERS
@app.get("/users", response_model=List[User])
def get_users() -> List[User]:
    return crud.get_users()

@app.get("/users/find/{id}", response_model=User)
def get_user_id(id: int) -> User:
    return crud.get_user_id(id)

#POST USERS
@app.post("/users", response_model=User)
def add_user(newuser: NewUser) -> User:
    return crud.add_user(newuser)

#GET USERS ID TASK
@app.get("/users/{id}/tasks", response_model=List[Task])
def get_user_task(current_user: User=Depends(get_current_user), done: Optional[bool] = None) -> List[Task]:
    return crud.get_user_task(current_user, done)

@app.patch("/tasks/{id}/done", response_model=Task)
def change_done(id: int, current_user: User=Depends(get_current_user)) -> Task:
    return crud.change_done(id, current_user)

@app.get("/users/by-username/{username}", response_model=User)
def get_user_by_username(username) -> User:
    return crud.get_user_by_username(username)

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends()):
    return auth.login_for_access_token(form_data)

@app.get("/profile")
def profile(current_user: User=Depends(get_current_user)):
    return crud.profile(current_user)

@app.get("/my-tasks", response_model=List[Task])
def my_tasks(current_user: User=Depends(get_current_user)) -> List[Task]:
    return crud.my_tasks(current_user)

@app.get("/completed-tasks", response_model=List[Task])
def completed_tasks(current_user: User=Depends(get_current_user)) -> List[Task]:
    return crud.completed_tasks(current_user)




