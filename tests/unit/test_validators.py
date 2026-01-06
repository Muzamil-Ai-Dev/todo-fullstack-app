import pytest
import sys
import os

# Add the src directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.lib.validators import (
    validate_task_title,
    validate_task_id,
    validate_menu_choice,
    validate_confirmation_input,
    validate_task_description,
    is_valid_datetime_format
)


class TestValidators:
    """
    Unit tests for validation functions.
    """

    def test_validate_task_title_valid(self):
        """
        Test valid task titles.
        """
        # Valid title within range
        is_valid, error_msg = validate_task_title("Valid task title")
        assert is_valid is True
        assert error_msg is None

        # Valid title at minimum length
        is_valid, error_msg = validate_task_title("A")
        assert is_valid is True
        assert error_msg is None

        # Valid title at maximum length
        long_title = "A" * 200
        is_valid, error_msg = validate_task_title(long_title)
        assert is_valid is True
        assert error_msg is None

    def test_validate_task_title_invalid(self):
        """
        Test invalid task titles.
        """
        # Empty title
        is_valid, error_msg = validate_task_title("")
        assert is_valid is False
        assert error_msg == "Task title cannot be empty"

        # Title with only whitespace
        is_valid, error_msg = validate_task_title("   ")
        assert is_valid is False
        assert error_msg == "Task title cannot be empty"

        # Title too long
        long_title = "A" * 201
        is_valid, error_msg = validate_task_title(long_title)
        assert is_valid is False
        assert "must be between 1 and 200 characters" in error_msg

        # Title too short (empty)
        is_valid, error_msg = validate_task_title("")
        assert is_valid is False
        assert error_msg == "Task title cannot be empty"

    def test_validate_task_id_valid(self):
        """
        Test valid task IDs.
        """
        existing_ids = [1, 2, 3, 4, 5]
        is_valid, error_msg = validate_task_id("3", existing_ids)
        assert is_valid is True
        assert error_msg is None

    def test_validate_task_id_invalid(self):
        """
        Test invalid task IDs.
        """
        existing_ids = [1, 2, 3, 4, 5]

        # Non-existent task ID
        is_valid, error_msg = validate_task_id("10", existing_ids)
        assert is_valid is False
        assert "does not exist" in error_msg

        # Invalid task ID (not an integer)
        is_valid, error_msg = validate_task_id("abc", existing_ids)
        assert is_valid is False
        assert "must be a valid integer" in error_msg

        # Negative task ID
        is_valid, error_msg = validate_task_id("-1", existing_ids)
        assert is_valid is False
        assert "must be a valid integer" in error_msg

    def test_validate_menu_choice_valid(self):
        """
        Test valid menu choices.
        """
        for choice in ["1", "2", "3", "4", "5", "6", "7"]:
            is_valid, error_msg = validate_menu_choice(choice)
            assert is_valid is True
            assert error_msg is None

    def test_validate_menu_choice_invalid(self):
        """
        Test invalid menu choices.
        """
        # Choice out of range (too low)
        is_valid, error_msg = validate_menu_choice("0")
        assert is_valid is False
        assert "must be between 1 and 7" in error_msg

        # Choice out of range (too high)
        is_valid, error_msg = validate_menu_choice("8")
        assert is_valid is False
        assert "must be between 1 and 7" in error_msg

        # Invalid choice (not an integer)
        is_valid, error_msg = validate_menu_choice("abc")
        assert is_valid is False
        assert "must be a valid integer" in error_msg

        # Invalid choice (float)
        is_valid, error_msg = validate_menu_choice("1.5")
        assert is_valid is False
        assert "must be a valid integer" in error_msg

    def test_validate_confirmation_input_valid(self):
        """
        Test valid confirmation inputs.
        """
        for valid_input in ["y", "n", "Y", "N", " y ", " n ", "Y ", "N "]:
            is_valid, error_msg = validate_confirmation_input(valid_input.strip())
            assert is_valid is True
            assert error_msg is None

    def test_validate_confirmation_input_invalid(self):
        """
        Test invalid confirmation inputs.
        """
        for invalid_input in ["yes", "no", "x", "a", "1", ""]:
            is_valid, error_msg = validate_confirmation_input(invalid_input)
            assert is_valid is False
            assert "must be 'y' or 'n'" in error_msg

    def test_validate_task_description_valid(self):
        """
        Test valid task descriptions.
        """
        # Valid descriptions
        test_cases = [
            "A valid description",
            "",  # Empty description is valid
            "   ",  # Whitespace-only description is valid
            "A" * 500,  # Reasonable length description
        ]

        for desc in test_cases:
            is_valid, error_msg = validate_task_description(desc)
            assert is_valid is True
            assert error_msg is None

    def test_validate_task_description_invalid(self):
        """
        Test invalid task descriptions (too long).
        """
        # Too long description
        long_desc = "A" * 1001  # Exceeds 1000 character limit
        is_valid, error_msg = validate_task_description(long_desc)
        assert is_valid is False
        assert "too long" in error_msg

    def test_is_valid_datetime_format_valid(self):
        """
        Test valid datetime formats.
        """
        valid_formats = [
            "2026-01-06 10:30:45",
            "1999-12-31 23:59:59",
            "2000-01-01 00:00:00",
            "2025-12-25 12:15:30"
        ]

        for dt_str in valid_formats:
            is_valid = is_valid_datetime_format(dt_str)
            assert is_valid is True

    def test_is_valid_datetime_format_invalid(self):
        """
        Test invalid datetime formats.
        """
        invalid_formats = [
            "2026-01-06",  # Missing time
            "2026/01/06 10:30:45",  # Wrong date separator
            "01-06-2026 10:30:45",  # Wrong date format
            "2026-01-06 10:30",  # Missing seconds
            "2026-01-06 25:30:45",  # Invalid hour
            "2026-01-06 10:60:45",  # Invalid minute
            "2026-01-06 10:30:60",  # Invalid second
            "invalid",  # Completely invalid
            "",  # Empty string
            "2026-1-6 10:30:45",  # Wrong padding
        ]

        for dt_str in invalid_formats:
            is_valid = is_valid_datetime_format(dt_str)
            assert is_valid is False