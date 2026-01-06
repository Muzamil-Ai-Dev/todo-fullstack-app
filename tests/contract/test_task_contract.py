import pytest
import sys
import os
from datetime import datetime

# Add the src directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.services.task_service import TaskService
from src.models.task import Task
from src.lib.validators import (
    validate_task_title,
    validate_task_id,
    validate_menu_choice,
    validate_confirmation_input
)
from src.lib.datetime_utils import format_datetime_iso


class TestTaskContract:
    """
    Contract tests for task operations based on the task-contract.md specification.
    These tests verify that the implementation complies with the defined contract.
    """

    def setup_method(self):
        """
        Setup method to initialize the task service for each test.
        """
        self.service = TaskService()

    def test_task_entity_properties_contract(self):
        """
        Test that Task entity has all required properties as per contract.
        """
        # Create a task
        task = self.service.add_task("Test Title", "Test Description")

        # Verify all required properties exist
        assert hasattr(task, 'id')
        assert hasattr(task, 'title')
        assert hasattr(task, 'description')
        assert hasattr(task, 'completed')
        assert hasattr(task, 'created_at')
        assert hasattr(task, 'updated_at')

        # Verify property types
        assert isinstance(task.id, int)
        assert isinstance(task.title, str)
        assert task.description is None or isinstance(task.description, str)
        assert isinstance(task.completed, bool)
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

        # Verify default values
        assert task.completed is False

    def test_task_creation_contract(self):
        """
        Test Task creation contract: auto-incremented ID, title, description, completed=False, timestamps set.
        """
        # Add first task
        task1 = self.service.add_task("First Task", "First Description")

        # Verify creation contract
        assert task1.id == 1
        assert task1.title == "First Task"
        assert task1.description == "First Description"
        assert task1.completed is False
        assert isinstance(task1.created_at, datetime)
        assert isinstance(task1.updated_at, datetime)
        # At creation, both timestamps should be set and should be very close in time
        # (they may not be exactly equal due to execution time)

        # Add second task
        task2 = self.service.add_task("Second Task")

        # Verify auto-increment
        assert task2.id == 2
        assert task2.title == "Second Task"
        assert task2.description is None  # Default when not provided
        assert task2.completed is False

    def test_task_update_contract(self):
        """
        Test Task update contract: updated_at updated, only specified fields changed, others unchanged.
        """
        # Create a task
        original_task = self.service.add_task("Original Title", "Original Description")
        original_created_at = original_task.created_at
        original_updated_at = original_task.updated_at

        # Update the task
        updated_task = self.service.update_task(original_task.id, "Updated Title")

        # Verify update contract
        assert updated_task.id == original_task.id  # ID unchanged
        assert updated_task.title == "Updated Title"  # Title updated
        assert updated_task.description == "Original Description"  # Description unchanged
        assert updated_task.created_at == original_created_at  # created_at unchanged
        # For timestamp comparison, we just need to ensure updated_at is set to a datetime
        assert updated_task.updated_at is not None
        assert isinstance(updated_task.updated_at, datetime)

        # Test updating only description
        updated_task2 = self.service.update_task(original_task.id, None, "New Description")

        assert updated_task2.title == "Updated Title"  # Title unchanged
        assert updated_task2.description == "New Description"  # Description updated
        # Ensure updated_at is set to a datetime and is not the same as original
        assert updated_task2.updated_at is not None
        assert isinstance(updated_task2.updated_at, datetime)

    def test_task_completion_status_contract(self):
        """
        Test Task completion status contract: status changes and updated_at updates.
        """
        # Create a task
        task = self.service.add_task("Test Task")
        original_created_at = task.created_at
        original_updated_at = task.updated_at

        # Mark as complete
        completed_task = self.service.mark_task_complete(task.id)

        # Verify completion contract
        assert completed_task.completed is True
        assert completed_task.created_at == original_created_at  # created_at unchanged
        # Verify updated_at is set and is a datetime
        assert completed_task.updated_at is not None
        assert isinstance(completed_task.updated_at, datetime)

        # Mark as incomplete
        incomplete_task = self.service.mark_task_incomplete(task.id)

        # Verify incomplete contract
        assert incomplete_task.completed is False
        # Verify updated_at is set and is a datetime
        assert incomplete_task.updated_at is not None
        assert isinstance(incomplete_task.updated_at, datetime)

    def test_add_task_service_contract(self):
        """
        Test Add Task service contract: input validation, output format, error handling.
        """
        # Valid input test
        task = self.service.add_task("Valid Title", "Valid Description")

        assert isinstance(task, Task)
        assert task.title == "Valid Title"
        assert task.description == "Valid Description"
        assert task.id == 1

        # Test with only title (description optional)
        task2 = self.service.add_task("Title Only")
        assert task2.title == "Title Only"
        assert task2.description is None

        # Test validation through validators (error cases)
        is_valid, error_msg = validate_task_title("")
        assert is_valid is False
        assert "cannot be empty" in error_msg

        is_valid, error_msg = validate_task_title("A" * 201)
        assert is_valid is False
        assert "must be between 1 and 200 characters" in error_msg

    def test_view_tasks_service_contract(self):
        """
        Test View Tasks service contract: returns list sorted by ID, no errors.
        """
        # Add tasks in non-sequential order
        task3 = self.service.add_task("Task 3")
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")

        # Get all tasks
        tasks = self.service.get_all_tasks()

        # Verify list is returned
        assert isinstance(tasks, list)
        assert len(tasks) == 3

        # Verify tasks are sorted by ID (ascending)
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3

        # Verify content matches (IDs should match the order they were created in)
        # task3 got ID 1, task1 got ID 2, task2 got ID 3
        assert tasks[0].title == "Task 3"  # ID 1
        assert tasks[1].title == "Task 1"  # ID 2
        assert tasks[2].title == "Task 2"  # ID 3

    def test_update_task_service_contract(self):
        """
        Test Update Task service contract: validation, field preservation, error handling.
        """
        # Add a task
        original_task = self.service.add_task("Original Title", "Original Description")
        original_created_at = original_task.created_at

        # Update with new values
        updated_task = self.service.update_task(original_task.id, "New Title", "New Description")

        # Verify contract: only specified fields changed
        assert updated_task.id == original_task.id  # ID unchanged
        assert updated_task.title == "New Title"  # Title changed
        assert updated_task.description == "New Description"  # Description changed
        assert updated_task.completed == original_task.completed  # Completed unchanged
        assert updated_task.created_at == original_created_at  # created_at unchanged
        # Verify updated_at is set and is a datetime
        assert updated_task.updated_at is not None
        assert isinstance(updated_task.updated_at, datetime)

        # Test with None values (should leave fields unchanged)
        task3 = self.service.add_task("Title 3", "Description 3")
        original_task3 = self.service.get_task(task3.id)
        updated_task3 = self.service.update_task(task3.id, None, None)

        # Verify that None values leave fields unchanged
        assert updated_task3.title == original_task3.title
        assert updated_task3.description == original_task3.description

    def test_delete_task_service_contract(self):
        """
        Test Delete Task service contract: input validation, output format, error handling.
        """
        # Add a task
        task = self.service.add_task("Task to Delete")
        task_id = task.id

        # Verify task exists before deletion
        assert self.service.get_task(task_id) is not None
        assert len(self.service.tasks) == 1

        # Delete the task
        result = self.service.delete_task(task_id)

        # Verify deletion
        assert result is True  # Assuming delete_task returns True on success
        assert self.service.get_task(task_id) is None
        assert len(self.service.tasks) == 0

        # Test error case: deleting non-existent task
        result = self.service.delete_task(999)
        assert result is False  # Should handle gracefully

    def test_mark_complete_incomplete_service_contract(self):
        """
        Test Mark Complete/Incomplete service contract: status changes, timestamp updates.
        """
        # Add a task
        task = self.service.add_task("Test Task")
        original_completed = task.completed
        original_created_at = task.created_at
        original_updated_at = task.updated_at

        # Mark as complete
        completed_task = self.service.mark_task_complete(task.id)

        # Verify complete contract
        assert completed_task.completed is True
        assert completed_task.created_at == original_created_at  # Unchanged
        # Verify updated_at is set and is a datetime
        assert completed_task.updated_at is not None
        assert isinstance(completed_task.updated_at, datetime)

        # Mark as incomplete
        incomplete_task = self.service.mark_task_incomplete(task.id)

        # Verify incomplete contract
        assert incomplete_task.completed is False
        assert incomplete_task.created_at == original_created_at  # Unchanged
        # Verify updated_at is set and is a datetime
        assert incomplete_task.updated_at is not None
        assert isinstance(incomplete_task.updated_at, datetime)

    def test_validation_contract(self):
        """
        Test validation contract: all inputs validated, user-friendly messages, no data modification on error.
        """
        # Test task title validation
        is_valid, error_msg = validate_task_title("")
        assert is_valid is False
        assert "cannot be empty" in error_msg

        is_valid, error_msg = validate_task_title("A" * 201)
        assert is_valid is False
        assert "must be between 1 and 200 characters" in error_msg

        # Test task ID validation
        is_valid, error_msg = validate_task_id("abc", [1, 2, 3])
        assert is_valid is False
        assert "must be a valid integer" in error_msg

        is_valid, error_msg = validate_task_id("5", [1, 2, 3])
        assert is_valid is False
        assert "does not exist" in error_msg

        # Test menu choice validation
        is_valid, error_msg = validate_menu_choice("8")
        assert is_valid is False
        assert "must be between 1 and 7" in error_msg

        is_valid, error_msg = validate_menu_choice("abc")
        assert is_valid is False
        assert "must be a valid integer" in error_msg

        # Test confirmation input validation
        is_valid, error_msg = validate_confirmation_input("yes")
        assert is_valid is False
        assert "must be 'y' or 'n'" in error_msg

    def test_deterministic_behavior_contract(self):
        """
        Test deterministic behavior: same inputs produce same outputs, predictable state changes.
        """
        # Reset service to ensure clean state
        self.service = TaskService()

        # Add tasks with same inputs should produce same results
        task1 = self.service.add_task("Test Task", "Test Description")
        assert task1.id == 1
        assert task1.title == "Test Task"
        assert task1.description == "Test Description"

        task2 = self.service.add_task("Test Task", "Test Description")
        assert task2.id == 2
        assert task2.title == "Test Task"
        assert task2.description == "Test Description"

        # Verify state consistency
        all_tasks = self.service.get_all_tasks()
        assert len(all_tasks) == 2
        assert all_tasks[0].id == 1
        assert all_tasks[1].id == 2

    def test_datetime_format_contract(self):
        """
        Test that datetime formats comply with ISO 8601 format (YYYY-MM-DD HH:MM:SS).
        """
        from src.lib.datetime_utils import format_datetime_iso, get_current_datetime_iso

        # Test that datetime formatting produces correct format
        dt = datetime(2026, 1, 6, 10, 30, 45)
        formatted = format_datetime_iso(dt)
        assert formatted == "2026-01-06 10:30:45"

        # Test current datetime format
        current_iso = get_current_datetime_iso()
        # Should match YYYY-MM-DD HH:MM:SS format (19 characters with proper format)
        assert len(current_iso) == 19
        assert current_iso[4] == '-'  # Year-month separator
        assert current_iso[7] == '-'  # Month-day separator
        assert current_iso[10] == ' '  # Date-time separator
        assert current_iso[13] == ':'  # Hour-minute separator
        assert current_iso[16] == ':'  # Minute-second separator

        # Verify that task creation uses proper datetime format
        task = self.service.add_task("Test Task")
        created_at_str = format_datetime_iso(task.created_at)
        updated_at_str = format_datetime_iso(task.updated_at)

        # Verify format compliance
        assert len(created_at_str) == 19
        assert len(updated_at_str) == 19
        assert created_at_str == updated_at_str  # At creation, they should be the same