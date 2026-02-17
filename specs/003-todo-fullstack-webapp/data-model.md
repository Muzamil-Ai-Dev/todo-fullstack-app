# Data Model: Todo Application Full-Stack Web Application

## Entity: User

### Attributes
- **id**: String (Primary Key)
  - Description: Unique identifier for the user
  - Constraints: Auto-generated UUID, required
- **email**: String (Unique)
  - Description: User's email address for authentication
  - Constraints: Required, valid email format, unique across all users
- **name**: String
  - Description: User's display name
  - Constraints: Required, 1-100 characters
- **password_hash**: String
  - Description: Hashed password for authentication
  - Constraints: Required, securely hashed
- **created_at**: DateTime (Timestamp)
  - Description: Timestamp when user account was created
  - Constraints: Auto-generated, required
- **updated_at**: DateTime (Timestamp)
  - Description: Timestamp when user account was last updated
  - Constraints: Auto-generated, updated on changes

### Relationships
- **tasks**: One-to-Many (User → Task)
  - Description: Collection of tasks owned by this user
  - Cardinality: One user can have many tasks

### Validation Rules
- Email must follow standard email format
- Email must be unique across all users
- Name must be between 1-100 characters
- Password must meet security requirements (handled by Better Auth)

## Entity: Task

### Attributes
- **id**: Integer (Primary Key, Auto-incremented)
  - Description: Unique identifier for the task
  - Constraints: Auto-generated, required
- **user_id**: String (Foreign Key)
  - Description: Reference to the user who owns this task
  - Constraints: Required, must reference an existing User.id
- **title**: String
  - Description: Title or brief description of the task
  - Constraints: Required, 1-200 characters
- **description**: String (Optional)
  - Description: Detailed description of the task
  - Constraints: Optional, maximum 1000 characters if provided
- **completed**: Boolean
  - Description: Whether the task is completed
  - Constraints: Required, default value is False
- **created_at**: DateTime (Timestamp)
  - Description: Timestamp when task was created
  - Constraints: Auto-generated, required
- **updated_at**: DateTime (Timestamp)
  - Description: Timestamp when task was last updated
  - Constraints: Auto-generated, updated on changes

### Relationships
- **user**: Many-to-One (Task → User)
  - Description: The user who owns this task
  - Cardinality: Many tasks belong to one user

### Validation Rules
- Title must be between 1-200 characters
- Description, if provided, must be maximum 1000 characters
- User_id must reference an existing user
- Completed must be a boolean value (true/false)
- User isolation: A task can only be accessed by its owner

## Database Schema Design

### Tables
```
users
├── id (VARCHAR PRIMARY KEY)
├── email (VARCHAR UNIQUE NOT NULL)
├── name (VARCHAR NOT NULL)
├── password_hash (VARCHAR NOT NULL)
├── created_at (TIMESTAMP NOT NULL)
└── updated_at (TIMESTAMP NOT NULL)

tasks
├── id (INTEGER PRIMARY KEY)
├── user_id (VARCHAR REFERENCES users(id))
├── title (VARCHAR NOT NULL)
├── description (TEXT)
├── completed (BOOLEAN NOT NULL DEFAULT FALSE)
├── created_at (TIMESTAMP NOT NULL)
└── updated_at (TIMESTAMP NOT NULL)
```

### Indexes
- **users.email_idx**: Index on email column for fast authentication lookups
- **tasks.user_id_idx**: Index on user_id column for efficient user-specific queries
- **tasks.completed_idx**: Index on completed column for efficient filtering
- **tasks.created_at_idx**: Index on created_at column for chronological ordering

### Constraints
- **FK_tasks_user_id**: Foreign key constraint ensuring user_id references valid user
- **CK_tasks_title_length**: Check constraint ensuring title is 1-200 characters
- **CK_tasks_desc_length**: Check constraint ensuring description is ≤1000 characters if provided
- **NN_tasks_required_fields**: NOT NULL constraints on all required fields

## State Transitions

### Task State Transitions
- **Active → Completed**: When user marks task as complete
- **Completed → Active**: When user unmarks task as complete
- **Any → Deleted**: When user deletes task (permanent deletion)

### Validation Scenarios
1. **Task Creation**: Validate title length, user exists, required fields present
2. **Task Update**: Validate title length, user owns task, allowed field changes
3. **Task Completion**: Validate user owns task, task exists
4. **Task Deletion**: Validate user owns task, task exists, confirmation received

## API Data Contracts

### Request/Response Objects

#### Task Creation Request
```json
{
  "title": "string (required, 1-200 chars)",
  "description": "string (optional, max 1000 chars)"
}
```

#### Task Response Object
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

#### Task Update Request
```json
{
  "title": "string (optional, 1-200 chars)",
  "description": "string (optional, max 1000 chars)",
  "completed": "boolean (optional)"
}
```

## Entity Lifecycle

### User Lifecycle
1. **Registration**: User creates account with email, name, password
2. **Authentication**: User logs in with email and password, receives JWT token
3. **Active Period**: User performs CRUD operations on their tasks
4. **Logout/Session Expiry**: JWT token expires, user must re-authenticate
5. **Account Deletion**: User can request account deletion (future feature)

### Task Lifecycle
1. **Creation**: User creates task with title and optional description
2. **Modification**: User updates task details or completion status
3. **Completion**: User marks task as complete
4. **Deletion**: User deletes task permanently