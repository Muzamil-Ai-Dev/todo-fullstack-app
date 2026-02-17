# Research: AI-Powered Todo Chatbot

**Feature**: 005-ai-todo-chatbot
**Date**: 2026-02-17

## Research Tasks

### 1. Groq API Integration for LLM Responses

**Decision**: Use Groq API with `groq` Python SDK

**Rationale**:
- Free tier available with generous rate limits
- OpenAI-compatible API interface (easy migration)
- Fast inference with LPU (Language Processing Unit) architecture
- Supports models like `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`

**Alternatives Considered**:
| Option | Rejected Because |
|--------|------------------|
| OpenAI API | Paid service, cost constraint |
| Ollama (local) | Requires local GPU, deployment complexity |
| Hugging Face Inference | Rate limits, slower responses |
| Anthropic Claude | Paid service |

**Implementation Pattern**:
```python
from groq import Groq

client = Groq(api_key=settings.GROQ_API_KEY)
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "..."}]
)
```

---

### 2. MCP (Model Context Protocol) Server Implementation

**Decision**: Use Official MCP Python SDK

**Rationale**:
- Official SDK from Anthropic with active maintenance
- Clean decorator-based tool definition
- Built-in schema validation
- WebSocket and HTTP transport support

**Alternatives Considered**:
| Option | Rejected Because |
|--------|------------------|
| Custom tool calling | Not standardized, harder to maintain |
| LangChain tools | Heavier dependency, not MCP-compliant |
| OpenAI function calling | Vendor lock-in, doesn't match hackathon spec |

**Implementation Pattern**:
```python
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("todo-mcp-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(name="add_task", description="Create a new task", inputSchema={...}),
        # ... more tools
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "add_task":
        return await add_task(**arguments)
    # ... handle other tools
```

---

### 3. OpenAI Agents SDK with Groq Compatibility

**Decision**: Use OpenAI Agents SDK structure with Groq as base URL

**Rationale**:
- Hackathon spec requires OpenAI Agents SDK
- Groq provides OpenAI-compatible API endpoint
- Can use `base_url` parameter to redirect to Groq
- Agent orchestration patterns still work

**Implementation Pattern**:
```python
from openai import OpenAI

# Use Groq's OpenAI-compatible endpoint
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=settings.GROQ_API_KEY
)

# Agents SDK-style tool calling
tools = [
    {"type": "function", "function": {"name": "add_task", ...}},
    # ... more tools
]
```

---

### 4. Conversation State Management

**Decision**: Database-persisted conversations with Message history

**Rationale**:
- Stateless server requirement (FR-010)
- Conversation continuity (FR-011, FR-012)
- Server restart resilience (User Story 7)

**Database Schema**:
```sql
-- Conversations table
CREATE TABLE conversation (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL REFERENCES "user"(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Messages table
CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversation(id),
    user_id VARCHAR NOT NULL REFERENCES "user"(id),
    role VARCHAR NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_message_conversation ON message(conversation_id);
CREATE INDEX idx_conversation_user ON conversation(user_id);
```

---

### 5. Stateless Request Flow Design

**Decision**: Retrieve conversation history on each request, build context, process, persist, return

**Rationale**:
- Enables horizontal scaling (any server can handle any request)
- Survives server restarts
- Clean separation of concerns

**Request Flow**:
```
1. POST /api/{user_id}/chat
2. Validate user authentication (JWT)
3. Validate message length (500 chars max)
4. Get or create conversation
5. Fetch message history from DB
6. Build messages array for LLM (history + new message)
7. Store user message in DB
8. Call Groq API with tools
9. Agent invokes MCP tools as needed
10. Store assistant response in DB
11. Return response with conversation_id
```

---

### 6. Intent Recognition Strategy

**Decision**: Use LLM's native tool-calling for intent recognition

**Rationale**:
- No separate intent classifier needed
- LLM selects appropriate tool based on user message
- Handles variations in phrasing naturally
- Tool descriptions guide the LLM

**Tool Descriptions for Intent Mapping**:
```python
tools = [
    {
        "name": "add_task",
        "description": "Create a new todo task. Use when user wants to add, create, or remember something."
    },
    {
        "name": "list_tasks",
        "description": "List all tasks or filter by status. Use when user wants to see, show, or view tasks."
    },
    {
        "name": "complete_task",
        "description": "Mark a task as completed. Use when user says done, finished, or completed."
    },
    {
        "name": "delete_task",
        "description": "Delete a task. Use when user wants to remove, delete, or cancel a task."
    },
    {
        "name": "update_task",
        "description": "Update task title or description. Use when user wants to change or modify a task."
    }
]
```

---

### 7. Frontend Chat Interface

**Decision**: Custom React component with streaming consideration for future

**Rationale**:
- OpenAI ChatKit requires paid plan for production
- Custom component gives full control
- Can add streaming later with Server-Sent Events
- Consistent with existing UI patterns

**Component Structure**:
```
ChatInterface.tsx
├── MessageList (displays conversation history)
├── MessageInput (text input with send button)
├── MessageBubble (individual message display)
└── LoadingIndicator (while waiting for response)
```

---

## Resolved Clarifications

| Item | Resolution |
|------|------------|
| LLM Provider | Groq API (free tier) |
| Message limit | 500 characters |
| Title limit | 200 characters |
| Ambiguous task reference | List matches, ask user to specify |
| Unrecognized intent | Polite response + list commands |
| AI service unavailable | Specific error message |

## Technology Stack Summary

| Component | Technology | Notes |
|-----------|------------|-------|
| LLM | Groq API | Free tier, OpenAI-compatible |
| MCP Server | Official MCP SDK | Python implementation |
| Agent Framework | OpenAI SDK pattern | Redirected to Groq |
| Backend | FastAPI | Existing from Phase 2 |
| Database | Neon PostgreSQL | Existing from Phase 2 |
| ORM | SQLModel | Existing from Phase 2 |
| Auth | Better Auth (JWT) | Existing from Phase 2 |
| Frontend | Next.js | Existing from Phase 2 |
