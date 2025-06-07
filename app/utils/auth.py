from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Request
from typing import Optional
from fastapi.responses import JSONResponse
import os

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

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    SECRET_KEY = os.getenv("JWT_TOKEN")

    if SECRET_KEY is None:
        raise RuntimeError("JWT_TOKEN not found in environment")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No JWT found",
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        request.state.user = payload.get("sub")
        return payload.get("sub")  # Optional: return user ID or claims
    except JWTError:
        response = JSONResponse(
            content={"detail": "Invalid or expired token"},
            status_code=401
        )
        response.delete_cookie("token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    
def log_db(db, user_id: int, endpoint: str, method: str):
    print("Guardando log en la base de datos...")
    try:
        query = """
            INSERT INTO logs (user_id, endpoint, method)
            VALUES (%s, %s, %s)
        """
        db.execute_query(query, (user_id, endpoint, method))
    except Exception as e:
        print("Error al guardar log:", e)

async def verify_token(request: Request) -> dict:
    # Extract token from cookies
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token"
        )
    
    try:
        # Verify and decode the JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


