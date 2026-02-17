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

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login user |
| GET | `/api/tasks` | Get all tasks |
| POST | `/api/tasks` | Create task |
| PUT | `/api/tasks/{id}` | Update task |
| DELETE | `/api/tasks/{id}` | Delete task |
| PATCH | `/api/tasks/{id}/toggle-complete` | Toggle completion |

## Configuration

Set these secrets in Hugging Face Space settings:

- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET_KEY` - Secret key for JWT tokens
- `BETTER_AUTH_SECRET` - Secret for Better Auth

## Health Check

- `GET /health` - Returns server health status
