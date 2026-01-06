from datetime import datetime
from typing import Dict, List, Optional
from src.models.task import Task


class TaskService:
    """
    Service class for managing tasks in-memory using a dictionary with ID as key.
    """

    def __init__(self):
        """
        Initialize the task service with an empty dictionary to store tasks.
        """
        self.tasks: Dict[int, Task] = {}
        self.next_id = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Add a new task to the in-memory storage.

        Args:
            title: Task title (1-200 characters)
            description: Optional task description

        Returns:
            Created Task instance with auto-assigned ID and timestamps
        """
        # Create the new task with auto-incremented ID
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            completed=False,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Add task to storage
        self.tasks[self.next_id] = task

        # Increment the next ID for the next task
        self.next_id += 1

        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task instance if found, None otherwise
        """
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks sorted by ID in ascending order.

        Returns:
            List of all tasks sorted by ID
        """
        # Sort tasks by ID in ascending order
        return sorted(self.tasks.values(), key=lambda task: task.id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title (optional, if not provided, current title is kept)
            description: New description (optional, if not provided, current description is kept)

        Returns:
            Updated Task instance if the task exists, None otherwise
        """
        if task_id not in self.tasks:
            return None

        task = self.tasks[task_id]

        # Update title if provided
        if title is not None:
            task.title = title

        # Update description if provided
        if description is not None:
            task.description = description

        # Update the updated_at timestamp
        task.updated_at = datetime.now()

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was successfully deleted, False if the task did not exist
        """
        if task_id not in self.tasks:
            return False

        del self.tasks[task_id]
        return True

    def mark_task_complete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as complete.

        Args:
            task_id: The ID of the task to mark as complete

        Returns:
            Updated Task instance if the task exists, None otherwise
        """
        if task_id not in self.tasks:
            return None

        task = self.tasks[task_id]
        task.completed = True
        task.updated_at = datetime.now()

        return task

    def mark_task_incomplete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as incomplete.

        Args:
            task_id: The ID of the task to mark as incomplete

        Returns:
            Updated Task instance if the task exists, None otherwise
        """
        if task_id not in self.tasks:
            return None

        task = self.tasks[task_id]
        task.completed = False
        task.updated_at = datetime.now()

        return task

    def get_next_id(self) -> int:
        """
        Get the next available ID for a new task.

        Returns:
            The next available ID
        """
        return self.next_id