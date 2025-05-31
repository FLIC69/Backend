from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional

class User(BaseModel):
    id: int
    username: str
    firstName: str
    lastName: str
    email: EmailStr
    password: str

class CreateUser(BaseModel):
    username: str
    firstName: str
    lastName: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str

    # Allows users to login with either their username or password
    @model_validator(mode="after")
    def validate_login(cls, model):
        if not model.email and not model.username:
            raise ValueError("Either 'email' or 'username' must be provided.")
        return model