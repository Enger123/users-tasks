from fastapi.params import Depends
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import cur
from models import UserInDB, TokenData, User
from fastapi import HTTPException, status
from datetime import datetime, timedelta

SECRET_KEY = "61810af68f485d54724418eb0c231b8a9e7b17b65f5bbce4118cdcb629615583"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def get_user(username: str):
    cur.execute("SELECT * FROM users WHERE name = ?", (username, ))
    return cur.fetchone()

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user[2]):
        return False
    return user

def create_access_token(data:dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth_2_scheme)):
    credential_exc = HTTPException(status_code=401, detail='Invalid login or password')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credential_exc
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exc
    user = get_user(username = token_data.username)
    if user is None:
        raise credential_exc
    return User(id=user[0], username=user[1], created=user[3])

def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid login or password')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({'sub': user[1]}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}
