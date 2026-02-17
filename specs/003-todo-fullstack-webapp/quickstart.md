# Quickstart: Todo Application Full-Stack Web Application

## Prerequisites

- Node.js 18+ for Next.js frontend
- Python 3.11+ for FastAPI backend
- PostgreSQL (or access to Neon Serverless PostgreSQL)
- npm/yarn/pnpm package managers
- Git for version control
- Docker (optional, for containerized development)

## Setup Instructions

### 1. Clone and Initialize Repository
```bash
git clone <repository-url>
cd <repository-name>

# Initialize the project structure
mkdir -p backend/src/{models,schemas,api,services,database,middleware,utils,config}
mkdir -p frontend/src/{app,components,services,lib,styles}
mkdir -p backend/tests/{unit,integration}
mkdir -p frontend/tests
```

### 2. Backend Setup (FastAPI + SQLModel + Neon PostgreSQL)

#### Environment Configuration
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install "fastapi[all]" uvicorn sqlmodel python-jose[cryptography] passlib[bcrypt] python-multipart python-dotenv httpx

# Create environment file
touch .env
```

#### Backend Environment Variables (.env)
```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
NEON_DATABASE_URL=your_neon_connection_string_here

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-before-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Better Auth Configuration
BETTER_AUTH_SECRET=your-better-auth-secret
BETTER_AUTH_TRUST_HOST=true

# Application
ENVIRONMENT=development
DEBUG=True
```

### 3. Frontend Setup (Next.js + TypeScript + Tailwind CSS)

```bash
# Navigate to frontend directory
cd ../frontend

# Initialize Next.js project
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"

# Install additional dependencies
npm install @hookform/resolvers axios class-variance-authority clsx react-hook-form react-icons tailwind-merge zod
npm install -D @types/react-dom
```

#### Frontend Environment Variables (.env.local)
```env
# Backend API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# Better Auth Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

### 4. Database Setup with Neon PostgreSQL

#### Option A: Using Neon Console
1. Create a Neon account at https://neon.tech
2. Create a new project
3. Copy the connection string to your backend `.env` file

#### Option B: Local PostgreSQL Setup
```sql
-- Create database
CREATE DATABASE todo_app;

-- Create tables (this will be handled by SQLModel migrations)
-- See backend/database/database.py for initialization
```

## Running the Application

### Development Mode

#### Terminal 1: Start Backend
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn src.main:app --reload --port 8000
```

#### Terminal 2: Start Frontend
```bash
cd frontend
npm run dev
```

### Production Mode
```bash
# Build frontend
cd frontend
npm run build

# The backend can be served with the built frontend assets
cd ../backend
# Configure your production server to serve static files from frontend's 'out' directory
```

## API Endpoints

### Authentication (via Better Auth)
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login existing user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user info

### Task Management (Protected Routes - JWT Required)
- `GET /api/tasks` - Get all user's tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{task_id}` - Get specific task
- `PUT /api/tasks/{task_id}` - Update task
- `DELETE /api/tasks/{task_id}` - Delete task
- `PATCH /api/tasks/{task_id}/toggle-complete` - Toggle task completion status

## Environment Variables

### Backend (.env)
```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
TEST_DATABASE_URL=postgresql://user:password@localhost:5432/todo_test

# JWT Configuration
JWT_SECRET_KEY=super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
ENVIRONMENT=development
DEBUG=true
SERVER_NAME=localhost
SERVER_HOST=http://localhost:8000

# CORS Configuration
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

### Frontend (.env.local)
```env
# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/ws

# Better Auth Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

## Testing the Application

### Backend Tests
```bash
# Run all backend tests
cd backend
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_tasks.py
```

### Frontend Tests
```bash
# Run all frontend tests
cd frontend
npm run test

# Run tests in watch mode
npm run test:watch
```

## Docker Setup (Optional)

### docker-compose.yml
```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_DB: todo_app
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/todo_app
    volumes:
      - ./backend:/app

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      - NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

volumes:
  postgres_data:
```

## Troubleshooting

### Common Issues:

1. **Database Connection Issues**:
   - Verify PostgreSQL is running
   - Check DATABASE_URL in backend .env
   - Ensure database tables are created (run initialization script)

2. **Authentication Issues**:
   - Verify JWT secrets match between frontend and backend
   - Check that Better Auth is properly configured
   - Ensure CORS settings allow communication

3. **Frontend-Backend Communication**:
   - Verify NEXT_PUBLIC_API_BASE_URL points to running backend
   - Check that both services are running on expected ports
   - Confirm proxy settings if using development proxy

4. **Dependency Issues**:
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Clear Python cache: `find . -type d -name __pycache__ -delete`

### Resetting Data:
```bash
# Reset database (WARNING: This will delete all data)
cd backend
source venv/bin/activate
python -c "
from src.database.database import engine
from src.models.user import User
from src.models.task import Task
from sqlmodel import SQLModel
SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)
"
```

## Next Steps

1. Implement the defined API endpoints in `backend/src/api/tasks.py`
2. Create the data models in `backend/src/models/`
3. Implement the authentication middleware
4. Create the frontend components for task management
5. Implement the API service layer in `frontend/src/services/api.ts`
6. Add form validation and error handling
7. Implement loading states and user feedback mechanisms