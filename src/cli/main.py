from datetime import datetime
import sys
import os
# Add the src directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Rich library for enhanced CLI formatting
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt

from src.models.task import Task
from src.services.task_service import TaskService
from src.lib.validators import validate_task_title, validate_menu_choice, validate_confirmation_input
from src.lib.datetime_utils import format_datetime_display
from src.lib.rich_utils import formatter, compatibility
from src.lib.theme import get_color, validate_theme_consistency

# Initialize Rich console
console = Console()


def display_menu():
    """
    Display the main menu with options 1-7 exactly as specified.
    Enhanced with Rich formatting for professional appearance.
    """
    # Create menu content
    menu_content = (
        "[bold]1.[/bold] Add Task\n"
        "[bold]2.[/bold] View Tasks\n"
        "[bold]3.[/bold] Update Task\n"
        "[bold]4.[/bold] Delete Task\n"
        "[bold]5.[/bold] Mark Task as Complete\n"
        "[bold]6.[/bold] Mark Task as Incomplete\n"
        "[bold]7.[/bold] Exit"
    )

    # Create and display the menu panel
    menu_panel = formatter.create_menu_panel(menu_content)
    console.print(menu_panel)
    console.print("\nChoose an option (1-7):", end=" ")


def get_user_input(prompt: str = "") -> str:
    """
    Get input from the user with an optional prompt using Rich formatting.

    Args:
        prompt: Optional prompt to display before getting input

    Returns:
        User input as a string
    """
    if prompt:
        console.print(prompt, end="")
    return input().strip()


def display_error(message: str):
    """
    Display an error message to the user with professional formatting.

    Args:
        message: Error message to display
    """
    formatter.display_error(message)


def display_success(message: str):
    """
    Display a success message to the user with professional formatting.

    Args:
        message: Success message to display
    """
    formatter.display_success(message)


def add_task(service: TaskService):
    """
    Handle the Add Task functionality (Option 1) with Rich formatting.

    Args:
        service: TaskService instance to manage tasks
    """
    console.print("--- Add New Task ---", style="bold blue")

    while True:
        title = get_user_input("Enter task title: ")
        is_valid, error_msg = validate_task_title(title)

        if is_valid:
            break
        else:
            display_error(error_msg)

    description = get_user_input("Enter task description (optional): ")
    if not description.strip():
        description = None

    task = service.add_task(title, description)
    display_success(f"Task added successfully with ID #{task.id}")


def view_tasks(service: TaskService):
    """
    Handle the View Tasks functionality (Option 2) with Rich table formatting.

    Args:
        service: TaskService instance to manage tasks
    """
    tasks = service.get_all_tasks()

    if not tasks:
        console.print("No tasks found.", style="yellow")
        return

    # Create a Rich table for displaying tasks
    table = formatter.create_task_table()

    for task in tasks:
        # Format the status using the formatter
        status_text = formatter.format_status(task.completed)

        # Add row to the table
        table.add_row(
            str(task.id),
            task.title,
            task.description if task.description else "None",
            status_text,
            format_datetime_display(task.created_at),
            format_datetime_display(task.updated_at)
        )

    # Display the table
    console.print(table)


def update_task(service: TaskService):
    """
    Handle the Update Task functionality (Option 3) with Rich formatting.

    Args:
        service: TaskService instance to manage tasks
    """
    task_id_str = get_user_input("Enter task ID to update: ")

    try:
        task_id = int(task_id_str)
    except ValueError:
        display_error("Task ID must be a valid integer")
        return

    task = service.get_task(task_id)
    if not task:
        display_error(f"Task with ID {task_id} does not exist")
        return

    new_title = get_user_input("Enter new title (leave blank to keep current): ")
    if not new_title.strip():
        new_title = None  # Keep current title

    new_description = get_user_input("Enter new description (leave blank to keep current): ")
    if not new_description.strip():
        new_description = None  # Keep current description

    updated_task = service.update_task(task_id, new_title, new_description)
    if updated_task:
        display_success(f"Task #{updated_task.id} updated successfully.")
    else:
        display_error(f"Failed to update task with ID {task_id}")


