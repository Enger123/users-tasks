from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str

class NewUser(BaseModel):
    username: str
    password: str

class Task(BaseModel):
    id: int
    title: str
    done: bool
    user_id: int

class NewTask(BaseModel):
    title: str
    user_id: int