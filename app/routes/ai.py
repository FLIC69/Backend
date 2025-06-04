from fastapi import APIRouter
from app.db import DB

router = APIRouter()

@router.get("/")
def home():
    return "AI Home"
