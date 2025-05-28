import datetime
from fastapi import APIRouter, Request, Form, Response
from fastapi.templating import Jinja2Templates
from typing import Annotated, Optional
from fastapi.responses import RedirectResponse
from app.database.models import ChatSession
from app.database.connection import SessionDependency, create_chat_message, get_all_messages
from sqlmodel import select
from uuid import uuid4
from datetime import datetime, timezone

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()
user_session_key_name = "user_session_id"


def extend_chat_session(db_session: SessionDependency, chat_session: ChatSession):
    chat_session.last_active_at = datetime.now(timezone.utc)
    db_session.add(chat_session)
    db_session.commit()
    db_session.refresh(chat_session)
    
    
def get_chat_session(request: Request, cookie_name: str, db_session: SessionDependency) -> ChatSession | None:
    cookie_session_id = request.cookies.get(cookie_name)
    chat_session: Optional[ChatSession] = None
    
    statement = select(ChatSession).where(ChatSession.user_session == cookie_session_id)
    chat_session = db_session.exec(statement).first()
    
    if chat_session:
        extend_chat_session(db_session, chat_session)
        print(f"Found existing chat session: {chat_session.user_session}")
    
    return chat_session
        
def create_new_chat_session_to_db(db_session: SessionDependency):
    new_session_uuid = str(uuid4())
    chat_session = ChatSession(user_session=new_session_uuid)
    db_session.add(chat_session)
    db_session.commit()
    db_session.refresh(chat_session)
    print(f"Set cookie name={user_session_key_name} value={new_session_uuid}")
    return new_session_uuid

@router.get("/")
async def home(request: Request, response: Response, db_session: SessionDependency ):
    
    chat_session = get_chat_session(request, user_session_key_name, db_session)
    messages = None
    
    if chat_session:
        messages = await get_all_messages(chat_session, db_session)
    
    print(messages) 
       
    template_response = templates.TemplateResponse("index.html", {"request": request, "chat_data": messages})
    
    if not chat_session:
        new_session_uuid = create_new_chat_session_to_db(db_session)
        # Jangan lupa untuk mengirim session ke cookie pengguna setiap kali membuat chat session
        template_response.set_cookie(key=user_session_key_name, value=new_session_uuid, httponly=True, secure=False, samesite="lax")

    return template_response


@router.post("/submit")
async def submit(req: Request, res: Response, prompt: Annotated[str, Form()], db: SessionDependency):
    chat_session = get_chat_session(req, user_session_key_name, db)
    if chat_session:
        create_chat_message(prompt, "This is the system answer", chat_session, db)
    return RedirectResponse("/", status_code=303)
