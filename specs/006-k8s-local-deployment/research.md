# Research: Local Kubernetes Deployment

**Feature**: 006-k8s-local-deployment
**Date**: 2026-02-18
**Purpose**: Document technical decisions and best practices for containerizing and deploying the Todo application to Minikube

## 1. Docker Multi-stage Builds

### Decision: Use multi-stage builds for both frontend and backend

**Rationale**:
- Reduces final image size by excluding build tools and dependencies
- Separates build-time and runtime dependencies
- Improves security by minimizing attack surface
- Faster deployment and startup times

**Alternatives Considered**:
- Single-stage builds: Rejected due to larger image sizes and included build tools in production
- Separate build and runtime Dockerfiles: Rejected due to maintenance overhead

**Implementation Notes**:

**Frontend (Next.js)**:
```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

**Backend (FastAPI)**:
```dockerfile
# Stage 1: Build
FROM python:3.13-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Stage 2: Production
FROM python:3.13-slim
WORKDIR /app
RUN addgroup --system --gid 1001 appuser && \
    adduser --system --uid 1001 --gid 1001 appuser
COPY --from=builder /app/.venv /app/.venv
COPY ./src ./src
COPY ./main.py ./
USER appuser
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Security Best Practices**:
- Use non-root users (nextjs:1001, appuser:1001)
- Use minimal base images (alpine, slim)
- Copy only necessary files
- Set NODE_ENV=production for Next.js

---

## 2. Helm Chart Structure

### Decision: Use a single parent chart with subcharts for frontend and backend

**Rationale**:
- Logical separation of concerns (frontend vs backend)
- Independent versioning and configuration
- Easier to manage service-specific values
- Follows Helm best practices for multi-service apps

**Alternatives Considered**:
- Flat chart with all resources: Rejected due to poor organization and harder maintenance
- Separate charts deployed independently: Rejected due to complexity in managing dependencies

**Implementation Notes**:

**Chart Structure**:
```
helm/
└── todo-app/
    ├── Chart.yaml
    ├── values.yaml
    ├── templates/
    │   ├── _helpers.tpl
    │   ├── configmap.yaml
    │   └── secret.yaml
    └── charts/
        ├── frontend/
        │   ├── Chart.yaml
        │   ├── values.yaml
        │   └── templates/
        │       ├── deployment.yaml
        │       ├── service.yaml
        │       └── ingress.yaml
        └── backend/
            ├── Chart.yaml
            ├── values.yaml
            └── templates/
                ├── deployment.yaml
                ├── service.yaml
                └── configmap.yaml
```

**Values File Structure**:
```yaml
# values.yaml (parent)
global:
  environment: development
  imagePullPolicy: IfNotPresent

database:
  host: "ep-xxx.neon.tech"
  name: "todo_db"
  sslmode: "require"

secrets:
  databaseUrl: ""  # Set via --set or values override
  groqApiKey: ""
  betterAuthSecret: ""

frontend:
  replicaCount: 1
  image:
    repository: todo-frontend
    tag: latest
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 250m
      memory: 256Mi

backend:
  replicaCount: 1
  image:
    repository: todo-backend
    tag: latest
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 250m
      memory: 256Mi
```

**Common Templates** (_helpers.tpl):
- Chart name helpers
- Label selectors
- Image pull policy
- Resource naming conventions

---

## 3. Minikube Configuration

### Decision: Use Minikube with 4GB RAM, 2 CPUs, and port-forwarding for local access

**Rationale**:
- 4GB RAM sufficient for frontend + backend + system overhead
- Port-forwarding simpler than ingress for local development
- Direct image loading faster than registry for local iteration

**Alternatives Considered**:
- Ingress controller: Rejected for Phase IV due to added complexity; suitable for Phase V
- Docker registry: Rejected due to slower iteration cycle for local development
- Larger resource allocation: Rejected to keep requirements accessible for most development machines

**Implementation Notes**:

**Minikube Start Command**:
```bash
minikube start --cpus=2 --memory=4096 --driver=docker
```

**Image Loading Strategy**:
```bash
# Build images
docker build -t todo-frontend:latest ./frontend
docker build -t todo-backend:latest ./backend

# Load into Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

**Access Pattern**:
```bash
# Port-forward frontend
kubectl port-forward svc/todo-frontend 3000:3000

