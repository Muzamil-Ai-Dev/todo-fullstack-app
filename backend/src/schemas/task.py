from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TaskCreateRequest(BaseModel):
    """
    Schema for creating a new task
    """
    title: str
    description: Optional[str] = None


class TaskUpdateRequest(BaseModel):
    """
    Schema for updating an existing task
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    """
    Schema for task response
    """
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    """
    Schema for listing tasks response
    """
    tasks: List[TaskResponse]
    total_count: int


class TaskToggleCompleteResponse(BaseModel):
    """
    Schema for task completion toggle response
    """
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime


class TaskDeleteResponse(BaseModel):
    """
    Schema for task deletion response (empty body for 204 No Content)
    """
    success: bool = True