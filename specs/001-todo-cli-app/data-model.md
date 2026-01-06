# Data Model: Todo Application CLI

## Entity: Task

### Fields
- **id**: Integer (auto-incremented unique identifier)
  - Type: int
  - Constraints: Positive integer, unique across all tasks, auto-incremented from 1
  - Required: Yes

- **title**: String (task title/description)
  - Type: str
  - Constraints: 1-200 characters, no empty values allowed
  - Required: Yes

- **description**: String (optional task description)
  - Type: str or None
  - Constraints: Optional field, can be None or empty string
  - Required: No

- **completed**: Boolean (completion status)
  - Type: bool
  - Constraints: True for completed, False for pending
  - Required: Yes, defaults to False

- **created_at**: DateTime (creation timestamp)
  - Type: datetime
  - Format: ISO 8601 format YYYY-MM-DD HH:MM:SS
  - Constraints: Set when task is created, immutable after creation
  - Required: Yes

- **updated_at**: DateTime (last modification timestamp)
  - Type: datetime
  - Format: ISO 8601 format YYYY-MM-DD HH:MM:SS
  - Constraints: Set when task is created and updated on any modification
  - Required: Yes

### Validation Rules
- Title must be 1-200 characters (no empty titles)
- ID must be positive integer and unique
- Completed status must be boolean (True/False)
- Timestamps must follow ISO 8601 format
- All required fields must be present when creating a task

### State Transitions
- New task: completed=False, created_at and updated_at set to current time
- Update task: title/description changed, updated_at updated to current time
- Mark complete: completed=True, updated_at updated to current time
- Mark incomplete: completed=False, updated_at updated to current time

### Relationships
- No relationships with other entities (standalone entity)
- Stored in-memory using dictionary with ID as key for efficient lookup