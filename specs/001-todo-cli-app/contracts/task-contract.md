# Task Contract

## Purpose
This contract defines the expected behavior and interface for task operations in the Todo Application CLI. All operations must comply with the constitution requirements for deterministic behavior, error handling resilience, and user-friendly messaging.

## Task Entity Contract

### Properties
- `id`: integer, auto-incremented unique identifier
- `title`: string, 1-200 characters, required
- `description`: string or null, optional
- `completed`: boolean, default false
- `created_at`: datetime in ISO 8601 format (YYYY-MM-DD HH:MM:SS)
- `updated_at`: datetime in ISO 8601 format (YYYY-MM-DD HH:MM:SS)

### Creation Contract
- When a task is created:
  - `id` is auto-assigned as next available integer starting from 1
  - `title` is set to provided value (1-200 chars)
  - `description` is set to provided value or null if not provided
  - `completed` is set to false
  - `created_at` is set to current timestamp in ISO 8601 format
  - `updated_at` is set to current timestamp in ISO 8601 format

### Update Contract
- When a task is updated:
  - `updated_at` is updated to current timestamp in ISO 8601 format
  - Only specified fields are changed
  - Unspecified fields remain unchanged
  - `id` and `created_at` are immutable

### Completion Status Contract
- When a task is marked complete:
  - `completed` is set to true
  - `updated_at` is updated to current timestamp in ISO 8601 format
- When a task is marked incomplete:
  - `completed` is set to false
  - `updated_at` is updated to current timestamp in ISO 8601 format

## Service Contract

### Add Task
- Input: title (string, 1-200 chars), description (optional string)
- Output: Task object with all properties populated
- Errors: Invalid title length, empty title
- Validation: Title must be 1-200 characters, non-empty

### View Tasks
- Input: none
- Output: List of Task objects sorted by ID ascending
- Errors: none
- Format: Tasks displayed in exact format specified in requirements with [✓] or [ ] status symbols

### Update Task
- Input: task ID, new title (optional), new description (optional)
- Output: Updated Task object
- Errors: Task not found, invalid ID
- Validation: Task ID must exist, blank inputs leave fields unchanged

### Delete Task
- Input: task ID
- Output: Boolean success indicator
- Errors: Task not found, invalid ID
- Confirmation: Requires 'y'/'n' confirmation before deletion

### Mark Complete/Incomplete
- Input: task ID
- Output: Updated Task object
- Errors: Task not found, invalid ID, already in requested state
- Validation: Must not already be in requested state

## Validation Contract
- All inputs must be validated before processing according to constitution requirements
- Error messages must be user-friendly and match exact text specified in requirements
- Invalid operations must not modify data
- All operations must return to main menu after completion or error
- Validation rules:
  - Task titles: 1-200 characters, no empty values
  - Task IDs: Must exist in current task list
  - Menu selections: Integers 1-7 only
  - Confirmation inputs: 'y'/'n' or 'Y'/'N' only
  - Numeric inputs: Within expected ranges

## Error Handling Contract
- No crashes under any circumstances
- All errors must result in user-friendly messages
- Application must always return to main menu after error
- Clean state recovery required for all error conditions
- Error recovery protocol: Display error message, return to main menu, maintain all existing data

## Deterministic Behavior Contract
- Same inputs must always produce same outputs
- State changes must be predictable and consistent
- Menu must display options 1-7 exactly as specified
- Application must show menu immediately upon startup
- All timestamps use consistent format throughout the session