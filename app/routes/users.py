from fastapi import APIRouter, Depends, HTTPException, status
from app.utils import getDb, auth
from app.db import DB
from datetime import timedelta
from fastapi import HTTPException

from app.models.user import *

router = APIRouter()

@router.get("/")
def root(db: DB = Depends(getDb.get_db)):
    data = db.execute_query("SELECT * FROM Users;", fetch=True)
    return data 


@router.post("/login")
def login(data: UserLogin, db: DB = Depends(getDb.get_db)):
    try:
        result = db.execute_query(
            "SELECT id, username, password FROM users WHERE username = %s", 
            (data.username,), 
            fetch=True
        )

        if not result:
            auth.log_db(db, 0, "/users/login", "POST")  
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        user = result[0]
        hashed_password = user[2]

        if not auth.verify_password(data.password, hashed_password):
            auth.log_db(db, user[0], "/users/login", "POST")  
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user[1]},
            expires_delta=access_token_expires
        )

        auth.log_db(db, user[0], "/users/login", "POST")  

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user[0],
            "username": user[1]
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}"
        )
    
@router.post("/register")
def register(data: CreateUser, db: DB = Depends(getDb.get_db)):
    try:
        hashed_password = auth.get_password_hash(data.password)

        query = """
        INSERT INTO users (username, password)
        VALUES (%s, %s)
        RETURNING username
        """
        
        params = (
            data.username,
            hashed_password
        )
        return db.execute_query(query, params, fetch=True)[0]

    except Exception as e:
        print("Error real:", str(e)) 
        raise HTTPException(status_code=500, detail=f"Error al registrar: {e}")




    
