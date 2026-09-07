from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey,DateTime,Text
from config.database import Base
from datetime import datetime

class LearningRecord(Base):
    __tablename__ = 'learning_record'
    id:Mapped[int]=mapped_column(
        Integer,
        primary_key=True
    )
    user_id:Mapped[int]=mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )
    title:Mapped[str]=mapped_column(
        String(255),
        nullable=False
    )
    content:Mapped[str]=mapped_column(
        Text,
        nullable=False
    )
    study_time:Mapped[int]=mapped_column(
        Integer,
        nullable=False
    )
    # Mapped[Python类型]=mapped_column(数据库类型)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )