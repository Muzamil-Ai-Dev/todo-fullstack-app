---
description: "Task list for Todo Application CLI implementation"
---

# Tasks: Todo Application CLI

**Input**: Design documents from `/specs/001-todo-cli-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in src/, tests/
- [x] T002 Initialize Python project with basic requirements.txt/pyproject.toml
- [x] T003 [P] Configure pytest for testing in pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [x] T004 Create Task model in src/models/task.py with all required fields (id, title, description, completed, created_at, updated_at)
- [x] T005 Create in-memory task storage in src/services/task_service.py (list/dictionary implementation)
- [x] T006 Create validation utilities in src/lib/validators.py for title length and other validations
- [x] T007 Setup main CLI structure in src/cli/main.py with basic menu display
- [x] T008 Create datetime utility functions for ISO 8601 formatting
- [x] T009 Implement main menu display with exact format: "==== Todo Application ====", options 1-7, and "Choose an option (1-7):"
- [x] T010 Implement user input handling and menu navigation in src/cli/main.py
- [x] T011 Implement main application loop that displays menu continuously until user exits

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks to their todo list through a simple, guided interface

**Independent Test**: Can be fully tested by running the application, selecting option 1, entering a valid title, and verifying that a task is created with an auto-incremented ID and proper timestamps.

### Implementation for User Story 1

- [x] T012 [P] [US1] Create Task model with all required fields in src/models/task.py
- [x] T013 [P] [US1] Implement add_task method in src/services/task_service.py
- [x] T014 [US1] Implement input validation for task title (1-200 chars) in src/lib/validators.py
- [x] T015 [US1] Implement add task CLI flow in src/cli/main.py (option 1)
- [x] T016 [US1] Add datetime handling for created_at and updated_at timestamps
- [x] T017 [US1] Add auto-incrementing ID functionality
- [x] T018 [US1] Implement error handling for empty titles
- [x] T019 [US1] Add success confirmation message "Task added successfully with ID #X"

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Allow users to see all their tasks in a clear, organized format to understand their current workload

**Independent Test**: Can be fully tested by adding a task, selecting option 2, and verifying that the task is displayed in the correct format with all required fields.

### Implementation for User Story 2

- [x] T020 [P] [US2] Implement get_all_tasks method in src/services/task_service.py
- [x] T021 [P] [US2] Implement view tasks CLI flow in src/cli/main.py (option 2)
- [x] T022 [US2] Add proper task display formatting with [✓] for complete and [ ] for pending
- [x] T023 [US2] Implement ascending ID sorting for task display
- [x] T024 [US2] Add "No tasks found." message when task list is empty
- [x] T025 [US2] Implement proper timestamp display format (YYYY-MM-DD HH:MM)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task Details (Priority: P2)

**Goal**: Allow users to modify the details of an existing task, such as updating the title or description

**Independent Test**: Can be fully tested by creating a task, selecting option 3, entering the task ID, updating the title, and verifying the task is updated with a new timestamp.

### Implementation for User Story 3

- [x] T026 [P] [US3] Implement update_task method in src/services/task_service.py
- [x] T027 [US3] Implement update task CLI flow in src/cli/main.py (option 3)
- [x] T028 [US3] Add validation for existing task ID
- [x] T029 [US3] Implement blank input handling (fields remain unchanged if blank)
- [x] T030 [US3] Update updated_at timestamp when task is modified
- [x] T031 [US3] Add success confirmation message "Task #X updated successfully."

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P2)

**Goal**: Allow users to remove completed or unwanted tasks from their list

**Independent Test**: Can be fully tested by creating a task, selecting option 4, confirming deletion, and verifying the task is removed and subsequent tasks maintain proper ID sequence.

### Implementation for User Story 4

- [x] T032 [P] [US4] Implement delete_task method in src/services/task_service.py
- [x] T033 [US4] Implement delete task CLI flow in src/cli/main.py (option 4)
- [x] T034 [US4] Add confirmation prompt "Are you sure you want to delete task #X? (y/n):"
- [x] T035 [US4] Implement 'y'/'n' input validation
- [x] T036 [US4] Add success confirmation "Task #X deleted successfully."
- [x] T037 [US4] Add cancellation message "Delete operation cancelled."
- [x] T038 [US4] Implement error handling for non-existent task IDs

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Mark Tasks Complete/Incomplete (Priority: P2)

**Goal**: Allow users to track the status of their tasks by marking them as complete or incomplete

**Independent Test**: Can be fully tested by creating a task, selecting option 5 to mark complete, then option 6 to mark incomplete, and verifying the status changes correctly.

### Implementation for User Story 5

- [x] T039 [P] [US5] Implement mark_task_complete method in src/services/task_service.py
- [x] T040 [P] [US5] Implement mark_task_incomplete method in src/services/task_service.py
- [x] T041 [US5] Implement mark complete CLI flow in src/cli/main.py (option 5)
- [x] T042 [US5] Implement mark incomplete CLI flow in src/cli/main.py (option 6)
- [x] T043 [US5] Add validation for existing task ID
- [x] T044 [US5] Add "Task is already completed/pending." messages
- [x] T045 [US5] Add success confirmation messages "Task #X marked as completed/pending."
- [x] T046 [US5] Update updated_at timestamp when status changes

**Checkpoint**: At this point, User Stories 1-5 should all work independently

---

## Phase 8: User Story 6 - Exit Application (Priority: P1)

**Goal**: Allow users to cleanly exit the application when finished

**Independent Test**: Can be fully tested by running the application and selecting option 7, verifying it exits cleanly with the proper goodbye message.

### Implementation for User Story 6

- [x] T047 [US6] Implement exit application CLI flow in src/cli/main.py (option 7)
- [x] T048 [US6] Add goodbye message "Thank you for using Todo Application. Goodbye!"
- [x] T049 [US6] Implement clean application exit

**Checkpoint**: All user stories should now be independently functional

---

## Phase 9: Error Handling & Edge Cases

**Goal**: Implement comprehensive error handling and edge case management

- [x] T050 Implement menu option validation (1-7 only) with friendly error messages
- [x] T051 Implement validation for task ID existence in update/delete operations
- [x] T052 Implement validation for confirmation inputs ('y'/'n' or 'Y'/'N')
- [x] T053 Implement validation for task title length (>200 characters)
- [x] T054 Implement validation for numeric inputs where expected
- [x] T055 Add error recovery protocol to return to main menu after errors
- [x] T056 Ensure no crashes under any circumstances

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T057 [P] Documentation updates in README.md
- [x] T058 Code cleanup and refactoring
- [x] T059 [P] Unit tests for Task model in tests/unit/test_task.py
- [x] T060 [P] Unit tests for validation logic in tests/unit/test_validators.py
- [x] T061 Integration tests for CLI flows in tests/integration/test_cli_flow.py
- [ ] T062 Contract tests for task operations in tests/contract/test_task_contract.py
- [ ] T063 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 6 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Add User Story 6 → Test independently → Deploy/Demo
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
   - Developer F: User Story 6
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence