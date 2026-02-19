# Tasks: Local Kubernetes Deployment

**Input**: Design documents from `/specs/006-k8s-local-deployment/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `frontend/`, `helm/`, `docs/`
- Based on existing monorepo structure from Phase II/III

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and documentation structure

- [x] T001 Create helm/ directory structure at repository root
- [x] T002 Create docs/kubernetes/ directory for deployment documentation
- [ ] T003 [P] Verify Docker Desktop is installed and running (tools not available in current environment)
- [ ] T004 [P] Verify Minikube is installed (version 1.30+) (tools not available in current environment)
- [ ] T005 [P] Verify kubectl is installed (version 1.27+) (tools not available in current environment)
- [ ] T006 [P] Verify Helm is installed (version 3.12+) (tools not available in current environment)

**Checkpoint**: Development environment ready for containerization

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Create frontend health endpoint at frontend/src/app/api/health/route.ts
- [x] T008 Verify backend health endpoint exists at backend/src/api/ (already implemented in Phase III)
- [x] T009 Document environment variables required for deployment in docs/kubernetes/environment-variables.md

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Containerize Applications (Priority: P1) 🎯 MVP

**Goal**: Build Docker images for frontend and backend that run consistently across environments

**Independent Test**: Build Docker images, run containers locally with `docker run`, verify applications work correctly

### Implementation for User Story 1

- [x] T010 [P] [US1] Create frontend Dockerfile at frontend/Dockerfile with multi-stage build
- [x] T011 [P] [US1] Create backend Dockerfile at backend/Dockerfile with multi-stage build
- [x] T012 [P] [US1] Create .dockerignore for frontend at frontend/.dockerignore
- [x] T013 [P] [US1] Create .dockerignore for backend at backend/.dockerignore
- [ ] T014 [US1] Build frontend Docker image and verify build succeeds (requires Docker)
- [ ] T015 [US1] Build backend Docker image and verify build succeeds (requires Docker)
- [ ] T016 [US1] Test frontend container standalone with docker run (requires Docker)
- [ ] T017 [US1] Test backend container standalone with docker run (requires Docker)
- [ ] T018 [US1] Verify frontend container serves health endpoint (requires Docker)
- [ ] T019 [US1] Verify backend container serves health endpoint and API (requires Docker)
- [x] T020 [US1] Document Docker build commands in docs/kubernetes/docker-build.md

**Checkpoint**: Docker images build successfully and run standalone - containerization complete

---

## Phase 4: User Story 2 - Create Helm Charts (Priority: P2)

**Goal**: Package Kubernetes resources declaratively for repeatable deployments

**Independent Test**: Run `helm template` to validate syntax, verify chart renders valid manifests

### Implementation for User Story 2

- [x] T021 [US2] Create parent Helm chart structure at helm/todo-app/
- [x] T022 [P] [US2] Create Chart.yaml for parent chart at helm/todo-app/Chart.yaml
- [x] T023 [P] [US2] Create values.yaml for parent chart at helm/todo-app/values.yaml
- [x] T024 [P] [US2] Create values-dev.yaml for development at helm/todo-app/values-dev.yaml
- [x] T025 [P] [US2] Create _helpers.tpl template at helm/todo-app/templates/_helpers.tpl
- [x] T026 [P] [US2] Create ConfigMap template at helm/todo-app/templates/configmap.yaml
- [x] T027 [P] [US2] Create Secret template at helm/todo-app/templates/secret.yaml
- [x] T028 [US2] Create frontend subchart structure at helm/todo-app/charts/frontend/
- [x] T029 [P] [US2] Create frontend Chart.yaml at helm/todo-app/charts/frontend/Chart.yaml
- [x] T030 [P] [US2] Create frontend values.yaml at helm/todo-app/charts/frontend/values.yaml
- [x] T031 [P] [US2] Create frontend _helpers.tpl at helm/todo-app/charts/frontend/templates/_helpers.tpl
- [x] T032 [P] [US2] Create frontend Deployment template at helm/todo-app/charts/frontend/templates/deployment.yaml
- [x] T033 [P] [US2] Create frontend Service template at helm/todo-app/charts/frontend/templates/service.yaml
- [x] T034 [US2] Create backend subchart structure at helm/todo-app/charts/backend/
- [x] T035 [P] [US2] Create backend Chart.yaml at helm/todo-app/charts/backend/Chart.yaml
- [x] T036 [P] [US2] Create backend values.yaml at helm/todo-app/charts/backend/values.yaml
- [x] T037 [P] [US2] Create backend _helpers.tpl at helm/todo-app/charts/backend/templates/_helpers.tpl
- [x] T038 [P] [US2] Create backend Deployment template at helm/todo-app/charts/backend/templates/deployment.yaml
- [x] T039 [P] [US2] Create backend Service template at helm/todo-app/charts/backend/templates/service.yaml
- [ ] T040 [US2] Validate Helm chart with helm lint (requires Helm)
- [ ] T041 [US2] Test Helm template rendering with helm template (requires Helm)
- [ ] T042 [US2] Verify all Kubernetes manifests are valid YAML (requires Helm)

**Checkpoint**: Helm charts created and validated - ready for deployment

---

## Phase 5: User Story 3 - Deploy to Minikube (Priority: P1)

**Goal**: Deploy containerized application to local Minikube cluster for testing

**Independent Test**: Start Minikube, deploy with Helm, verify all pods Running and application accessible

### Implementation for User Story 3

- [ ] T043 [US3] Start Minikube cluster with appropriate resources (4GB RAM, 2 CPUs)
- [ ] T044 [US3] Load frontend Docker image into Minikube
- [ ] T045 [US3] Load backend Docker image into Minikube
- [ ] T046 [US3] Verify images are loaded in Minikube
- [ ] T047 [US3] Create Kubernetes secrets for database and API keys
- [ ] T048 [US3] Install Helm chart to Minikube cluster
- [ ] T049 [US3] Verify all pods reach Running state
- [ ] T050 [US3] Verify frontend deployment is healthy
- [ ] T051 [US3] Verify backend deployment is healthy
- [ ] T052 [US3] Check pod logs for errors
- [ ] T053 [US3] Setup port-forwarding for frontend service
- [ ] T054 [US3] Setup port-forwarding for backend service
- [ ] T055 [US3] Test frontend accessibility via localhost:3000
- [ ] T056 [US3] Test backend API accessibility via localhost:8000
- [ ] T057 [US3] Verify backend can connect to external Neon database
- [ ] T058 [US3] Test complete user flow (login, create task, AI chatbot)
- [ ] T059 [US3] Verify 100% feature parity with Phase III
- [ ] T060 [US3] Test pod restart resilience (delete pod, verify recreation)
- [ ] T061 [US3] Test scaling deployment (scale to 2 replicas)
- [ ] T062 [US3] Document deployment commands in docs/kubernetes/deployment-commands.md

**Checkpoint**: Application deployed to Minikube and fully functional

---

## Phase 6: User Story 4 - Use AIOps Tools for Deployment (Priority: P3)

**Goal**: Document and demonstrate AI-powered operations tools for Kubernetes

**Independent Test**: Use kubectl-ai or Docker AI to perform operations and verify helpful output

### Implementation for User Story 4

- [ ] T063 [P] [US4] Document kubectl-ai installation in docs/kubernetes/aiops-setup.md
- [ ] T064 [P] [US4] Document Docker AI (Gordon) usage in docs/kubernetes/aiops-setup.md
- [ ] T065 [P] [US4] Document kagent installation (optional) in docs/kubernetes/aiops-setup.md
- [ ] T066 [P] [US4] Create kubectl-ai examples in docs/kubernetes/kubectl-ai-examples.md
- [ ] T067 [P] [US4] Create Docker AI examples in docs/kubernetes/docker-ai-examples.md
- [ ] T068 [P] [US4] Add AIOps section to quickstart guide
- [ ] T069 [US4] Test kubectl-ai with sample deployment commands
- [ ] T070 [US4] Test Docker AI with Dockerfile optimization suggestions

**Checkpoint**: AIOps tools documented and examples provided

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, troubleshooting, and final validation

- [ ] T071 [P] Create comprehensive troubleshooting guide at docs/kubernetes/troubleshooting.md
- [ ] T072 [P] Create Minikube setup guide at docs/kubernetes/minikube-setup.md
- [ ] T073 [P] Document common operations (scale, update, rollback) in docs/kubernetes/common-operations.md
- [ ] T074 [P] Add quick reference commands to docs/kubernetes/quick-reference.md
- [ ] T075 Update main README.md with Phase IV deployment instructions
- [ ] T076 Validate quickstart.md by following all steps
- [ ] T077 Test complete deployment from scratch (clean Minikube)
- [ ] T078 Verify all success criteria from spec.md are met
- [ ] T079 Document known issues and limitations
- [ ] T080 Create deployment checklist for Phase V preparation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 (Containerize) must complete before US2 (Helm Charts)
  - US2 (Helm Charts) must complete before US3 (Deploy to Minikube)
  - US4 (AIOps Tools) can proceed in parallel with US3 or after
- **Polish (Phase 7)**: Depends on US1, US2, US3 being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies
- **User Story 2 (P2)**: Depends on User Story 1 (needs Docker images)
- **User Story 3 (P1)**: Depends on User Stories 1 and 2 (needs images and charts)
- **User Story 4 (P3)**: Can start after Foundational, best after US3 for testing

### Parallel Opportunities

- **Phase 1**: Tasks T003-T006 can run in parallel (verification tasks)
- **Phase 2**: Tasks T007-T009 can run in parallel (different files)
- **Phase 3 (US1)**:
  - T010-T013 can run in parallel (creating Dockerfiles and .dockerignore)
  - T014-T015 can run in parallel (building images)
  - T016-T019 can run in parallel (testing containers)
- **Phase 4 (US2)**:
  - T022-T027 can run in parallel (parent chart files)
  - T029-T033 can run in parallel (frontend subchart files)
  - T035-T039 can run in parallel (backend subchart files)
- **Phase 6 (US4)**: Tasks T063-T067 can run in parallel (documentation)
- **Phase 7**: Tasks T071-T074 can run in parallel (documentation)

---

## Parallel Example: User Story 1 (Containerization)

```bash
# Launch all Dockerfile creation tasks together:
Task: "Create frontend Dockerfile at frontend/Dockerfile"
Task: "Create backend Dockerfile at backend/Dockerfile"
Task: "Create .dockerignore for frontend"
Task: "Create .dockerignore for backend"

# After Dockerfiles exist, build images in parallel:
Task: "Build frontend Docker image"
Task: "Build backend Docker image"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (verify tools installed)
2. Complete Phase 2: Foundational (health endpoints, env vars)
3. Complete Phase 3: User Story 1 (Containerization)
4. **STOP and VALIDATE**: Test Docker images run standalone
5. Proceed to Helm charts if containerization successful

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test Docker images standalone → Validate (Containers work!)
3. Add User Story 2 → Test Helm charts render → Validate (Charts ready!)
4. Add User Story 3 → Deploy to Minikube → Validate (Full deployment!)
5. Add User Story 4 → Document AIOps tools → Validate (Complete!)
6. Polish → Final validation → Deploy/Demo

### Recommended Sequence

For single developer:
1. Phase 1 (Setup) → Phase 2 (Foundational)
2. Phase 3 (US1 - Containerize) → Validate images
3. Phase 4 (US2 - Helm Charts) → Validate charts
4. Phase 5 (US3 - Deploy) → Validate deployment
5. Phase 6 (US4 - AIOps) → Document tools
6. Phase 7 (Polish) → Final validation

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Phase 1: Setup | 6 | Tool verification and directory structure |
| Phase 2: Foundational | 3 | Health endpoints and environment variables |
| Phase 3: US1 (P1) | 11 | Docker containerization |
| Phase 4: US2 (P2) | 22 | Helm chart creation |
| Phase 5: US3 (P1) | 20 | Minikube deployment |
| Phase 6: US4 (P3) | 8 | AIOps tools documentation |
| Phase 7: Polish | 10 | Documentation and validation |
| **Total** | **80** | |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- US1 must complete before US2, US2 before US3 (sequential dependency)
- US4 can proceed in parallel with US3 or after
