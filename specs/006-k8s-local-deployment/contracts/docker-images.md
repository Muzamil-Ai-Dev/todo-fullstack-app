# Docker Image Contracts

**Feature**: 006-k8s-local-deployment
**Date**: 2026-02-18
**Purpose**: Define the interface contracts for Docker images

## Frontend Image Contract

### Image Metadata

```yaml
repository: todo-frontend
tag: latest
baseImage: node:20-alpine
exposedPorts:
  - 3000
user: nextjs (uid: 1001)
workdir: /app
```

### Build Contract

**Input Requirements**:
- Source code in `/frontend` directory
- `package.json` and `package-lock.json` present
- `.env.local` or environment variables for build-time configuration
- Next.js configuration in `next.config.js`

**Build Command**:
```bash
docker build -t todo-frontend:latest -f frontend/Dockerfile ./frontend
```

**Build Arguments** (optional):
```dockerfile
ARG NODE_ENV=production
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Expected Output**:
- Docker image tagged as `todo-frontend:latest`
- Image size: < 200MB (optimized with multi-stage build)
- Build time: < 5 minutes on standard hardware

### Runtime Contract

**Environment Variables** (required):
```bash
NODE_ENV=production
PORT=3000
```

**Environment Variables** (optional):
```bash
NEXT_PUBLIC_API_URL=http://todo-backend:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

**Exposed Ports**:
- `3000/tcp` - HTTP server

**Volume Mounts** (none required):
- Application is stateless
- All data fetched from backend API

**Health Check Endpoint**:
- Path: `/api/health`
- Method: GET
- Expected Response: `200 OK` with `{"status": "healthy"}`
- Response Time: < 100ms

**Startup Behavior**:
- Starts Next.js server on port 3000
- Ready to accept connections within 10-30 seconds
- Logs startup messages to stdout

**Resource Requirements**:
```yaml
requests:
  cpu: 250m
  memory: 256Mi
limits:
  cpu: 500m
  memory: 512Mi
```

### Run Contract

**Standalone Docker Run**:
```bash
docker run -d \
  --name todo-frontend \
  -p 3000:3000 \
  -e NODE_ENV=production \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
  todo-frontend:latest
```

**Expected Behavior**:
- Container starts successfully
- HTTP server listens on port 3000
- Health endpoint responds within 30 seconds
- Application serves static assets and API routes

**Kubernetes Deployment**:
```yaml
spec:
  containers:
  - name: frontend
    image: todo-frontend:latest
    imagePullPolicy: IfNotPresent
    ports:
    - containerPort: 3000
      protocol: TCP
    env:
    - name: NODE_ENV
      value: "production"
    - name: NEXT_PUBLIC_API_URL
      value: "http://todo-backend:8000"
    livenessProbe:
      httpGet:
        path: /api/health
        port: 3000
      initialDelaySeconds: 30
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /api/health
        port: 3000
      initialDelaySeconds: 10
      periodSeconds: 5
```

---

## Backend Image Contract

### Image Metadata

```yaml
repository: todo-backend
tag: latest
baseImage: python:3.13-slim
exposedPorts:
  - 8000
user: appuser (uid: 1001)
workdir: /app
```

### Build Contract

**Input Requirements**:
- Source code in `/backend` directory
- `pyproject.toml` and `uv.lock` present
- Python source in `/backend/src` and `/backend/main.py`

**Build Command**:
```bash
docker build -t todo-backend:latest -f backend/Dockerfile ./backend
```

**Build Arguments** (optional):
```dockerfile
ARG PYTHON_VERSION=3.13
```

**Expected Output**:
- Docker image tagged as `todo-backend:latest`
- Image size: < 300MB (optimized with multi-stage build)
- Build time: < 5 minutes on standard hardware

### Runtime Contract

**Environment Variables** (required):
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
GROQ_API_KEY=gsk_xxx
BETTER_AUTH_SECRET=secret_xxx
```

**Environment Variables** (optional):
```bash
LOG_LEVEL=info
CORS_ORIGINS=http://localhost:3000,http://todo-frontend:3000
```

**Exposed Ports**:
- `8000/tcp` - HTTP API server

**Volume Mounts** (none required):
- Application is stateless
- All data stored in external PostgreSQL database

**Health Check Endpoint**:
- Path: `/health`
- Method: GET
- Expected Response: `200 OK` with `{"status": "healthy"}`
- Response Time: < 50ms

**Startup Behavior**:
- Starts Uvicorn server on port 8000
- Connects to PostgreSQL database
- Ready to accept connections within 10-20 seconds
- Logs startup messages to stdout

**Resource Requirements**:
```yaml
requests:
  cpu: 250m
  memory: 256Mi
