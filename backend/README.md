---
title: Todo Application Backend API
emoji: ✅
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# Todo Application Backend API

FastAPI backend for the Todo Application with the following features:

- User authentication with JWT
- Task CRUD operations
- PostgreSQL database support (Neon)
- **AI-powered chatbot for natural language task management**

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login user |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks |
| POST | `/api/tasks` | Create task |
| PUT | `/api/tasks/{id}` | Update task |
| DELETE | `/api/tasks/{id}` | Delete task |
| PATCH | `/api/tasks/{id}/toggle-complete` | Toggle completion |

### AI Chatbot (Phase 3)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/{user_id}/chat` | Send a chat message to AI assistant |
| GET | `/api/{user_id}/chat/conversations` | List all conversations |
| GET | `/api/{user_id}/chat/conversations/{id}` | Get conversation history |
| DELETE | `/api/{user_id}/chat/conversations/{id}` | Delete a conversation |

**Chat Example:**
```bash
curl -X POST "http://localhost:8000/api/{user_id}/chat" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```

**Response:**
```json
{
  "conversation_id": 1,
  "response": "I've created a new task 'Buy groceries' for you.",
  "tool_calls": [{"tool_name": "add_task", "arguments": {"title": "Buy groceries"}, "result": {...}}]
}
```

## Configuration

Set these secrets in Hugging Face Space settings:

- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET_KEY` - Secret key for JWT tokens
- `BETTER_AUTH_SECRET` - Secret for Better Auth
- `GROQ_API_KEY` - Groq API key for AI chatbot (free tier at console.groq.com)

## Health Check

- `GET /health` - Returns server health status
