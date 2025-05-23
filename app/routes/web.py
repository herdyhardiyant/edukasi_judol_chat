from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Welcome"})
