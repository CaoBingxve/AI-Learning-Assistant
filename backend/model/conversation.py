from datetime import datetime

from sqlalchemy import DateTime,ForeignKey, String,Text
from sqlalchemy.orm import Mapped,mapped_column,relationship

from config.database import Base

class Conversation(Base):
    """
    一次聊天会话。
    一个用户可以拥有多个 Conversation。
    """
    __tablename__ = 'conversation'
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="新对话"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )
    # delete-orphan：当一条消息从会话的 messages 列表中被移除（不再被任何会话引用），自动删除这条消息记录。
    messages: Mapped[list["ChatMessage"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan"#ORM层
    )

class ChatMessage(Base):
    """
        会话中的一条消息。
        role:
            user
            assistant
        """
    __tablename__ = 'chat_message'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    conversation_id: Mapped[str] = mapped_column(
        ForeignKey("conversation.id",ondelete="CASCADE"),#数据库层
        nullable=False,
        index=True
    )
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )

    conversation: Mapped["Conversation"] = relationship(
        back_populates="messages"
    )