# Docker Build Commands

**Feature**: 006-k8s-local-deployment
**Purpose**: Commands for building Docker images for the Todo application

## Prerequisites

- Docker Desktop installed and running
- Navigate to project root directory

## Build Frontend Image

```bash
# Navigate to project root
cd /path/to/Todo_Application_P002

# Build frontend image
docker build -t todo-frontend:latest -f frontend/Dockerfile ./frontend

# Verify image was created
docker images | grep todo-frontend
```

**Expected Output**:
```
todo-frontend    latest    <image-id>    <time>    <size>
```

**Build Time**: 3-5 minutes

## Build Backend Image

```bash
# Navigate to project root
cd /path/to/Todo_Application_P002

# Build backend image
docker build -t todo-backend:latest -f backend/Dockerfile ./backend

# Verify image was created
docker images | grep todo-backend
```

**Expected Output**:
```
todo-backend     latest    <image-id>    <time>    <size>
```

**Build Time**: 2-4 minutes

## Build Both Images in Parallel

```bash
# Build both images simultaneously
docker build -t todo-frontend:latest -f frontend/Dockerfile ./frontend &
docker build -t todo-backend:latest -f backend/Dockerfile ./backend &

# Wait for both builds to complete
wait

# Verify both images
docker images | grep todo
```

## Test Images Locally

### Test Frontend Container

```bash
# Run frontend container
docker run -d \
  --name todo-frontend-test \
  -p 3000:3000 \
  -e NODE_ENV=production \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
  todo-frontend:latest

# Check container is running
docker ps | grep todo-frontend

# Test health endpoint
curl http://localhost:3000/api/health

# View logs
docker logs todo-frontend-test

# Stop and remove container
docker stop todo-frontend-test
docker rm todo-frontend-test
```

### Test Backend Container

```bash
# Run backend container (requires environment variables)
docker run -d \
  --name todo-backend-test \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db?sslmode=require" \
  -e GROQ_API_KEY="gsk_xxx" \
  -e BETTER_AUTH_SECRET="secret_xxx" \
  todo-backend:latest

# Check container is running
docker ps | grep todo-backend

# Test health endpoint
curl http://localhost:8000/health

# Test API docs
curl http://localhost:8000/docs

# View logs
docker logs todo-backend-test

# Stop and remove container
docker stop todo-backend-test
docker rm todo-backend-test
```

## Rebuild Images (After Code Changes)

```bash
# Rebuild frontend (no cache)
docker build --no-cache -t todo-frontend:latest -f frontend/Dockerfile ./frontend

# Rebuild backend (no cache)
docker build --no-cache -t todo-backend:latest -f backend/Dockerfile ./backend
```

## Tag Images for Registry (Future Use)

```bash
# Tag for Docker Hub
docker tag todo-frontend:latest username/todo-frontend:v1.0.0
docker tag todo-backend:latest username/todo-backend:v1.0.0

# Tag for GitHub Container Registry
docker tag todo-frontend:latest ghcr.io/username/todo-frontend:v1.0.0
docker tag todo-backend:latest ghcr.io/username/todo-backend:v1.0.0
```

## Clean Up Images

```bash
# Remove specific images
docker rmi todo-frontend:latest
docker rmi todo-backend:latest

# Remove all unused images
docker image prune -a

# Remove dangling images
docker image prune
```

## Troubleshooting

### Build fails with "no space left on device"

**Solution**: Clean up Docker resources
```bash
docker system prune -a --volumes
```

### Build fails with dependency errors

**Frontend**: Check package.json and package-lock.json are in sync
```bash
cd frontend
npm install
```

**Backend**: Check pyproject.toml and uv.lock are in sync
```bash
cd backend
uv sync
```

### Image size too large

**Check image size**:
```bash
docker images todo-frontend:latest
docker images todo-backend:latest
```

**Optimize**:
- Ensure .dockerignore is properly configured
- Use multi-stage builds (already implemented)
- Remove unnecessary dependencies

### Container fails to start

**Check logs**:
```bash
docker logs <container-name>
```

**Common issues**:
- Missing environment variables
- Port already in use
- Invalid configuration

## Next Steps

After building and testing images locally:
1. Load images into Minikube: See `minikube-setup.md`
2. Deploy with Helm: See `deployment-commands.md`
3. Troubleshoot issues: See `troubleshooting.md`
