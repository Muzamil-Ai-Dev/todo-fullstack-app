from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserLoginRequest(BaseModel):
    """
    Schema for user login request
    """
    email: str
    password: str


class UserLoginResponse(BaseModel):
    """
    Schema for user login response
    """
    access_token: str
    token_type: str = "bearer"


class UserRegisterRequest(BaseModel):
    """
    Schema for user registration request
    """
    email: str
    name: str
    password: str


class UserRegisterResponse(BaseModel):
    """
    Schema for user registration response
    """
    id: str
    email: str
    name: str
    created_at: datetime


class UserResponse(BaseModel):
    """
    Schema for user response (public data only)
    """
    id: str
    email: str
    name: str
    created_at: datetime
    updated_at: datetime