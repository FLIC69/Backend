from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional

class User(BaseModel):
    id: int
    username: str
    password: str

class CreateUser(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
