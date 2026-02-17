# Tasks: AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/005-ai-todo-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Based on existing monorepo structure from Phase 2

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency setup

- [x] T001 Add groq, mcp, openai dependencies to backend/pyproject.toml
- [x] T002 [P] Add GROQ_API_KEY to backend/src/config/settings.py
- [x] T003 [P] Create backend/src/mcp/__init__.py module initialization

**Checkpoint**: Dependencies installed, environment configured

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Models

- [x] T004 [P] Create Conversation model in backend/src/models/conversation.py
- [x] T005 [P] Create Message model in backend/src/models/conversation.py
- [x] T006 Update User model relationships in backend/src/models/user.py for conversations/messages

### Chat Schemas

- [x] T007 [P] Create ChatRequest schema in backend/src/schemas/chat.py
- [x] T008 [P] Create ChatResponse schema in backend/src/schemas/chat.py
- [x] T009 [P] Create ToolCallInfo schema in backend/src/schemas/chat.py
- [x] T010 [P] Create ConversationHistory and MessageRead schemas in backend/src/schemas/chat.py

### Database Migration

- [x] T011 Create database migration script for conversation and message tables in backend/init_db.py

### MCP Tools Foundation

- [x] T012 Create MCP server setup in backend/src/mcp/server.py
- [x] T013 Define MCP tool schemas (add_task, list_tasks, complete_task, delete_task, update_task) in backend/src/mcp/tools.py

### Chat Service Foundation

- [x] T014 Create ChatService class skeleton in backend/src/services/chat_service.py with Groq client initialization

### Chat API Foundation

- [x] T015 Create chat router skeleton in backend/src/api/chat.py
- [x] T016 Register chat router in backend/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Create Tasks via Natural Language (Priority: P1) 🎯 MVP

**Goal**: Users can add new tasks by telling the chatbot in natural language

**Independent Test**: Send "Add a task to buy groceries" and verify task appears in user's task list

### Implementation for User Story 1

- [x] T017 [US1] Implement add_task MCP tool in backend/src/mcp/tools.py (wraps task_service.create_task)
- [x] T018 [US1] Implement conversation creation logic in backend/src/services/chat_service.py
- [x] T019 [US1] Implement message persistence (user message) in backend/src/services/chat_service.py
- [x] T020 [US1] Implement Groq API call with add_task tool in backend/src/services/chat_service.py
- [x] T021 [US1] Implement message persistence (assistant response) in backend/src/services/chat_service.py
- [x] T022 [US1] Implement POST /api/{user_id}/chat endpoint in backend/src/api/chat.py
- [x] T023 [US1] Add input validation (500 char limit) in backend/src/api/chat.py
- [x] T024 [US1] Add authentication middleware to chat endpoint in backend/src/api/chat.py

### Frontend for User Story 1

- [x] T025 [P] [US1] Create ChatInterface component in frontend/src/components/ChatInterface/ChatInterface.tsx
- [x] T026 [P] [US1] Create ChatInterface types in frontend/src/components/ChatInterface/ChatInterface.types.ts
- [x] T027 [P] [US1] Create MessageBubble component in frontend/src/components/MessageBubble/MessageBubble.tsx
- [x] T028 [US1] Create chat page at frontend/src/app/chat/page.tsx
- [x] T029 [US1] Add chat API client function in frontend/src/lib/api.ts

**Checkpoint**: User Story 1 complete - users can create tasks via natural language

---

## Phase 4: User Story 2 - View and List Tasks (Priority: P1)

**Goal**: Users can ask to see their tasks with optional status filters

**Independent Test**: Send "Show me my tasks" or "What's pending?" and verify correct task list displayed

### Implementation for User Story 2

- [x] T030 [US2] Implement list_tasks MCP tool in backend/src/mcp/tools.py with status filter support
- [x] T031 [US2] Add list_tasks tool to Groq API call in backend/src/services/chat_service.py
- [x] T032 [US2] Update tool calling logic to handle list_tasks response formatting in backend/src/services/chat_service.py

**Checkpoint**: User Stories 1 AND 2 complete - users can create and view tasks

---

## Phase 5: User Story 3 - Mark Tasks as Complete (Priority: P1)

**Goal**: Users can mark tasks complete by telling the chatbot

**Independent Test**: Send "Mark task 3 as complete" and verify task status changes

### Implementation for User Story 3

- [x] T033 [US3] Implement complete_task MCP tool in backend/src/mcp/tools.py
- [x] T034 [US3] Add complete_task tool to Groq API call in backend/src/services/chat_service.py
- [x] T035 [US3] Implement task-not-found error handling in backend/src/services/chat_service.py

**Checkpoint**: User Stories 1, 2, AND 3 complete - core task operations via chat

---

## Phase 6: User Story 4 - Delete Tasks via Natural Language (Priority: P2)

**Goal**: Users can delete tasks through natural language

**Independent Test**: Send "Delete task 2" and verify task is removed

### Implementation for User Story 4

- [x] T036 [US4] Implement delete_task MCP tool in backend/src/mcp/tools.py
- [x] T037 [US4] Add delete_task tool to Groq API call in backend/src/services/chat_service.py

**Checkpoint**: User Stories 1-4 complete

---

## Phase 7: User Story 5 - Update Task Details (Priority: P2)

**Goal**: Users can modify task titles or descriptions

