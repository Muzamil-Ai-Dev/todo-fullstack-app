from datetime import datetime
from typing import Optional


class Task:
    """
    Task entity representing a todo item with all required fields.

    Fields:
    - id: Integer (auto-incremented unique identifier)
    - title: String (1-200 characters, required)
    - description: String (optional, can be None)
    - completed: Boolean (completion status, defaults to False)
    - created_at: DateTime (creation timestamp in ISO 8601 format)
    - updated_at: DateTime (last modification timestamp in ISO 8601 format)
    """

    def __init__(self,
                 id: int,
                 title: str,
                 description: Optional[str] = None,
                 completed: bool = False,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        """
        Initialize a Task instance.

        Args:
            id: Unique identifier for the task
            title: Task title (1-200 characters)
            description: Optional task description
            completed: Completion status (defaults to False)
            created_at: Creation timestamp (defaults to current time if not provided)
            updated_at: Last modification timestamp (defaults to current time if not provided)
        """
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed

        if created_at is None:
            self.created_at = datetime.now()
        else:
            self.created_at = created_at

        if updated_at is None:
            self.updated_at = datetime.now()
        else:
            self.updated_at = updated_at

    def to_dict(self) -> dict:
        """
        Convert the Task instance to a dictionary representation.

        Returns:
            Dictionary representation of the task with all fields formatted properly
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __str__(self) -> str:
        """
        String representation of the task for display purposes.

        Returns:
            Formatted string representation of the task
        """
        status_symbol = '✓' if self.completed else ' '
        return f"[{status_symbol}] {self.title}"

    def __repr__(self) -> str:
        """
        Detailed string representation of the task.

        Returns:
            Detailed string representation for debugging purposes
        """
        return (f"Task(id={self.id}, title='{self.title}', "
                f"description='{self.description}', completed={self.completed}, "
                f"created_at='{self.created_at}', updated_at='{self.updated_at}')")