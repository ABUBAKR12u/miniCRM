from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import String
from app.database.Base import Base

class Login(Base):
    __tablename__ = 'Login'
    id: Mapped[int]=mapped_column(primary_key=True)
    username:Mapped[str]=mapped_column(String(100))
    password:Mapped[str]=mapped_column(String(255))
    role:Mapped[str]=mapped_column(String(20),default="user")
