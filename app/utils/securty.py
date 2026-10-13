from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from typing import Annotated

from app.database.connection import get_db
from app.models.Login import Login

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

connects=Annotated[Session, Depends(get_db)]

pwd_context = CryptContext(schemes=["argon2"])

def hash_password(password):
    return pwd_context.hash(password)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id):
    user_data = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=60),
        "type": "access"
    }
    return jwt.encode(user_data, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id):
    user_data = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=60),
        "type": "refresh"
    }
    return jwt.encode(user_data, SECRET_KEY, algorithm=ALGORITHM)

def new_access_token(user_data):
    try:
        payload = jwt.decode(user_data, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["type"] != "refresh":
            raise HTTPException(400 , "Invalid refresh token")
        user_id = payload["user_id"]
        new_access_token = create_access_token(user_id)
        return new_access_token
    except JWTError:
        raise HTTPException(401 , "unauthorized")


bearer=HTTPBearer()


def get_current_user(db:connects, token: str = Depends(bearer)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["type"] != "access":
            raise HTTPException(400 , "Token is not valid")
        user_id = payload["user_id"]
        user=db.get(Login , user_id)
        if not user:
            raise HTTPException(404 , "user not exist")
        return user
    except JWTError:
        raise HTTPException(401 , "unauthorized")