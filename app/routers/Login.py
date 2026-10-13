from os import access

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated
from app.database.connection import get_db
from app.models.Login import Login
from app.scheme.Login import AddLogin, RefreshToken, ResponseLogin
from app.utils.securty import verify_password, create_access_token, create_refresh_token, new_access_token, \
    get_current_user

router = APIRouter(prefix="/login",tags=["login"])

connect=Annotated[Session, Depends(get_db)]

@router.post("/login")
def create_login(request: Request,data:AddLogin, db: connect):
    user = db.execute(select(Login).where(Login.username == data.username)).scalars().first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(401, "Invalid username or password")
    access_token=create_access_token(user.id)
    refresh_token=create_refresh_token(user.id)

    return {"access_token":access_token,
            "refresh_token":refresh_token}

@router.post("/refresh")
def new_token(data:RefreshToken, db: connect):
    return new_access_token(data.access_token)

@router.get("/me", response_model=ResponseLogin)
def get_me(current_user=Depends(get_current_user)):
    return current_user