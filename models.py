from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    created: str

class NewUser(BaseModel):
    username: str
    password: str

class Task(BaseModel):
    id: int
    title: str
    done: bool
    user_id: int
    created: str

class NewTask(BaseModel):
    title: str

class UpdateTask(BaseModel):
    title: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserInDB(BaseModel):
    hashed_password: str
