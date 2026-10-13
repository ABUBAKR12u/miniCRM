from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String, func
from app.database.Base import Base


class Activity(Base):
    __tablename__ = 'activities'
    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int]
    action: Mapped[str] = mapped_column(String(100))
    detail: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())
