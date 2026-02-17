"""
MCP Tools implementation for the AI-powered todo chatbot.

These tools wrap the existing task_service functions and provide
the interface that the AI agent uses to perform task operations.
"""

from typing import Dict, Any, List, Optional
from sqlmodel import Session
from ..services.task_service import TaskService
from ..models.task import TaskRead, TaskCreate, TaskUpdate


def add_task(
    session: Session,
    user_id: str,
    title: str,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new todo task.

    Args:
        session: Database session
        user_id: ID of the user creating the task
        title: Task title (max 200 chars)
        description: Optional task description

    Returns:
        Dictionary with task creation result
    """
    try:
        # Validate title length
        if len(title) > 200:
            return {
                "success": False,
                "error": "Task title must be 200 characters or less"
            }

        # Create TaskCreate model for the service
        task_create = TaskCreate(title=title, description=description)

        task = TaskService.create_task(
            session=session,
            user_id=user_id,
            task_create=task_create
        )

        return {
            "success": True,
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def list_tasks(
    session: Session,
    user_id: str,
    status: str = "all"
) -> Dict[str, Any]:
    """
    List tasks for a user with optional status filter.

    Args:
        session: Database session
        user_id: ID of the user
        status: Filter by 'all', 'pending', or 'completed'

    Returns:
        Dictionary with list of tasks
    """
    try:
        tasks = TaskService.get_tasks_by_user(session=session, user_id=user_id)

        # Filter by status
        if status == "pending":
            tasks = [t for t in tasks if not t.completed]
        elif status == "completed":
            tasks = [t for t in tasks if t.completed]

        # Format tasks for response
        task_list = [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "completed": t.completed,
                "created_at": t.created_at.isoformat() if t.created_at else None
            }
            for t in tasks
        ]

        return {
            "success": True,
            "count": len(task_list),
            "tasks": task_list
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def complete_task(
    session: Session,
    user_id: str,
    task_id: int
) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        session: Database session
        user_id: ID of the user
        task_id: ID of the task to complete

    Returns:
        Dictionary with completion result
    """
    try:
        # Use TaskUpdate model
        task_update = TaskUpdate(completed=True)

        updated_task = TaskService.update_task(
            session=session,
            task_id=task_id,
            user_id=user_id,
            task_update=task_update
        )

        if not updated_task:
            return {
                "success": False,
                "error": f"Task with ID {task_id} not found or doesn't belong to you"
            }

        return {
            "success": True,
            "task_id": updated_task.id,
            "title": updated_task.title,
            "completed": updated_task.completed
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def delete_task(
    session: Session,
    user_id: str,
    task_id: int
) -> Dict[str, Any]:
    """
    Delete a task.

    Args:
        session: Database session
        user_id: ID of the user
        task_id: ID of the task to delete

    Returns:
        Dictionary with deletion result
    """
    try:
        # Get task first to return its title
        from ..models.task import Task
        from sqlmodel import select
        stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(stmt).first()

        if not task:
            return {
                "success": False,
                "error": f"Task with ID {task_id} not found or doesn't belong to you"
            }

        title = task.title

        deleted = TaskService.delete_task(session=session, task_id=task_id, user_id=user_id)

        if not deleted:
            return {
                "success": False,
                "error": f"Could not delete task with ID {task_id}"
            }

        return {
            "success": True,
            "task_id": task_id,
            "title": title
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def update_task(
    session: Session,
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update a task's title or description.

    Args:
        session: Database session
        user_id: ID of the user
        task_id: ID of the task to update
        title: New title (optional)
        description: New description (optional)

    Returns:
        Dictionary with update result
    """
    try:
        # Validate title length if provided
        if title and len(title) > 200:
            return {
                "success": False,
                "error": "Task title must be 200 characters or less"
            }

        # Create TaskUpdate model with only provided fields
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description

        task_update = TaskUpdate(**update_data)

        updated_task = TaskService.update_task(
            session=session,
            task_id=task_id,
            user_id=user_id,
            task_update=task_update
        )

        if not updated_task:
            return {
                "success": False,
                "error": f"Task with ID {task_id} not found or doesn't belong to you"
            }

        return {
            "success": True,
            "task_id": updated_task.id,
            "title": updated_task.title,
            "description": updated_task.description,
            "completed": updated_task.completed
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_all_tools() -> List[Dict[str, Any]]:
    """
    Get list of all available tool names.

    Returns:
        List of tool names
    """
    return ["add_task", "list_tasks", "complete_task", "delete_task", "update_task"]


def execute_tool(
    session: Session,
    user_id: str,
    tool_name: str,
    arguments: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute a tool by name with the given arguments.

    Args:
        session: Database session
        user_id: ID of the user
        tool_name: Name of the tool to execute
        arguments: Tool arguments

    Returns:
        Tool execution result
    """
    tool_map = {
        "add_task": add_task,
        "list_tasks": list_tasks,
        "complete_task": complete_task,
        "delete_task": delete_task,
        "update_task": update_task
    }

    if tool_name not in tool_map:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }

    tool_func = tool_map[tool_name]

    # Add session and user_id to arguments
    args = {"session": session, "user_id": user_id}
    args.update(arguments)

    # Remove session and user_id from args if they exist in arguments (they shouldn't)
    # and call with positional/keyword args properly
    return tool_func(
        session=session,
        user_id=user_id,
        **{k: v for k, v in arguments.items() if k not in ["session", "user_id"]}
    )