**Independent Test**: Send "Change task 1 to 'Call mom tonight'" and verify task updated

### Implementation for User Story 5

- [x] T038 [US5] Implement update_task MCP tool in backend/src/mcp/tools.py
- [x] T039 [US5] Add update_task tool to Groq API call in backend/src/services/chat_service.py

**Checkpoint**: User Stories 1-5 complete - all task CRUD via chat

---

## Phase 8: User Story 6 - Maintain Conversation Context (Priority: P2)

**Goal**: Chatbot remembers conversation for context-aware responses

**Independent Test**: Create a task, then ask "What was that task I just added?" and verify chatbot references it

### Implementation for User Story 6

- [x] T040 [US6] Implement conversation history retrieval in backend/src/services/chat_service.py
- [x] T041 [US6] Build message context array for Groq API (history + new message) in backend/src/services/chat_service.py
- [x] T042 [US6] Implement GET /api/{user_id}/conversations endpoint in backend/src/api/chat.py
- [x] T043 [US6] Implement GET /api/{user_id}/conversations/{id} endpoint in backend/src/api/chat.py
- [x] T044 [US6] Display conversation history in frontend ChatInterface component

**Checkpoint**: User Stories 1-6 complete - full conversation support

---

## Phase 9: User Story 7 - Resume Conversations After Server Restart (Priority: P3)

**Goal**: Conversation history persists across server restarts

**Independent Test**: Create conversation, restart server, verify history still accessible

### Implementation for User Story 7

- [x] T045 [US7] Verify conversation persistence in database (already handled by Phase 2 models)
- [x] T046 [US7] Implement DELETE /api/{user_id}/conversations/{id} endpoint in backend/src/api/chat.py
- [x] T047 [US7] Add conversation list UI to frontend chat page

**Checkpoint**: All user stories complete

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, edge cases, and improvements

### Error Handling

- [x] T048 [P] Implement AI service unavailability handling in backend/src/services/chat_service.py
- [x] T049 [P] Implement unrecognized intent handling (polite response + command list) in backend/src/services/chat_service.py
- [x] T050 [P] Implement ambiguous task reference handling in backend/src/services/chat_service.py

### Frontend Polish

- [x] T051 [P] Add loading indicator to ChatInterface in frontend/src/components/ChatInterface/ChatInterface.tsx
- [x] T052 [P] Add error state display to ChatInterface in frontend/src/components/ChatInterface/ChatInterface.tsx
- [x] T053 Add navigation link to chat page in frontend layout

### Documentation

- [x] T054 [P] Update backend/README.md with chatbot endpoint documentation
- [x] T055 Run quickstart.md validation to verify setup instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-9)**: All depend on Foundational phase completion
- **Polish (Phase 10)**: Depends on user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2)
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - independent of US1
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - independent of US1/US2
- **User Story 4 (P2)**: Can start after Foundational (Phase 2)
- **User Story 5 (P2)**: Can start after Foundational (Phase 2)
- **User Story 6 (P2)**: Depends on conversation/message persistence (Phase 2)
- **User Story 7 (P3)**: Depends on User Story 6 for conversation management

### Parallel Opportunities

- All tasks marked [P] within the same phase can run in parallel
- User Stories 1, 2, 3 can be developed in parallel (all P1)
- User Stories 4, 5 can be developed in parallel (both P2)
- Frontend tasks (T025-T029) can run parallel with backend tasks for US1

---

## Parallel Example: User Story 1

```bash
# Launch all parallel tasks for User Story 1 together:
Task: "Create ChatInterface component in frontend/src/components/ChatInterface/ChatInterface.tsx"
Task: "Create ChatInterface types in frontend/src/components/ChatInterface/ChatInterface.types.ts"
Task: "Create MessageBubble component in frontend/src/components/MessageBubble/MessageBubble.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test creating tasks via chat
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy (MVP!)
3. Add User Stories 2, 3 → Test → Deploy (Core complete!)
4. Add User Stories 4, 5 → Test → Deploy (Full CRUD!)
5. Add User Stories 6, 7 → Test → Deploy (Full feature!)

### Recommended Sequence

For single developer:
1. Phase 1 → Phase 2 (Foundational)
2. Phase 3 (US1 - Create) → Frontend integration
3. Phase 4 (US2 - List) → Phase 5 (US3 - Complete)
4. Phase 6 (US4 - Delete) → Phase 7 (US5 - Update)
5. Phase 8 (US6 - Context) → Phase 9 (US7 - Persistence)
6. Phase 10 (Polish)

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Phase 1: Setup | 3 | Dependencies and environment |
| Phase 2: Foundational | 13 | Models, schemas, MCP foundation |
| Phase 3: US1 (P1) | 13 | Create tasks via chat + frontend |
| Phase 4: US2 (P1) | 3 | List tasks via chat |
| Phase 5: US3 (P1) | 3 | Complete tasks via chat |
| Phase 6: US4 (P2) | 2 | Delete tasks via chat |
| Phase 7: US5 (P2) | 2 | Update tasks via chat |
| Phase 8: US6 (P2) | 5 | Conversation context |
| Phase 9: US7 (P3) | 3 | Persistence & history UI |
| Phase 10: Polish | 8 | Error handling, polish |
| **Total** | **55** | |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Tests not explicitly requested - omitted per spec
