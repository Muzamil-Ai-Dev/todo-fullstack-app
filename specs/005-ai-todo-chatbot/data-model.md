# Data Model: AI-Powered Todo Chatbot

**Feature**: 005-ai-todo-chatbot
**Date**: 2026-02-17

## Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────────┐       ┌─────────────┐
│    User     │       │  Conversation   │       │   Message   │
├─────────────┤       ├─────────────────┤       ├─────────────┤
│ id (PK)     │───┐   │ id (PK)         │───┐   │ id (PK)     │
│ email       │   │   │ user_id (FK)    │   │   │ conv_id(FK) │
│ name        │   │   │ created_at      │   │   │ user_id(FK) │
│ created_at  │   │   │ updated_at      │   │   │ role        │
└─────────────┘   │   └─────────────────┘   │   │ content     │
                  │                         │   │ created_at  │
                  │                         │   └─────────────┘
                  │                         │
                  └─────────────────────────┴─── One User has many Conversations
                                                One Conversation has many Messages

┌─────────────┐
│    Task     │  (EXISTING - from Phase 2)
├─────────────┤
│ id (PK)     │
│ user_id(FK) │
│ title       │
│ description │
│ completed   │
│ created_at  │
│ updated_at  │
└─────────────┘
```

## Entities

### 1. Conversation

Represents a chat session between a user and the AI assistant.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PK, AUTO_INCREMENT | Unique conversation identifier |
| user_id | VARCHAR(255) | FK → user.id, NOT NULL | Owner of the conversation |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When conversation started |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last message timestamp |

**Indexes**:
- `idx_conversation_user` on `user_id` - Fast lookup of user's conversations
- `idx_conversation_updated` on `updated_at` - Recent conversations query

**SQLModel Implementation**:
```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversation"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")
```

---

### 2. Message

Individual messages within a conversation, from user or assistant.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PK, AUTO_INCREMENT | Unique message identifier |
| conversation_id | INTEGER | FK → conversation.id, NOT NULL | Parent conversation |
| user_id | VARCHAR(255) | FK → user.id, NOT NULL | Owner of the message |
| role | VARCHAR(20) | NOT NULL, CHECK IN ('user', 'assistant') | Message sender role |
| content | TEXT | NOT NULL, MAX 500 chars | Message text content |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When message was sent |

**Indexes**:
- `idx_message_conversation` on `conversation_id` - Fetch all messages for a conversation
- `idx_message_created` on `created_at` - Chronological ordering

**SQLModel Implementation**:
```python
class Message(SQLModel, table=True):
    __tablename__ = "message"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", nullable=False)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    role: str = Field(nullable=False)  # 'user' or 'assistant'
    content: str = Field(nullable=False, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
    user: "User" = Relationship(back_populates="messages")
```

---

### 3. Task (EXISTING - from Phase 2)

Already implemented. Referenced by MCP tools for task operations.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PK, AUTO_INCREMENT | Unique task identifier |
| user_id | VARCHAR(255) | FK → user.id, NOT NULL | Task owner |
| title | VARCHAR(200) | NOT NULL, 1-200 chars | Task title |
| description | TEXT | NULLABLE, max 1000 chars | Task description |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP | NOT NULL | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL | Last update timestamp |

---

## Schema Schemas (Pydantic/SQLModel)

### Chat Request
```python
class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None  # Creates new if not provided
    message: str = Field(..., min_length=1, max_length=500)
```

### Chat Response
```python
class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[ToolCallInfo] = []

class ToolCallInfo(BaseModel):
    tool_name: str
    arguments: dict
    result: dict
```

### Conversation History
```python
class ConversationHistory(BaseModel):
    conversation_id: int
    messages: List[MessageRead]
    created_at: datetime
    updated_at: datetime

class MessageRead(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime
```

---

## State Transitions

### Conversation Lifecycle
```
[User sends first message]
        ↓
[New Conversation Created] ──→ [conversation_id returned]
        ↓
[Messages added] ──→ [updated_at refreshed]
        ↓
[User continues] ──→ [Messages appended]
        ↓
[Server restarts] ──→ [Conversation persists in DB]
        ↓
[User reconnects] ──→ [History fetched, context restored]
```

### Message Flow
```
[User Input] → Validate (500 chars) → Store (role='user')
                                           ↓
[Build Context] ← Fetch History ← [Get conversation_id]
                                           ↓
[LLM Response] → Tool Calls? → Execute MCP Tools
                                           ↓
[Store Response] (role='assistant') → Return to User
```

---

## Database Migration SQL

```sql
-- Create conversations table
CREATE TABLE IF NOT EXISTS conversation (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create messages table
CREATE TABLE IF NOT EXISTS message (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversation(id) ON DELETE CASCADE,
    user_id VARCHAR(255) NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_conversation_user ON conversation(user_id);
CREATE INDEX IF NOT EXISTS idx_conversation_updated ON conversation(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_message_conversation ON message(conversation_id);
CREATE INDEX IF NOT EXISTS idx_message_created ON message(created_at);

-- Update user table to add relationships (if needed)
-- This assumes user table already exists from Phase 2
```

---

## Data Volume Estimates

| Entity | Growth Rate | Storage per Row | Expected Volume |
|--------|-------------|-----------------|-----------------|
| Conversation | ~1/day/user | ~100 bytes | ~365/year/user |
| Message | ~20/day/user | ~300 bytes | ~7,300/year/user |
| Task | ~5/day/user | ~200 bytes | ~1,825/year/user |

For 50 concurrent users: ~1MB conversation data per month - negligible for Neon free tier.
