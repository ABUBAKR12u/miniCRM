from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated
from app.database.connection import get_db
from app.models.Login import Login
from app.scheme.Login import AddLogin
from app.utils.securty import get_current_user, hash_password

router = APIRouter(prefix="/create_login", tags=["Create Login"])

connect = Annotated[Session, Depends(get_db)]


@router.post("/newlogin")
def create_login(db: connect, data: AddLogin, current_user=Depends(get_current_user)):
    if current_user.role != "boss":
        raise HTTPException(status_code=405, detail="method not allowed")
    if data.role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="role must be admin or user")
    user = db.execute(select(Login).where(Login.username == data.username)).scalars().first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    obj = Login(
        username=data.username,
        password=hash_password(data.password),
        role=data.role
    )
    db.add(obj)
    db.commit()
    return {"msg": "new login created"}


@router.get("/users")
def list_users(db: connect, current_user=Depends(get_current_user)):
    if current_user.role != "boss":
        raise HTTPException(status_code=405, detail="method not allowed")
    users = db.execute(select(Login).order_by(Login.id)).scalars().all()
    return [{"id": u.id, "username": u.username, "role": u.role} for u in users]


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: connect, current_user=Depends(get_current_user)):
    if current_user.role != "boss":
        raise HTTPException(status_code=405, detail="method not allowed")
    user = db.get(Login, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="cannot delete yourself")
    db.delete(user)
    db.commit()
    return {"msg": "user deleted"}
