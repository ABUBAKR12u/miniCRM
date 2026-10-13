from sqlalchemy.orm import Mapped , mapped_column
from app.database.Base import Base

class Login(Base):
    __tablename__ = 'Login'
    id: Mapped[int]=mapped_column(primary_key=True)
    username:Mapped[str]
    password:Mapped[str]
    role:Mapped[str]=mapped_column(default="user")
