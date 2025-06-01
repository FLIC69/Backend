from fastapi import APIRouter, Depends, HTTPException, status
from app.utils import getDb, auth
from app.db import DB
from datetime import timedelta

from app.models.user import *

router = APIRouter()

@router.get("/")
def root(db: DB = Depends(getDb.get_db)):
    data = db.execute_query("SELECT * FROM Users;", fetch=True)
    return data 


@router.post("/login")
def login(data: UserLogin, db: DB = Depends(getDb.get_db)):
    try:
        # Fetch user - results are tuples
        result = db.execute_query(
            "SELECT id, username, password FROM users WHERE username = %s", 
            (data.username,), 
            fetch=True
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        user = result[0]
        hashed_password = user[2]  # password is index 2

        if not auth.verify_password(data.password, hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Create JWT token
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user[1]},  # user[1] is username
            expires_delta=access_token_expires
        )

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
    hashed_password = auth.get_password_hash(data.password)

    query = """
    INSERT INTO users (username, first_name, last_name, email, password)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id, username, first_name, last_name, email, created_at
    """
    
    params = (
        data.username,
        data.firstName,
        data.lastName,
        data.email,
        hashed_password
    )
    return db.execute_query(query, params, fetch=True)[0]



    
