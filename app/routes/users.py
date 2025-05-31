from fastapi import APIRouter, Depends
from app.utils import getDb, hash
from db import DB

from app.models.user import *

router = APIRouter()

@router.get("/")
def root():
    return "Users!"

@router.post("/login")
def login(data: UserLogin, db: DB = Depends(getDb.get_db)):
    username = data.username
    password = data.password

    user = db.execute_query("SELECT username, password FROM Users WHERE username = %s", (username,))

    can_login = hash.verify_password(password, user.password)

    if can_login:
        return 



    
