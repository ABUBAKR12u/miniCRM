from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func
from app.database.Base import Base


class Activity(Base):
    __tablename__ = 'activities'
    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int]
    action: Mapped[str]
    detail: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())
