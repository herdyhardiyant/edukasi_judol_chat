
from sqlmodel import Session, select
from app.database.connection import engine
from app.database.models import ChatSession
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

 
class SessionAuthMiddleware(BaseHTTPMiddleware):
    user_session_key_name = "user_session_id"

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        chat_session = self._get_chat_session(request, self.user_session_key_name)
        
        request.state.chat_session = None
        
        if chat_session:
            request.state.chat_session = chat_session
        
        response: Response = await call_next(request)
        
        if not chat_session:
            new_session_uuid = self._create_new_chat_session_to_db()
            response.set_cookie(key=self.user_session_key_name, value=new_session_uuid, httponly=True, secure=False, samesite="lax")
            
        return response

    def _extend_chat_session(self, db_session: Session, chat_session: ChatSession):
        chat_session.last_active_at = datetime.now(timezone.utc)
        db_session.add(chat_session)
        db_session.commit()
        db_session.refresh(chat_session)
        

    def _get_chat_session(self, request: Request, cookie_name: str) -> ChatSession | None:
        cookie_session_id = request.cookies.get(cookie_name)
        chat_session: Optional[ChatSession] = None
        
        if cookie_session_id:
            with Session(engine) as db:
                statement = select(ChatSession).where(ChatSession.user_session == cookie_session_id)
                chat_session = db.exec(statement).first()
        
                if chat_session:
                    self._extend_chat_session( db, chat_session)
                    print(f"Found existing chat session: {chat_session.user_session}")
        
        return chat_session
    
    def _create_new_chat_session_to_db(self):
        with Session(engine) as db_session:
            new_session_uuid = str(uuid4())
            chat_session = ChatSession(user_session=new_session_uuid)
            db_session.add(chat_session)
            db_session.commit()
            db_session.refresh(chat_session)
            print(f"Set cookie name={self.user_session_key_name} value={new_session_uuid}")
            
        return new_session_uuid

