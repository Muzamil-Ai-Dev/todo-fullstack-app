# Implementation Plan: AI-Powered Todo Chatbot

**Branch**: `005-ai-todo-chatbot` | **Date**: 2026-02-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-ai-todo-chatbot/spec.md`

## Summary

Build an AI-powered conversational interface for managing todo tasks through natural language. The chatbot will use Groq API (free tier) for LLM responses, MCP (Model Context Protocol) server architecture for tool exposure, and integrate with the existing Phase 2 FastAPI backend and Neon PostgreSQL database. The architecture follows a stateless design where conversation history is persisted to the database for context continuity.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI, SQLModel, Groq API, MCP SDK (Official), OpenAI Agents SDK (compatible with Groq)
**Storage**: Neon PostgreSQL (existing from Phase 2)
**Testing**: pytest
**Target Platform**: Linux server (Hugging Face Spaces), Vercel (frontend)
**Project Type**: Web application (existing monorepo with backend/ and frontend/)
**Performance Goals**: <5 seconds response time, 50 concurrent conversations
**Constraints**: Free-tier Groq API (no paid services), 500 char message limit, 200 char title limit
**Scale/Scope**: Single-user conversations, multi-tenant by user_id

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Spec-Driven Development | ✅ PASS | Spec created and clarified before implementation |
| Python-Only Technology | ✅ PASS | Backend remains Python; Frontend is Next.js (existing) |
| In-Memory Architecture | ⚠️ OVERRIDE | Phase 3 requires persistent storage (PostgreSQL) for conversations - this is a hackathon requirement |
| Menu-Driven CLI Interface | ⚠️ OVERRIDE | Phase 3 is a chatbot interface, not CLI - this is a hackathon requirement |
| Deterministic Behavior | ✅ PASS | Task operations are deterministic; AI responses guided by tools |
| Error Handling Resilience | ✅ PASS | All edge cases defined with graceful handling |

**Justification for Overrides**: This is Phase 3 of the hackathon which explicitly requires a web-based AI chatbot with database persistence. The constitution was written for Phase 1 (CLI app) and is being extended for this phase.

## Project Structure

### Documentation (this feature)

```text
specs/005-ai-todo-chatbot/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (API contracts)
│   └── chat-api.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task.py          # EXISTING - reuse
│   │   ├── user.py          # EXISTING - reuse
│   │   └── conversation.py  # NEW - Conversation & Message models
│   ├── services/
│   │   ├── task_service.py  # EXISTING - reuse
│   │   ├── auth.py          # EXISTING - reuse
│   │   └── chat_service.py  # NEW - AI agent orchestration
│   ├── mcp/
│   │   ├── __init__.py      # NEW
│   │   ├── server.py        # NEW - MCP server setup
│   │   └── tools.py         # NEW - MCP tool definitions
│   ├── api/
│   │   ├── tasks.py         # EXISTING - reuse
│   │   ├── auth.py          # EXISTING - reuse
│   │   └── chat.py          # NEW - chat endpoint
│   ├── schemas/
│   │   ├── task.py          # EXISTING - reuse
│   │   ├── user.py          # EXISTING - reuse
│   │   └── chat.py          # NEW - request/response schemas
│   └── config/
│       └── settings.py      # UPDATE - add Groq API key
├── main.py                  # UPDATE - add chat router
└── tests/
    ├── test_chat.py         # NEW
    └── test_mcp_tools.py    # NEW

frontend/
├── src/
│   ├── app/
│   │   └── chat/            # NEW - chat page
│   │       └── page.tsx
│   ├── components/
│   │   ├── ChatInterface/   # NEW - chat UI component
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── ChatInterface.types.ts
│   │   │   └── index.ts
│   │   └── MessageBubble/   # NEW - message display
│   └── lib/
│       └── api.ts           # UPDATE - add chat API client
└── ...
```

**Structure Decision**: Extend existing backend/frontend monorepo structure. Add new `mcp/` module for MCP server implementation, `models/conversation.py` for new entities, and `app/chat/` page in frontend.

## Complexity Tracking

> **Violations justified due to hackathon Phase 3 requirements**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| MCP Server Architecture | Required by hackathon spec | Direct function calls insufficient - MCP enables tool abstraction for AI agents |
| Groq API Integration | Free-tier requirement | OpenAI Agents SDK requires paid API; Groq provides free alternative |
| Conversation Persistence | Stateless server requirement | In-memory would lose context on restart, violating FR-010 to FR-012 |

## Key Architectural Decisions

### 1. Groq API with OpenAI-Compatible Interface
Groq API provides an OpenAI-compatible API, allowing use of standard OpenAI SDK patterns with a base URL change.

### 2. MCP Tools Architecture
MCP tools will be implemented as Python functions that the AI agent can invoke. Each tool wraps existing task_service functions.

### 3. Stateless Request Flow
```
User Message → Chat Endpoint → Fetch Conversation History →
Build Context → Call Groq API → Agent Invokes MCP Tools →
Store Messages → Return Response
```

### 4. OpenAI Agents SDK Compatibility
Using OpenAI Agents SDK structure but pointing to Groq API endpoint for cost-free LLM calls.

## Dependencies to Add

```toml
# pyproject.toml additions
groq = ">=0.4.0"           # Groq API client
mcp = ">=1.0.0"            # Official MCP SDK
openai = ">=1.0.0"         # For Agents SDK structure (Groq-compatible)
```