limits:
  cpu: 500m
  memory: 512Mi
```

### Run Contract

**Standalone Docker Run**:
```bash
docker run -d \
  --name todo-backend \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e GROQ_API_KEY="gsk_xxx" \
  -e BETTER_AUTH_SECRET="secret_xxx" \
  todo-backend:latest
```

**Expected Behavior**:
- Container starts successfully
- HTTP server listens on port 8000
- Database connection established
- Health endpoint responds within 20 seconds
- API endpoints accessible

**Kubernetes Deployment**:
```yaml
spec:
  containers:
  - name: backend
    image: todo-backend:latest
    imagePullPolicy: IfNotPresent
    ports:
    - containerPort: 8000
      protocol: TCP
    env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: todo-secrets
          key: DATABASE_URL
    - name: GROQ_API_KEY
      valueFrom:
        secretKeyRef:
          name: todo-secrets
          key: GROQ_API_KEY
    - name: BETTER_AUTH_SECRET
      valueFrom:
        secretKeyRef:
          name: todo-secrets
          key: BETTER_AUTH_SECRET
    livenessProbe:
      httpGet:
        path: /health
        port: 8000
      initialDelaySeconds: 20
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /health
        port: 8000
      initialDelaySeconds: 10
      periodSeconds: 5
```

---

## Image Loading Contract (Minikube)

### Loading Images into Minikube

**Command**:
```bash
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

**Expected Behavior**:
- Images transferred to Minikube's Docker daemon
- Images available for Kubernetes to pull
- No registry authentication required

**Verification**:
```bash
minikube image ls | grep todo
```

**Expected Output**:
```
docker.io/library/todo-frontend:latest
docker.io/library/todo-backend:latest
```

---

## Image Pull Policy Contract

### Kubernetes ImagePullPolicy

**Policy**: `IfNotPresent`

**Rationale**:
- Images loaded directly into Minikube
- No external registry configured
- Avoids unnecessary pull attempts

**Behavior**:
- Kubernetes checks local image cache first
- Only pulls if image not present locally
- Fails if image not found (expected for local development)

**Alternative for Production** (Phase V):
- Policy: `Always`
- Images pushed to container registry
- Kubernetes always pulls latest version

---

## Security Contract

### Non-Root User

**Frontend**:
- User: `nextjs`
- UID: 1001
- GID: 1001

**Backend**:
- User: `appuser`
- UID: 1001
- GID: 1001

**Rationale**:
- Follows security best practices
- Prevents privilege escalation
- Required for production deployments

### Minimal Base Images

**Frontend**: `node:20-alpine`
- Minimal attack surface
- Smaller image size
- Faster pulls and starts

**Backend**: `python:3.13-slim`
- Minimal attack surface
- Includes only essential system libraries
- Smaller than full Python image

### No Secrets in Images

**Contract**:
- No hardcoded credentials in Dockerfiles
- No secrets in environment variables at build time
- All secrets provided at runtime via Kubernetes Secrets

---

## Validation Contract

### Image Build Validation

**Success Criteria**:
- `docker build` exits with code 0
- Image tagged successfully
- Image size within expected range
- No security vulnerabilities in base image (scan with `docker scan`)

### Image Run Validation

**Success Criteria**:
- Container starts without errors
- Health endpoint responds within timeout
- Application logs show successful startup
- No crash loops or restart behavior

### Kubernetes Deployment Validation

**Success Criteria**:
- Pods reach Running state
- Readiness probes pass
- Services route traffic to pods
- Application accessible via port-forward

---

## Summary

These contracts define the interface and behavior expectations for Docker images in the deployment pipeline. Key aspects:

1. **Build Contract**: Inputs, commands, and expected outputs
2. **Runtime Contract**: Environment variables, ports, health checks, resources
3. **Run Contract**: Standalone and Kubernetes deployment specifications
4. **Security Contract**: Non-root users, minimal images, secret management
5. **Validation Contract**: Success criteria for build, run, and deployment

All contracts ensure consistency between local development, Minikube testing, and future production deployment.
