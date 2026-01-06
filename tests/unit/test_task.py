import pytest
import sys
import os
from datetime import datetime

# Add the src directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.task import Task


class TestTask:
    """
    Unit tests for the Task model.
    """

    def test_task_creation_with_required_fields(self):
        """
        Test creating a Task with required fields only.
        """
        task_id = 1
        title = "Test Task"
        created_at = datetime(2026, 1, 6, 10, 0, 0)
        updated_at = datetime(2026, 1, 6, 10, 0, 0)

        task = Task(
            id=task_id,
            title=title,
            created_at=created_at,
            updated_at=updated_at
        )

        assert task.id == task_id
        assert task.title == title
        assert task.description is None
        assert task.completed is False
        assert task.created_at == created_at
        assert task.updated_at == updated_at

    def test_task_creation_with_all_fields(self):
        """
        Test creating a Task with all fields provided.
        """
        task_id = 1
        title = "Test Task"
        description = "This is a test task"
        completed = True
        created_at = datetime(2026, 1, 6, 10, 0, 0)
        updated_at = datetime(2026, 1, 6, 10, 0, 0)

        task = Task(
            id=task_id,
            title=title,
            description=description,
            completed=completed,
            created_at=created_at,
            updated_at=updated_at
        )

        assert task.id == task_id
        assert task.title == title
        assert task.description == description
        assert task.completed == completed
        assert task.created_at == created_at
        assert task.updated_at == updated_at

    def test_task_creation_with_default_timestamps(self):
        """
        Test creating a Task with default timestamps.
        """
        task_id = 1
        title = "Test Task"

        task = Task(id=task_id, title=title)

        assert task.id == task_id
        assert task.title == title
        assert task.description is None
        assert task.completed is False
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_task_to_dict(self):
        """
        Test converting a Task to dictionary representation.
        """
        task_id = 1
        title = "Test Task"
        description = "This is a test task"
        completed = True
        created_at = datetime(2026, 1, 6, 10, 0, 0)
        updated_at = datetime(2026, 1, 6, 11, 0, 0)

        task = Task(
            id=task_id,
            title=title,
            description=description,
            completed=completed,
            created_at=created_at,
            updated_at=updated_at
        )

        expected_dict = {
            'id': task_id,
            'title': title,
            'description': description,
            'completed': completed,
            'created_at': '2026-01-06 10:00:00',
            'updated_at': '2026-01-06 11:00:00'
        }

        assert task.to_dict() == expected_dict

    def test_task_str_representation(self):
        """
        Test string representation of a Task.
        """
        task_id = 1
        title = "Test Task"
        completed = False

        task = Task(id=task_id, title=title, completed=completed)

        expected_str = "[ ] Test Task"
        assert str(task) == expected_str

        # Test completed task
        task.completed = True
        expected_str_completed = "[✓] Test Task"
        assert str(task) == expected_str_completed

    def test_task_repr_representation(self):
        """
        Test detailed string representation of a Task.
        """
        task_id = 1
        title = "Test Task"
        description = "This is a test task"
        completed = True
        created_at = datetime(2026, 1, 6, 10, 0, 0)
        updated_at = datetime(2026, 1, 6, 11, 0, 0)

        task = Task(
            id=task_id,
            title=title,
            description=description,
            completed=completed,
            created_at=created_at,
            updated_at=updated_at
        )

        repr_str = repr(task)
        assert f"Task(id={task_id}" in repr_str
        assert f"title='{title}'" in repr_str
        assert f"description='{description}'" in repr_str
        assert f"completed={completed}" in repr_str

    def test_task_creation_with_empty_description(self):
        """
        Test creating a Task with an empty description.
        """
        task_id = 1
        title = "Test Task"
        description = ""

        task = Task(id=task_id, title=title, description=description)

        assert task.id == task_id
        assert task.title == title
        assert task.description == description  # Empty string is allowed as description

    def test_task_title_can_contain_special_characters(self):
        """
        Test that task title can contain special characters.
        """
        task_id = 1
        title = "Test Task with special chars: !@#$%^&*()"

        task = Task(id=task_id, title=title)

        assert task.title == title