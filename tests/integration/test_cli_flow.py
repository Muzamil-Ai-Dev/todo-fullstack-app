import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the src directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.cli.main import main, add_task, view_tasks, update_task, delete_task, mark_task_complete, mark_task_incomplete
from rich.console import Console
from src.services.task_service import TaskService
from src.models.task import Task


class TestCLIFlowIntegration:
    """
    Integration tests for CLI flows.
    """

    def setup_method(self):
        """
        Setup method to initialize the task service for each test.
        """
        self.service = TaskService()

    def test_add_task_integration(self):
        """
        Test adding a task through the CLI flow.
        """
        # Prepare mock input for the CLI flow
        with patch('src.cli.main.get_user_input') as mock_input:
            mock_input.side_effect = ["Test Task", "Test Description"]

            # Call the add_task function
            add_task(self.service)

            # Verify the task was added
            assert len(self.service.tasks) == 1
            task = list(self.service.tasks.values())[0]
            assert task.title == "Test Task"
            assert task.description == "Test Description"
            assert task.completed is False

    def test_add_task_with_empty_description_integration(self):
        """
        Test adding a task with empty description through the CLI flow.
        """
        with patch('src.cli.main.get_user_input') as mock_input:
            mock_input.side_effect = ["Test Task", ""]  # Empty description

            add_task(self.service)

            assert len(self.service.tasks) == 1
            task = list(self.service.tasks.values())[0]
            assert task.title == "Test Task"
            assert task.description is None  # Should be None when empty

    def test_view_tasks_integration(self):
        """
        Test viewing tasks through the CLI flow.
        """
        # Add a task first
        self.service.add_task("Test Task", "Test Description")

        # Mock Rich console print function to capture output
        with patch('src.cli.main.console.print') as mock_print:
            view_tasks(self.service)

            # Verify that print was called (meaning tasks were displayed)
            assert mock_print.called

    def test_update_task_integration(self):
        """
        Test updating a task through the CLI flow.
        """
        # Add a task first
        task = self.service.add_task("Original Title", "Original Description")

        # Mock input for the update flow
        with patch('src.cli.main.get_user_input') as mock_input:
            mock_input.side_effect = [str(task.id), "Updated Title", "Updated Description"]

            update_task(self.service)

            # Verify the task was updated
            updated_task = self.service.get_task(task.id)
            assert updated_task.title == "Updated Title"
            assert updated_task.description == "Updated Description"

    def test_update_task_with_blank_inputs_integration(self):
        """
        Test updating a task with blank inputs (should keep original values).
        """
        # Add a task first
        task = self.service.add_task("Original Title", "Original Description")

        # Mock input with blank values (should keep original values)
        with patch('src.cli.main.get_user_input') as mock_input:
            mock_input.side_effect = [str(task.id), "", ""]  # Blank title and description

            update_task(self.service)

            # Verify the task values remain unchanged
            updated_task = self.service.get_task(task.id)
            assert updated_task.title == "Original Title"
            assert updated_task.description == "Original Description"

    def test_delete_task_integration(self):
        """
        Test deleting a task through the CLI flow.
        """
        # Add a task first
        task = self.service.add_task("Test Task", "Test Description")

        # Mock input for the delete flow
        with patch('src.cli.main.get_user_input') as mock_input:
            mock_input.side_effect = [str(task.id), "y"]  # Confirm deletion

            delete_task(self.service)

            # Verify the task was deleted
            assert len(self.service.tasks) == 0
            assert self.service.get_task(task.id) is None

    def test_delete_task_cancelled_integration(self):
        """
        Test cancelling task deletion through the CLI flow.
        """
        # Add a task first
        task = self.service.add_task("Test Task", "Test Description")

        # Mock input to cancel deletion
        with patch('src.cli.main.get_user_input') as mock_input:
            mock_input.side_effect = [str(task.id), "n"]  # Cancel deletion

            delete_task(self.service)

            # Verify the task still exists
            assert len(self.service.tasks) == 1
            assert self.service.get_task(task.id) is not None

    def test_mark_task_complete_integration(self):
        """
        Test marking a task as complete through the CLI flow.
        """
        # Add a task first
        task = self.service.add_task("Test Task", "Test Description")
        assert task.completed is False  # Initially not completed

        # Mock input for the mark complete flow
        with patch('src.cli.main.get_user_input') as mock_input:
            mock_input.return_value = str(task.id)

            mark_task_complete(self.service)

            # Verify the task was marked as complete
            updated_task = self.service.get_task(task.id)
            assert updated_task.completed is True

    def test_mark_task_incomplete_integration(self):
        """
        Test marking a task as incomplete through the CLI flow.
        """
        # Add a task first and mark it as complete
        task = self.service.add_task("Test Task", "Test Description")
        task.completed = True  # Manually mark as complete

        # Mock input for the mark incomplete flow
        with patch('src.cli.main.get_user_input') as mock_input:
            mock_input.return_value = str(task.id)

            mark_task_incomplete(self.service)

            # Verify the task was marked as incomplete
            updated_task = self.service.get_task(task.id)
            assert updated_task.completed is False

    def test_menu_validation_integration(self):
        """
        Test that the CLI validates menu choices properly.
        """
        # Test with valid choice
        from src.cli.main import validate_menu_choice
        is_valid, error_msg = validate_menu_choice("1")
        assert is_valid is True

        # Test with invalid choice
        is_valid, error_msg = validate_menu_choice("10")
        assert is_valid is False

    def test_task_service_and_model_integration(self):
        """
        Test integration between Task model and TaskService.
        """
        # Add a task
        task = self.service.add_task("Integration Test", "Testing service-model integration")

        # Retrieve the task
        retrieved_task = self.service.get_task(task.id)

        # Verify the task is the same
        assert retrieved_task.id == task.id
        assert retrieved_task.title == task.title
        assert retrieved_task.description == task.description
        assert retrieved_task.completed == task.completed

        # Update the task
        updated_task = self.service.update_task(task.id, "Updated Integration Test", "Updated description")

        # Verify the update
        assert updated_task.title == "Updated Integration Test"
        assert updated_task.description == "Updated description"

        # Verify the updated timestamp
        assert updated_task.updated_at > updated_task.created_at