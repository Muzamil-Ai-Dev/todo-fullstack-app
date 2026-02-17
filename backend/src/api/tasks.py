from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import Session
from typing import Annotated, Optional
from src.database import get_session
from src.middleware.auth_middleware import get_current_user_with_auth, jwt_security
from src.services.task_service import TaskService
from src.schemas.task import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskResponse,
    TaskListResponse,
    TaskToggleCompleteResponse
)


tasks_router = APIRouter()


@tasks_router.get("/tasks", response_model=TaskListResponse,
                  description="Retrieve all tasks for the authenticated user")
def get_user_tasks(
    current_user_id: Annotated[str, Depends(get_current_user_with_auth)],
    session: Annotated[Session, Depends(get_session)],
    status_filter: Optional[str] = Query(None, description="Filter by status (all, pending, completed)"),
    limit: Optional[int] = Query(50, ge=1, le=100, description="Number of tasks to return (default: 50)"),
    offset: Optional[int] = Query(0, ge=0, description="Offset for pagination (default: 0)")
):
    """
    Retrieve all tasks for the authenticated user
    """
    tasks = TaskService.get_tasks_by_user(
        session=session,
        user_id=current_user_id,
        status_filter=status_filter,
        limit=limit,
        offset=offset
    )

    # Convert to response format
    task_responses = []
    for task in tasks:
        task_responses.append(TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        ))

    return TaskListResponse(tasks=task_responses, total_count=len(task_responses))


@tasks_router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED,
                   description="Create a new task for the authenticated user")
def create_task(
    current_user_id: Annotated[str, Depends(get_current_user_with_auth)],
    task_create: TaskCreateRequest,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Create a new task for the authenticated user
    """
    # Validate input - title must be 1-200 characters
    if not (1 <= len(task_create.title) <= 200):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title must be between 1 and 200 characters"
        )

    # Validate description if provided - must be <= 1000 characters
    if task_create.description and len(task_create.description) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description must be 1000 characters or less"
        )

    # Create the task
    db_task = TaskService.create_task(
        session=session,
        user_id=current_user_id,
        task_create=task_create
    )

    # Convert to response format
    return TaskResponse(
        id=db_task.id,
        user_id=db_task.user_id,
        title=db_task.title,
        description=db_task.description,
        completed=db_task.completed,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at
    )


@tasks_router.get("/tasks/{task_id}", response_model=TaskResponse,
                  description="Retrieve a specific task by ID for the authenticated user")
def get_task(
    current_user_id: Annotated[str, Depends(get_current_user_with_auth)],
    task_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Retrieve a specific task by ID for the authenticated user
    """
    db_task = TaskService.get_task_by_id_and_user(
        session=session,
        task_id=task_id,
        user_id=current_user_id
    )

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    return TaskResponse(
        id=db_task.id,
        user_id=db_task.user_id,
        title=db_task.title,
        description=db_task.description,
        completed=db_task.completed,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at
    )


@tasks_router.put("/tasks/{task_id}", response_model=TaskResponse,
                  description="Update an existing task for the authenticated user")
def update_task(
    current_user_id: Annotated[str, Depends(get_current_user_with_auth)],
    task_id: int,
    task_update: TaskUpdateRequest,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Update an existing task for the authenticated user
    """
    # Validate input if fields are provided
    if task_update.title is not None and not (1 <= len(task_update.title) <= 200):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title must be between 1 and 200 characters"
        )

    if task_update.description is not None and len(task_update.description) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description must be 1000 characters or less"
        )

    # Update the task
    updated_task = TaskService.update_task(
        session=session,
        task_id=task_id,
        user_id=current_user_id,
        task_update=task_update
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    return TaskResponse(
        id=updated_task.id,
        user_id=updated_task.user_id,
        title=updated_task.title,
        description=updated_task.description,
        completed=updated_task.completed,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )


@tasks_router.patch("/tasks/{task_id}/toggle-complete", response_model=TaskToggleCompleteResponse,
                     description="Toggle the completion status of a task")
def toggle_task_completion(
    current_user_id: Annotated[str, Depends(get_current_user_with_auth)],
    task_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Toggle the completion status of a task
    """
    # Toggle task completion
    updated_task = TaskService.toggle_task_completion(
        session=session,
        task_id=task_id,
        user_id=current_user_id
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    return TaskToggleCompleteResponse(
        id=updated_task.id,
        user_id=updated_task.user_id,
        title=updated_task.title,
        description=updated_task.description,
        completed=updated_task.completed,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )


@tasks_router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT,
                     description="Delete a specific task by ID for the authenticated user")
def delete_task(
    current_user_id: Annotated[str, Depends(get_current_user_with_auth)],
    task_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Delete a specific task by ID for the authenticated user
    """
    success = TaskService.delete_task(
        session=session,
        task_id=task_id,
        user_id=current_user_id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    # Return 204 No Content on successful deletion
    return