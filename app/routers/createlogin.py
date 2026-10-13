from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated
from app.database.connection import get_db
from app.models.Login import Login
from app.scheme.Login import AddLogin
from app.utils.securty import get_current_user, hash_password

router = APIRouter(prefix="/create_login", tags=["Create Login"])


@router.post("/newlogin")
def create_login(db:Annotated[Session, Depends(get_db)] , data:AddLogin ,current_user=Depends(get_current_user)):
    user= db.execute(select(Login).where(Login.username == data.username)).scalars().first()
    if user:
        raise HTTPException(status_code=400 , detail="Username already exists")
    if current_user.role!="boss":
        raise HTTPException(status_code=405 , detail="method not allowed")
    obj = Login(
        username=data.username,
        password=hash_password(data.password)
    )
    db.add(obj)
    db.commit()
    return {"msg":"new login created"}



