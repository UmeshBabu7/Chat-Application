from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models import UserRole

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.USER

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    
    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None

# Message schemas
class MessageBase(BaseModel):
    content: str
    room_id: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    user_id: int
    created_at: datetime
    user: User
    
    class Config:
        from_attributes = True

# WebSocket message schemas
class WebSocketMessage(BaseModel):
    type: str  # "message", "join", "leave"
    content: Optional[str] = None
    room_id: str
    user_id: Optional[int] = None
    username: Optional[str] = None 