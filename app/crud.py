from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app.models import User, Message, UserRole
from app.schemas import UserCreate, MessageCreate
from app.auth import get_password_hash, verify_password

# User CRUD operations
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username."""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate user with username and password."""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users with pagination."""
    return db.query(User).offset(skip).limit(limit).all()

# Message CRUD operations
def create_message(db: Session, message: MessageCreate, user_id: int) -> Message:
    """Create a new message."""
    db_message = Message(
        content=message.content,
        room_id=message.room_id,
        user_id=user_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages_by_room(
    db: Session, 
    room_id: str, 
    skip: int = 0, 
    limit: int = 50,
    cursor: Optional[int] = None
) -> List[Message]:
    """Get messages for a specific room with cursor-based pagination."""
    query = db.query(Message).filter(Message.room_id == room_id)
    
    if cursor:
        query = query.filter(Message.id < cursor)
    
    return query.order_by(desc(Message.id)).offset(skip).limit(limit).all()

def get_message_by_id(db: Session, message_id: int) -> Optional[Message]:
    """Get message by ID."""
    return db.query(Message).filter(Message.id == message_id).first()

def delete_message(db: Session, message_id: int, user_id: int) -> bool:
    """Delete a message (only by the author or admin)."""
    message = get_message_by_id(db, message_id)
    if not message:
        return False
    
    # Check if user is the author or admin
    user = get_user_by_id(db, user_id)
    if message.user_id != user_id and user.role != UserRole.ADMIN:
        return False
    
    db.delete(message)
    db.commit()
    return True 