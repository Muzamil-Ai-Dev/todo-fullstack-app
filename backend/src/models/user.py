from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

class UserBase(SQLModel):
    """
    Base model for User with shared attributes
    """
    email: str = Field(unique=True, nullable=False, max_length=255)
    name: str = Field(nullable=False, min_length=1, max_length=100)


class User(UserBase, table=True):
    """
    User model representing a registered user of the system
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default=datetime.utcnow(), nullable=False)

    # Relationship to tasks
    tasks: list["Task"] = Relationship(back_populates="user")



class UserRead(UserBase):
    """
    Schema for reading user data (without sensitive information)
    """
    id: str
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    """
    Schema for creating a new user
    """
    password: str = Field(min_length=6)  # Password will be hashed before storing


class UserUpdate(SQLModel):
    """
    Schema for updating user information
    """
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[str] = Field(default=None, max_length=255)