# TodoPro - Full-Stack Todo Application

A modern full-stack todo application built with Next.js, FastAPI, SQLModel, and Neon PostgreSQL.

## Overview

This is a full-stack web application that allows users to manage tasks with user authentication, persistent storage, and a responsive UI. Part of the **Hackathon II - Phase 2** project.

## Live Demo

- **Frontend**: https://muzamil-ai-dev.github.io/todo-fullstack-app/
- **Backend API**: https://muzamil-ai-dev-todo-backend.hf.space

## Features

- User authentication (Register, Login, Logout)
- Create, Read, Update, Delete (CRUD) tasks
- Mark tasks as complete/incomplete
- Responsive design with Tailwind CSS
- JWT-based authentication
- Persistent PostgreSQL database storage

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16+ (App Router), React 19, TypeScript, Tailwind CSS |
| Backend | Python FastAPI |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Authentication | JWT Tokens |
| Deployment | GitHub Pages (Frontend), Hugging Face Spaces (Backend) |

## Project Structure

```
├── frontend/                # Next.js application
│   ├── src/
│   │   ├── app/            # App router pages
│   │   ├── components/     # React components
│   │   ├── context/        # Auth context
│   │   ├── services/       # API services
│   │   └── styles/         # Global styles
│   └── package.json
├── backend/                 # FastAPI application
│   ├── src/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # SQLModel models
│   │   ├── services/       # Business logic
│   │   ├── database/       # Database config
│   │   └── config/         # Settings
│   ├── main.py
│   └── requirements.txt
├── specs/                   # Feature specifications
└── .github/workflows/       # CI/CD pipelines
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login user |
| POST | `/api/auth/logout` | Logout user |
| GET | `/api/auth/me` | Get current user |
| GET | `/api/tasks` | Get all tasks |
| POST | `/api/tasks` | Create task |
| PUT | `/api/tasks/{id}` | Update task |
| DELETE | `/api/tasks/{id}` | Delete task |
| PATCH | `/api/tasks/{id}/toggle-complete` | Toggle completion |

## Local Development

### Prerequisites

- Node.js 20+
- Python 3.11+
- PostgreSQL database (or Neon account)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with your database URL
cp .env.example .env

# Run the server
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install

# Create .env.local with backend URL
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" > .env.local

# Run the development server
npm run dev
```

## Deployment

This project uses GitHub Actions for automated deployment:

- **Frontend**: Automatically deployed to GitHub Pages on push to master
- **Backend**: Automatically deployed to Hugging Face Spaces on push to master

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `HF_TOKEN` | Hugging Face write token |
| `BACKEND_API_URL` | Backend API URL for frontend |

### Required HF Space Secrets

| Secret | Description |
|--------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `JWT_SECRET_KEY` | Secret key for JWT tokens |
| `BETTER_AUTH_SECRET` | Secret for auth |

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## License

MIT License

---

Built as part of **Hackathon II - Phase 2** using Spec-Driven Development with Claude Code and Spec-Kit Plus.
