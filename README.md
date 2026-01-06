# Todo Application CLI

A menu-driven CLI Todo application with in-memory storage built in Python.

## Overview

This is a command-line interface (CLI) todo application that allows users to manage tasks through a menu system. The application stores all tasks in memory only and provides a clean, guided user experience.

## Features

- Add new tasks with titles and optional descriptions
- View all tasks with their status and details
- Update existing tasks
- Delete tasks with confirmation
- Mark tasks as complete or incomplete
- Clean exit functionality
- Professional visual appearance with Rich formatting
- Enhanced menu display with borders and colors
- Professional task table display with aligned columns
- Consistent blue/gray color scheme throughout
- Improved error and success message formatting
- Enhanced user guidance with clear prompts

## Requirements

- Python 3.13+
- Rich library for enhanced CLI formatting (installed automatically via dependencies)

## Installation

1. Clone or download the repository
2. Navigate to the project directory
3. Install dependencies (if any) with `pip install -e .`

## Usage

Run the application using:
```
python src/cli/main.py
```

Or if installed as a package:
```
todo-app
```

## Menu Options

1. **Add Task** - Create a new task with title and optional description
2. **View Tasks** - Display all tasks with their status and details
3. **Update Task** - Modify an existing task's title or description
4. **Delete Task** - Remove a task with confirmation
5. **Mark Task as Complete** - Update task status to completed
6. **Mark Task as Incomplete** - Update task status to pending
7. **Exit** - Close the application

## Architecture

The application follows a clean architecture pattern:

- **Models**: Task entity definition (`src/models/task.py`)
- **Services**: Business logic for task operations (`src/services/task_service.py`)
- **CLI**: User interface and menu system (`src/cli/main.py`)
- **Lib**: Utility functions (`src/lib/`)
  - **Rich Utilities**: Rich formatting functions (`src/lib/rich_utils.py`)
  - **Theme Configuration**: Professional color scheme (`src/lib/theme.py`)

## Data Model

Each task contains:
- `id`: Auto-incremented unique identifier
- `title`: Required string (1-200 characters)
- `description`: Optional string
- `completed`: Boolean status
- `created_at`: Timestamp when task was created
- `updated_at`: Timestamp when task was last modified

## Error Handling

The application implements comprehensive error handling:
- All invalid inputs are caught and handled gracefully
- Users are returned to the main menu after errors
- No crashes occur under any circumstances
- Friendly error messages guide users

## Testing

To run tests:
```
pytest tests/
```

## License

MIT License