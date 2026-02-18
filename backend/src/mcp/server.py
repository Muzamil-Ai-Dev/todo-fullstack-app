"""
MCP Server setup for the AI-powered todo chatbot.

This module provides the MCP server configuration that exposes
task management tools to the AI agent.
"""

from typing import List, Dict, Any

# Tool definitions for Groq/OpenAI function calling
# These define the interface that the AI agent uses to invoke task operations

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new todo task. Use when user wants to add, create, or remember something.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the task (max 200 characters)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description or notes for the task"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks or filter by status. Use when user wants to see, show, or view tasks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter tasks by status: 'all', 'pending', or 'completed'"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed or incomplete. Use when user says done, finished, completed, or wants to mark incomplete/uncomplete.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to mark as complete or incomplete"
                    },
                    "completed": {
                        "type": "boolean",
                        "description": "True to mark as complete, False to mark as incomplete. Defaults to True.",
                        "default": True
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task. Use when user wants to remove, delete, or cancel a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update task title or description. Use when user wants to change or modify a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title for the task (optional)"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description for the task (optional)"
                    }
                },
                "required": ["task_id"]
            }
        }
    }
]


def get_tool_definitions() -> List[Dict[str, Any]]:
    """
    Get the list of MCP tool definitions for Groq/OpenAI function calling.

    Returns:
        List of tool definition dictionaries
    """
    return TOOL_DEFINITIONS
