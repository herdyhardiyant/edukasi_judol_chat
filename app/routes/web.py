import datetime
from fastapi import APIRouter, Request, Form, Response
from fastapi.templating import Jinja2Templates
from typing import Annotated, Optional
from fastapi.responses import RedirectResponse
from app.database.models import ChatSession
from app.database.connection import SessionDependency
from sqlmodel import select
from uuid import uuid4
from datetime import datetime, timezone

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()



@router.get("/")
async def home(request: Request, response: Response, db_session: SessionDependency ):
    user_session_key_name = "user_session_id"
    cookie_session_id = request.cookies.get(user_session_key_name)
    chat_session: Optional[ChatSession] = None
    
    template_response = templates.TemplateResponse("index.html", {"request": request, "message": "Welcome"})
    
    if cookie_session_id:
        statement = select(ChatSession).where(ChatSession.user_session == cookie_session_id)
        chat_session = db_session.exec(statement).first()
    
    if not chat_session:
        print(f"user don't have session in their cookies")
        new_session_uuid = str(uuid4())
        chat_session = ChatSession(user_session=new_session_uuid)
        db_session.add(chat_session)
        db_session.commit()
        db_session.refresh(chat_session)
        print(response.headers)
        print(f"Set cookie name={user_session_key_name} value={new_session_uuid}")
        template_response.set_cookie(key=user_session_key_name, value=new_session_uuid, httponly=True, secure=False, samesite="lax")
        
    else:
        chat_session.last_active_at = datetime.now(timezone.utc)
        db_session.add(chat_session)
        db_session.commit()
        db_session.refresh(chat_session)
        print(f"Found existing chat session: {chat_session.user_session}")

    return template_response


@router.post("/submit")
async def submit(req: Request, res: Response, prompt: Annotated[str, Form()], db: SessionDependency):
    return RedirectResponse("/", status_code=303)
