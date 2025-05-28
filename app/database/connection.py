from sqlmodel import create_engine, SQLModel, Session
from sqlmodel import SQLModel, Session, select
from app.database.models import *
from typing import Annotated
from fastapi import Depends

sqlite_file_name = "database.sqlite"
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
                            bot_answer: str,
                              chat_session: ChatSession,
                              db_session: Session
                              ):
    """
    Buat pesan baru untuk chat session saat ini.
    Jika tidak ada chat session, maka buat chat session baru beserta dengan nilai user_session disimpan di cookie user.
    chat_session merupakan kredensial autentifikasi user untuk mengakses riwayat chatnya sendiri.
    """
    new_message = ChatMessage(
        message_content=message_content,
        session_id= chat_session.id,
        bot_answer=bot_answer
    )
    
    db_session.add(new_message)
    db_session.commit()
    db_session.refresh(new_message)
    return new_message

async def get_all_messages(chat_session: ChatSession, db_session: Session):
        """
        Mengambil semua riwayat pesan user saat ini.
        """
        message_statement = select(ChatMessage).where(ChatMessage.session == chat_session)
        messages = db_session.exec(message_statement).all()
        return messages

