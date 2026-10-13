from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from typing import Annotated
from app.database.connection import get_db
from app.models.Lead import Lead
from app.scheme.Lead import DashboardResponse
from app.utils.securty import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

connect = Annotated[Session, Depends(get_db)]


@router.get("/stats", response_model=DashboardResponse)
def get_stats(db: connect, current_user=Depends(get_current_user)):
    total = db.execute(select(func.count()).select_from(Lead)).scalar()
    new = db.execute(select(func.count()).select_from(Lead).where(Lead.status == "New")).scalar()
    contacted = db.execute(select(func.count()).select_from(Lead).where(Lead.status == "Contacted")).scalar()
    qualified = db.execute(select(func.count()).select_from(Lead).where(Lead.status == "Qualified")).scalar()
    won = db.execute(select(func.count()).select_from(Lead).where(Lead.status == "Won")).scalar()
    lost = db.execute(select(func.count()).select_from(Lead).where(Lead.status == "Lost")).scalar()

    return DashboardResponse(
        total=total,
        new=new,
        contacted=contacted,
        qualified=qualified,
        won=won,
        lost=lost
    )
