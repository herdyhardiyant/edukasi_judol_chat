from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import web
from app.database.connection import create_db_and_tables
from app.database.models import *
from contextlib import asynccontextmanager
from app.auth.middleware import SessionAuthMiddleware
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(web.router)

app.add_middleware(SessionAuthMiddleware)