from pydantic import BaseModel

# Pydantic models
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True