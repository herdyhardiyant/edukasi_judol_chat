from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship

class ChatSession(SQLModel, table=True):
    """
        Tabel yang menyimpan chat session setiap user untuk autentifikasi.
        User menyimpan Chat Session dalam bentuk cookie sebagai kredensial autentifikasi untuk mengakses riwayat chatnya dengan GPT
        Gunakan tabel ini untuk memeriksa cookie yang dimiliki user, jika cookie ada di dalam tabel, maka ia terautentifikasi.
        user_session merupakan string uuid4 yang akan dicocokkan dengan kode yg disimpan di cookie browser user
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_session: str = Field(unique=True, index=True)
    last_active_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    messages: list["ChatMessage"] = Relationship(back_populates="session")

class ChatMessage(SQLModel, table=True):
    """
        Tabel yang menyimpan riwayat prompt user beserta jawabannya dari GPT
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: Optional[int] = Field(default=None, foreign_key="chatsession.id")
    message_content: Optional[str]
    bot_answer: Optional[str]
    image_url: Optional[str] 
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    session: ChatSession = Relationship(back_populates="messages")
