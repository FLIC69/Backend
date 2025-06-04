from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Optional
import os
from sqlalchemy import text

from dotenv import load_dotenv
load_dotenv()

# Configuration
SECRET_KEY = os.environ["JWT_TOKEN"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Here you would typically fetch user from DB
    # For now we'll just return the username
    return {"username": username}

def get_user_by_username(username: str, db) -> dict | None:
    try:
        query = text("SELECT * FROM usuarios WHERE username = :username")
        result = db.fetch_one(query, {"username": username})
        return result
    except Exception as e:
        print("Error al consultar el usuario:", e)
        return None
    

def log_db(db, user_id: int, endpoint: str, method: str):
    print("Guardando log en la base de datos...")
    try:
        query = text("""
            INSERT INTO logs (user_id, endpoint, method)
            VALUES (%s, %s, %s)
        """)
        db.execute(query, (user_id, endpoint, method))
    except Exception as e:
        print("Error al guardar log:", e)


