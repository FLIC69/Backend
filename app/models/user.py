from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    username: str
    firstName: str
    lastName: str
    email: EmailStr
    password: str

class CreateUser(BaseModel):