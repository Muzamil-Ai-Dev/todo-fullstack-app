from sqlmodel import Session, select, update
from typing import List, Optional
from datetime import datetime
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User


class TaskService:
    """
    Service class for handling task-related operations
    """

    @staticmethod
    def create_task(session: Session, user_id: str, task_create: TaskCreate) -> Task:
        """
        Create a new task for the specified user
        """
        # Get current timestamp to ensure both created_at and updated_at are identical
        current_time = datetime.utcnow()

        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=False,  # Default to not completed
            user_id=user_id,
            created_at=current_time,
            updated_at=current_time
        )

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return db_task

    @staticmethod
    def get_tasks_by_user(
        session: Session,
        user_id: str,
        status_filter: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Task]:
        """
        Get all tasks for a specific user with optional filtering
        """
        statement = select(Task).where(Task.user_id == user_id)

        # Apply status filter if provided
        if status_filter:
            if status_filter.lower() == "completed":
                statement = statement.where(Task.completed == True)
            elif status_filter.lower() == "pending":
                statement = statement.where(Task.completed == False)

        # Apply pagination if provided
        if limit is not None:
            statement = statement.limit(limit)
        if offset is not None:
            statement = statement.offset(offset)

        return session.exec(statement).all()

    @staticmethod
    def get_task_by_id_and_user(session: Session, task_id: int, user_id: str) -> Optional[Task]:
        """
        Get a specific task by ID and ensure it belongs to the user
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def update_task(session: Session, task_id: int, user_id: str, task_update: TaskUpdate) -> Optional[Task]:
        """
        Update an existing task for the specified user
        """
        # First verify the task belongs to the user
        db_task = TaskService.get_task_by_id_and_user(session, task_id, user_id)
        if not db_task:
            return None

        # Prepare update data
        update_data = task_update.dict(exclude_unset=True)

        # Apply updates
        for field, value in update_data.items():
            setattr(db_task, field, value)

        # Update the updated_at timestamp
        db_task.updated_at = datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return db_task

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: str) -> bool:
        """
        Delete a task for the specified user
        """
        # First verify the task belongs to the user
        db_task = TaskService.get_task_by_id_and_user(session, task_id, user_id)
        if not db_task:
            return False

        session.delete(db_task)
        session.commit()

        return True

    @staticmethod
    def toggle_task_completion(session: Session, task_id: int, user_id: str) -> Optional[Task]:
        """
        Toggle the completion status of a task
        """
        # First verify the task belongs to the user
        db_task = TaskService.get_task_by_id_and_user(session, task_id, user_id)
        if not db_task:
            return None

        # Toggle the completion status
        db_task.completed = not db_task.completed

        # Update the updated_at timestamp
        db_task.updated_at = datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return db_task