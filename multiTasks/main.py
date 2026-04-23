from fastapi import FastAPI
from sqlalchemy.orm import Session
from . import models,schemas
from .database import get_db
import psycopg2
from .router import user,auth,assign,comments

app = FastAPI()


app.include_router(user.router)
app.include_router(auth.router)
app.include_router(assign.router)
app.include_router(comments.router)
