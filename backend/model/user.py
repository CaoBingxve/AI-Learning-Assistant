from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from config.database import Base

class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(
        Integer,
        primary_key=True
    )
    username:Mapped[str]=mapped_column(
        String(20),
        unique=True,
        nullable=False
    )
    password_hash:Mapped[str]=mapped_column(
        String(255),
        nullable=False
    )