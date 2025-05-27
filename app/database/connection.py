from sqlmodel import create_engine, SQLModel, Session
from sqlmodel import SQLModel, Session, select
from app.database.models import *
from typing import Annotated
from fastapi import Depends

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connection_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connection_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_database_session():
    with Session(engine) as session:
        yield session
        
SessionDependency = Annotated[Session, Depends(get_database_session)]

def create_chat_message(message_content: str,
                            is_user_message: bool,
                              chat_session: ChatSession,
                              db_session: Session
                              ):
    """
    Buat pesan baru untuk chat session saat ini.
    Jika tidak ada chat session, maka akan dibuat baru.
    """
    new_message = ChatMessage(
        message_content=message_content,
        session_id= chat_session.id,
        bot_answer=""
    )
    
    db_session.add(new_message)
    db_session.commit()
    db_session.refresh(new_message)
    return new_message

async def get_all_messages(chat_session: ChatSession, db_session: Session):
        """
        Mengambil semua pesan
        """
        message_statement = select(ChatMessage).where(ChatMessage.session_id == chat_session.id)
        messages = db_session.exec(message_statement).all()
        return messages

