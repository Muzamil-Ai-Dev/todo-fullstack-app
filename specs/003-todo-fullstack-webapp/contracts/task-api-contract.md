# API Contract: Task Management Endpoints

## Overview
This document defines the API contract for task management endpoints in the Todo Application Full-Stack Web Application. All endpoints require JWT authentication in the Authorization header.

## Common Headers
- `Authorization: Bearer {jwt_token}` (Required for all endpoints)
- `Content-Type: application/json` (For POST/PUT/PATCH requests)

## Authentication Endpoints

### Register User
- **Endpoint**: `POST /api/auth/register`
- **Description**: Register a new user account
- **Request**:
  ```json
  {
    "email": "string (required)",
    "name": "string (required, 1-100 chars)",
    "password": "string (required, secure password)"
  }
  ```
- **Response**:
  - `201 Created`: User registered successfully
  - `400 Bad Request`: Invalid input data
  - `409 Conflict`: Email already exists

### Login User
- **Endpoint**: `POST /api/auth/login`
- **Description**: Authenticate user and return JWT token
- **Request**:
  ```json
  {
    "email": "string (required)",
    "password": "string (required)"
  }
  ```
- **Response**:
  - `200 OK`: Authentication successful, returns token
  - `401 Unauthorized`: Invalid credentials

## Task Management Endpoints

### Get User's Tasks
- **Endpoint**: `GET /api/tasks`
- **Description**: Retrieve all tasks for the authenticated user
- **Query Parameters**:
  - `status` (optional): Filter by status ("all", "pending", "completed")
  - `limit` (optional): Number of tasks to return (default: 50)
  - `offset` (optional): Offset for pagination (default: 0)
- **Response**:
  - `200 OK`:
    ```json
    {
      "tasks": [
        {
          "id": "integer",
          "user_id": "string",
          "title": "string",
          "description": "string or null",
          "completed": "boolean",
          "created_at": "timestamp",
          "updated_at": "timestamp"
        }
      ],
      "total_count": "integer"
    }
    ```
  - `401 Unauthorized`: Invalid or expired JWT token

### Create Task
- **Endpoint**: `POST /api/tasks`
- **Description**: Create a new task for the authenticated user
- **Request Body**:
  ```json
  {
    "title": "string (required, 1-200 chars)",
    "description": "string (optional, max 1000 chars)"
  }
  ```
- **Response**:
  - `201 Created`:
    ```json
    {
      "id": "integer",
      "user_id": "string",
      "title": "string",
      "description": "string or null",
      "completed": "boolean",
      "created_at": "timestamp",
      "updated_at": "timestamp"
    }
    ```
  - `400 Bad Request`: Invalid input data
  - `401 Unauthorized`: Invalid or expired JWT token

### Get Specific Task
- **Endpoint**: `GET /api/tasks/{task_id}`
- **Description**: Retrieve a specific task by ID for the authenticated user
- **Path Parameter**: `task_id` (integer)
- **Response**:
  - `200 OK`:
    ```json
    {
      "id": "integer",
      "user_id": "string",
      "title": "string",
      "description": "string or null",
      "completed": "boolean",
      "created_at": "timestamp",
      "updated_at": "timestamp"
    }
    ```
  - `401 Unauthorized`: Invalid or expired JWT token
  - `403 Forbidden`: User does not own this task
  - `404 Not Found`: Task does not exist

### Update Task
- **Endpoint**: `PUT /api/tasks/{task_id}`
- **Description**: Update an existing task for the authenticated user
- **Path Parameter**: `task_id` (integer)
- **Request Body**:
  ```json
  {
    "title": "string (optional, 1-200 chars)",
    "description": "string (optional, max 1000 chars)",
    "completed": "boolean (optional)"
  }
  ```
- **Response**:
  - `200 OK`:
    ```json
    {
      "id": "integer",
      "user_id": "string",
      "title": "string",
      "description": "string or null",
      "completed": "boolean",
      "created_at": "timestamp",
      "updated_at": "timestamp"
    }
    ```
  - `400 Bad Request`: Invalid input data
  - `401 Unauthorized`: Invalid or expired JWT token
  - `403 Forbidden`: User does not own this task
  - `404 Not Found`: Task does not exist

### Delete Task
- **Endpoint**: `DELETE /api/tasks/{task_id}`
- **Description**: Delete a specific task by ID for the authenticated user
- **Path Parameter**: `task_id` (integer)
- **Response**:
  - `204 No Content`: Task successfully deleted
  - `401 Unauthorized`: Invalid or expired JWT token
  - `403 Forbidden`: User does not own this task
  - `404 Not Found`: Task does not exist

### Toggle Task Completion
- **Endpoint**: `PATCH /api/tasks/{task_id}/toggle-complete`
- **Description**: Toggle the completion status of a task
- **Path Parameter**: `task_id` (integer)
- **Response**:
  - `200 OK`:
    ```json
    {
      "id": "integer",
      "user_id": "string",
      "title": "string",
      "description": "string or null",
      "completed": "boolean",
      "created_at": "timestamp",
      "updated_at": "timestamp"
    }
    ```
  - `401 Unauthorized`: Invalid or expired JWT token
  - `403 Forbidden`: User does not own this task
  - `404 Not Found`: Task does not exist

## Error Response Format
All error responses follow this format:
```json
{
  "detail": "string - Error message describing the issue"
}
```

## Authentication Requirements
All task management endpoints require a valid JWT token in the Authorization header. The token must correspond to the user who owns the tasks being accessed. Users can only access their own tasks.

## Validation Rules
- All string fields are trimmed of leading/trailing whitespace
- Title must be 1-200 characters
- Description must be 0-1000 characters
- User ID in token must match the user ID associated with the task
- Task ID must exist and belong to the authenticated user