# Port-forward backend
kubectl port-forward svc/todo-backend 8000:8000
```

**Minikube Addons**:
```bash
minikube addons enable metrics-server  # For resource monitoring
minikube addons enable dashboard       # For visual cluster inspection
```

---

## 4. External Database Connectivity

### Decision: Use direct connection with Kubernetes Secrets for credentials

**Rationale**:
- Neon PostgreSQL is externally hosted and accessible via public endpoint
- Secrets provide secure credential storage
- Direct connection simpler than ExternalName service for this use case
- Connection pooling handled by SQLAlchemy in backend code

**Alternatives Considered**:
- ExternalName service: Rejected as unnecessary abstraction for single external database
- ConfigMap for credentials: Rejected due to security concerns (credentials in plain text)

**Implementation Notes**:

**Secret Creation**:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-secrets
type: Opaque
stringData:
  DATABASE_URL: "postgresql://user:password@ep-xxx.neon.tech:5432/todo_db?sslmode=require"
  GROQ_API_KEY: "gsk_xxx"
  BETTER_AUTH_SECRET: "xxx"
```

**Deployment Environment Variables**:
```yaml
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
```

**Connection Pooling** (already implemented in Phase III):
- SQLAlchemy engine with pool_pre_ping=True
- pool_recycle=300 (5 minutes)
- pool_size=5, max_overflow=10

**Network Considerations**:
- Ensure Minikube can reach external internet
- Neon requires SSL connection (sslmode=require)
- No additional network policies needed for external connectivity

---

## 5. Health Checks

### Decision: Implement HTTP-based liveness and readiness probes for both services

**Rationale**:
- HTTP probes are standard for web applications
- Separate liveness (restart if unhealthy) and readiness (remove from service if not ready)
- Appropriate delays prevent premature restarts during startup

**Alternatives Considered**:
- TCP probes: Rejected as less informative than HTTP (can't check application health)
- Exec probes: Rejected due to overhead and complexity

**Implementation Notes**:

**Frontend (Next.js) Health Endpoint**:
```javascript
// pages/api/health.ts
export default function handler(req, res) {
  res.status(200).json({ status: 'healthy' });
}
```

**Backend (FastAPI) Health Endpoint** (already exists):
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**Deployment Probe Configuration**:

**Frontend**:
```yaml
livenessProbe:
  httpGet:
    path: /api/health
    port: 3000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /api/health
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

**Backend**:
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 20
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

**Timing Rationale**:
- initialDelaySeconds: Allow time for application startup (Next.js takes longer)
- periodSeconds: Balance between responsiveness and overhead
- failureThreshold: 3 failures before action (prevents flapping)

---

## 6. AIOps Tools Integration

### Decision: Document kubectl-ai and Docker AI usage; kagent optional for advanced scenarios

**Rationale**:
- kubectl-ai simplifies common Kubernetes operations with natural language
- Docker AI (Gordon) helps optimize Dockerfiles
- kagent provides advanced cluster analysis but adds complexity
- Tools enhance productivity but aren't required for core functionality

**Alternatives Considered**:
- Manual kubectl commands only: Rejected as missing opportunity to demonstrate AIOps
- Mandatory kagent usage: Rejected due to installation complexity and learning curve

**Implementation Notes**:

**kubectl-ai Installation**:
```bash
# Install kubectl-ai
brew install kubectl-ai  # macOS
# or download from https://github.com/GoogleCloudPlatform/kubectl-ai

# Configure with API key
kubectl ai config set-api-key <your-key>
```

**Common kubectl-ai Commands**:
```bash
# Deploy application
kubectl ai "deploy the todo app with 2 replicas"

# Scale deployment
kubectl ai "scale the backend to 3 replicas"

# Troubleshoot
kubectl ai "check why the frontend pods are failing"
kubectl ai "show me logs from the backend pod"

# Resource management
kubectl ai "show resource usage for all pods"
```

**Docker AI (Gordon) Usage**:
```bash
# Get Dockerfile recommendations
docker ai "optimize my Dockerfile for production"

# Build assistance
docker ai "help me build a multi-stage Dockerfile for Next.js"

# Troubleshooting
docker ai "why is my image so large?"
```

**kagent (Optional)**:
```bash
# Install kagent
pip install kagent

# Cluster analysis
kagent "analyze cluster health"
kagent "optimize resource allocation"
kagent "identify potential issues"
```

**Documentation Strategy**:
- Include kubectl-ai examples in quickstart.md
- Provide Docker AI tips in Dockerfile comments
- Mark kagent as optional enhancement
- Focus on practical, time-saving commands

---

## Summary of Key Decisions

| Area | Decision | Primary Benefit |
|------|----------|-----------------|
| Docker | Multi-stage builds with non-root users | Security + smaller images |
| Helm | Parent chart with frontend/backend subcharts | Organization + maintainability |
| Minikube | 4GB RAM, port-forwarding, direct image load | Simplicity + fast iteration |
| Database | Direct connection with K8s Secrets | Security + simplicity |
| Health Checks | HTTP probes with appropriate delays | Reliability + proper startup handling |
| AIOps | kubectl-ai + Docker AI (kagent optional) | Productivity + hackathon requirements |

All decisions prioritize simplicity, security, and alignment with hackathon Phase IV requirements while maintaining production-ready patterns.
