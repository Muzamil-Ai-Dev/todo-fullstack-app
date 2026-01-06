# Quickstart: Todo Application CLI

## Prerequisites
- Python 3.13+ installed
- UV package manager (optional, for dependency management)

## Setup
1. Clone or create the project structure:
```
todo-application/
├── src/
│   ├── models/
│   │   └── task.py
│   ├── services/
│   │   └── task_service.py
│   ├── cli/
│   │   └── main.py
│   └── lib/
│       └── validators.py
└── tests/
    ├── unit/
    ├── integration/
    └── contract/
```

2. Install dependencies (if any):
```
uv sync  # if using uv
# or
pip install -r requirements.txt  # if using pip
```

## Running the Application
```
cd todo-application
python src/cli/main.py
```

## Expected Behavior
1. Application starts and displays the main menu:
```
==== Todo Application ====
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task as Complete
6. Mark Task as Incomplete
7. Exit

Choose an option (1-7):
```

2. Select options 1-7 to perform corresponding actions
3. Application handles all errors gracefully and returns to main menu
4. Application exits cleanly when option 7 is selected

## Testing Strategy
The application follows a comprehensive testing approach to ensure deterministic behavior and error handling resilience:

### Unit Tests
- Test individual components (models, validators, service methods)
- Verify correct behavior of validation functions
- Test datetime handling and formatting

### Integration Tests
- Test CLI flow integration with service layer
- Verify error handling across component boundaries
- Test menu system behavior

### Contract Tests
- Validate that service contracts are fulfilled
- Ensure all constitution requirements are met
- Verify error recovery protocols

## Running Tests
Run the full test suite:
```
pytest tests/
```

Or run specific test types:
```
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests
pytest tests/contract/      # Contract tests
```

## Development Workflow
1. Implement models first (task.py)
2. Implement service layer (task_service.py)
3. Implement validation utilities (validators.py)
4. Implement CLI interface (main.py)
5. Write tests for each component
6. Run all tests before committing changes