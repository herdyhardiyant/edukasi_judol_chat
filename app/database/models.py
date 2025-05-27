from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship

class ChatSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_session: str = Field(unique=True, index=True)
    last_active_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    messages: list["ChatMessage"] = Relationship(back_populates="session")

class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: Optional[int] = Field(default=None, foreign_key="chatsession.id")
    message_content: str
    bot_answer: Optional[str]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    session: ChatSession = Relationship(back_populates="messages")
