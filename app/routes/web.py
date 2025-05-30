from fastapi import APIRouter, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from typing import Annotated, Optional
from fastapi.responses import RedirectResponse
from app.database.models import ChatSession
from app.database.connection import SessionDependency, create_chat_message, get_all_messages

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()
user_session_key_name = "user_session_id"


@router.get("/")
async def home(request: Request, db_session: SessionDependency ):
    chat_session: ChatSession = request.state.chat_session
    
    messages = []
    
    if chat_session:
        messages = await get_all_messages(chat_session, db_session)
    
    template_response = templates.TemplateResponse("index.html", {"request": request, "chat_data": messages})

    return template_response

@router.post("/submit")
async def submit(req: Request, message: Annotated[Optional[str], Form()], image: Annotated[Optional[UploadFile], File()], db: SessionDependency):
    chat_session: ChatSession = req.state.chat_session
    print(f"Received content type: {image.content_type if image else 'No image'}")
    if chat_session:
        create_chat_message(message, "This is the system answer", None, chat_session, db)
    return RedirectResponse("/", status_code=303)