def delete_task(service: TaskService):
    """
    Handle the Delete Task functionality (Option 4) with Rich formatting.

    Args:
        service: TaskService instance to manage tasks
    """
    task_id_str = get_user_input("Enter task ID to delete: ")

    try:
        task_id = int(task_id_str)
    except ValueError:
        display_error("Task ID must be a valid integer")
        return

    task = service.get_task(task_id)
    if not task:
        display_error(f"Task with ID {task_id} does not exist")
        return

    confirmation = get_user_input(f"Are you sure you want to delete task #{task_id}? (y/n): ")
    is_valid, error_msg = validate_confirmation_input(confirmation)

    if not is_valid:
        display_error(error_msg)
        return

    if confirmation.lower() in ['y', 'yes']:
        success = service.delete_task(task_id)
        if success:
            display_success(f"Task #{task_id} deleted successfully.")
        else:
            display_error(f"Failed to delete task with ID {task_id}")
    else:
        display_success("Delete operation cancelled.")


def mark_task_complete(service: TaskService):
    """
    Handle the Mark Task as Complete functionality (Option 5) with Rich formatting.

    Args:
        service: TaskService instance to manage tasks
    """
    task_id_str = get_user_input("Enter task ID to mark as complete: ")

    try:
        task_id = int(task_id_str)
    except ValueError:
        display_error("Task ID must be a valid integer")
        return

    task = service.get_task(task_id)
    if not task:
        display_error(f"Task with ID {task_id} does not exist")
        return

    if task.completed:
        display_error("Task is already completed.")
        return

    updated_task = service.mark_task_complete(task_id)
    if updated_task:
        display_success(f"Task #{updated_task.id} marked as completed.")
    else:
        display_error(f"Failed to mark task with ID {task_id} as completed")


def mark_task_incomplete(service: TaskService):
    """
    Handle the Mark Task as Incomplete functionality (Option 6) with Rich formatting.

    Args:
        service: TaskService instance to manage tasks
    """
    task_id_str = get_user_input("Enter task ID to mark as incomplete: ")

    try:
        task_id = int(task_id_str)
    except ValueError:
        display_error("Task ID must be a valid integer")
        return

    task = service.get_task(task_id)
    if not task:
        display_error(f"Task with ID {task_id} does not exist")
        return

    if not task.completed:
        display_error("Task is already pending.")
        return

    updated_task = service.mark_task_incomplete(task_id)
    if updated_task:
        display_success(f"Task #{updated_task.id} marked as pending.")
    else:
        display_error(f"Failed to mark task with ID {task_id} as pending")


def main():
    """
    Main function to run the Todo Application CLI with Rich formatting.
    """
    service = TaskService()

    # Validate theme consistency at startup
    if not validate_theme_consistency():
        console.print("Warning: Theme consistency issues detected", style="yellow")

    while True:
        try:
            display_menu()
            choice = get_user_input()

            # Validate menu choice
            is_valid, error_msg = validate_menu_choice(choice)
            if not is_valid:
                display_error(error_msg)
                continue  # Show menu again

            # Process the user's choice
            if choice == "1":
                add_task(service)
            elif choice == "2":
                view_tasks(service)
            elif choice == "3":
                update_task(service)
            elif choice == "4":
                delete_task(service)
            elif choice == "5":
                mark_task_complete(service)
            elif choice == "6":
                mark_task_incomplete(service)
            elif choice == "7":
                console.print("Thank you for using Todo Application. Goodbye!", style="bold green")
                break
            else:
                # This shouldn't happen due to validation, but just in case
                display_error(f"Invalid option: {choice}")

        except KeyboardInterrupt:
            console.print("\nThank you for using Todo Application. Goodbye!", style="bold green")
            break
        except Exception as e:
            display_error(f"An unexpected error occurred: {str(e)}")
            console.print("Please try again.", style="yellow")


if __name__ == "__main__":
    main()