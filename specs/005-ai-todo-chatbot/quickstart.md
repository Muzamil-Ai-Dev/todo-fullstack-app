# Quickstart: AI-Powered Todo Chatbot

**Feature**: 005-ai-todo-chatbot
**Date**: 2026-02-17

## Prerequisites

- Python 3.13+
- Node.js 18+
- UV package manager
- Groq API key (free tier)
- Neon PostgreSQL database (existing from Phase 2)

## Environment Setup

### 1. Backend Environment Variables

Add to `backend/.env`:
```env
# Existing variables from Phase 2
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
BETTER_AUTH_SECRET=your-secret-key

# New variables for Phase 3
GROQ_API_KEY=gsk_your_groq_api_key_here
```

### 2. Get Groq API Key (Free)

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up / Log in
3. Navigate to API Keys
4. Create a new API key
5. Copy and add to `.env`

### 3. Install Dependencies

```bash
cd backend

# Add new dependencies
uv add groq mcp openai

# Or update pyproject.toml and run
uv sync
```

## Database Migration

Run the migration to create conversation and message tables:

```bash
cd backend

# Option 1: Using the init script (recommended)
python -c "from src.database.database import init_db; init_db()"

# Option 2: Manual SQL (run in Neon SQL editor)
# See specs/005-ai-todo-chatbot/data-model.md for SQL
```

## Running the Application

### Development Mode

```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Next.js application |
| Backend API | http://localhost:3000/api | API endpoints |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Chat Page | http://localhost:3000/chat | Chatbot interface |

## Testing the Chatbot

### 1. Authentication First

Before using the chat, users must be authenticated:
1. Go to http://localhost:3000
2. Sign up or sign in
3. Navigate to `/chat`

### 2. Basic Chat Flow

```bash
# Using curl (replace TOKEN with your JWT)
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```

### 3. Example Conversations

| User Says | Expected Response |
|-----------|-------------------|
| "Add a task to buy groceries" | Creates task, confirms creation |
| "Show me my tasks" | Lists all tasks with status |
| "Mark task 1 as complete" | Marks task complete, confirms |
| "Delete task 2" | Deletes task, confirms |
| "What's pending?" | Lists only incomplete tasks |
| "Hello" | Polite greeting + lists available commands |

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/{user_id}/chat | Send chat message |
| GET | /api/{user_id}/conversations | List conversations |
| GET | /api/{user_id}/conversations/{id} | Get conversation history |
| DELETE | /api/{user_id}/conversations/{id} | Delete conversation |

## MCP Tools

The chatbot exposes these tools to the AI agent:

| Tool | Purpose | Parameters |
|------|---------|------------|
| `add_task` | Create a new task | `title`, `description?` |
| `list_tasks` | List tasks | `status?` (all/pending/completed) |
| `complete_task` | Mark task complete | `task_id` |
| `delete_task` | Delete a task | `task_id` |
| `update_task` | Update task | `task_id`, `title?`, `description?` |

## Troubleshooting

### "AI service temporarily unavailable"
- Check GROQ_API_KEY is set correctly
- Verify Groq API status at status.groq.com
- Check rate limits (free tier has limits)

### "Unauthorized" errors
- Ensure JWT token is valid
- Check token hasn't expired
- Verify Authorization header format: `Bearer TOKEN`

### "Conversation not found"
- Conversation may have been deleted
- Try starting a new conversation (omit conversation_id)

### Database connection errors
- Verify DATABASE_URL is correct
- Check Neon database is running
- Ensure IP is whitelisted (if applicable)

## Deployment

### Backend (Hugging Face Spaces)

```bash
# Build and push
cd backend
# Create Dockerfile if needed
# Push to Hugging Face Space
```

### Frontend (Vercel)

```bash
cd frontend
vercel --prod
```

### Environment Variables (Production)

Set in Hugging Face Spaces / Vercel:
- `DATABASE_URL`
- `BETTER_AUTH_SECRET`
- `GROQ_API_KEY`
- `ENVIRONMENT=production`

## Next Steps

After quickstart validation:
1. Run `/sp.tasks` to generate implementation tasks
2. Implement backend components (models, services, MCP tools)
3. Implement frontend chat interface
4. Test with various natural language commands
5. Deploy to production
