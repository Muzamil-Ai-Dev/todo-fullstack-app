# Data Model: Local Kubernetes Deployment

**Feature**: 006-k8s-local-deployment
**Date**: 2026-02-18
**Purpose**: Define the structure and relationships of deployment artifacts

## Overview

This feature focuses on deployment infrastructure rather than application data models. The data model describes the structure of deployment artifacts (Docker images, Helm charts, Kubernetes resources) rather than business entities.

## Deployment Artifacts

### Docker Image

**Purpose**: Containerized application package ready for deployment

**Attributes**:
- **repository**: String - Image repository name (e.g., "todo-frontend", "todo-backend")
- **tag**: String - Image version identifier (e.g., "latest", "v1.0.0", git commit SHA)
- **digest**: String - SHA256 hash of image content (immutable identifier)
- **size**: Integer - Image size in bytes
- **created**: Timestamp - When the image was built
- **layers**: Array - List of filesystem layers comprising the image

**Relationships**:
- Referenced by Kubernetes Deployment
- Stored in Minikube's local image cache
- Built from Dockerfile

**Validation Rules**:
- Repository name must follow Docker naming conventions (lowercase, alphanumeric, hyphens)
- Tag must be valid semantic version or descriptive label
- Image must exist in Minikube before deployment

**State Transitions**:
1. Built (docker build)
2. Loaded into Minikube (minikube image load)
3. Pulled by Kubernetes (when pod starts)
4. Running (container executing)

---

### Helm Chart

**Purpose**: Package of Kubernetes resource definitions

**Attributes**:
- **name**: String - Chart name (e.g., "todo-app", "frontend", "backend")
- **version**: String - Chart version (semantic versioning)
- **appVersion**: String - Application version this chart deploys
- **description**: String - Human-readable chart description
- **dependencies**: Array - List of subchart dependencies
- **values**: Object - Default configuration values

**Relationships**:
- Contains Kubernetes resource templates
- May have subchart dependencies (frontend, backend)
- Deployed to Kubernetes cluster via Helm

**Validation Rules**:
- Chart.yaml must be valid YAML with required fields
- Version must follow semantic versioning (MAJOR.MINOR.PATCH)
- Templates must render valid Kubernetes manifests
- Values must match schema defined in values.schema.json (if present)

**Structure**:
```
Chart/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default values
├── templates/          # Kubernetes resource templates
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── secret.yaml
└── charts/             # Subchart dependencies
```

---

### Kubernetes Deployment

**Purpose**: Declarative specification for running application pods

**Attributes**:
- **name**: String - Deployment name (e.g., "todo-frontend", "todo-backend")
- **namespace**: String - Kubernetes namespace (default: "default")
- **replicas**: Integer - Desired number of pod instances
- **selector**: Object - Label selector for pods
- **template**: Object - Pod template specification
  - **containers**: Array - Container specifications
    - **name**: String
    - **image**: String - Docker image reference
    - **ports**: Array - Exposed ports
    - **env**: Array - Environment variables
    - **resources**: Object - CPU/memory limits and requests
    - **livenessProbe**: Object - Health check for restart
    - **readinessProbe**: Object - Health check for traffic routing

**Relationships**:
- Creates and manages Pods
- Referenced by Service for load balancing
- Uses ConfigMap and Secret for configuration

**Validation Rules**:
- Replicas must be >= 0
- Image must exist and be pullable
- Resource requests must be <= limits
- Probes must have valid HTTP/TCP/Exec configuration
- Container ports must be unique within pod

**State Transitions**:
1. Created (kubectl apply / helm install)
2. Progressing (creating pods)
3. Available (desired replicas running)
4. Degraded (some pods failing)
5. Failed (unable to create pods)

---

### Kubernetes Service

**Purpose**: Network abstraction providing stable endpoint for pods

**Attributes**:
- **name**: String - Service name (e.g., "todo-frontend", "todo-backend")
- **namespace**: String - Kubernetes namespace
- **type**: String - Service type (ClusterIP, NodePort, LoadBalancer)
- **selector**: Object - Label selector to match pods
- **ports**: Array - Port mappings
  - **name**: String - Port name
  - **port**: Integer - Service port (exposed to cluster)
  - **targetPort**: Integer - Container port (pod port)
  - **protocol**: String - TCP or UDP

**Relationships**:
- Routes traffic to Pods matching selector
- Used by other services for internal communication
- Exposed externally via port-forwarding or Ingress

**Validation Rules**:
- Type must be valid Kubernetes service type
- Ports must be in valid range (1-65535)
- Selector must match at least one pod
- Port names must be unique within service

---

### Kubernetes ConfigMap

**Purpose**: Store non-sensitive configuration data

**Attributes**:
- **name**: String - ConfigMap name
- **namespace**: String - Kubernetes namespace
- **data**: Object - Key-value pairs of configuration
- **binaryData**: Object - Binary data (base64 encoded)

**Relationships**:
- Mounted into Pods as environment variables or files
- Referenced by Deployment

**Validation Rules**:
- Keys must be valid environment variable names or filenames
- Total size must be < 1MB
- Data must be UTF-8 encoded strings

**Example Data**:
```yaml
data:
  ENVIRONMENT: "development"
  LOG_LEVEL: "info"
  FRONTEND_URL: "http://localhost:3000"
  BACKEND_URL: "http://todo-backend:8000"
```

---

### Kubernetes Secret

**Purpose**: Store sensitive configuration data (credentials, API keys)

**Attributes**:
- **name**: String - Secret name
- **namespace**: String - Kubernetes namespace
- **type**: String - Secret type (Opaque, kubernetes.io/tls, etc.)
- **data**: Object - Key-value pairs (base64 encoded)
- **stringData**: Object - Key-value pairs (plain text, encoded on creation)

**Relationships**:
- Mounted into Pods as environment variables or files
- Referenced by Deployment
- Access controlled by RBAC

**Validation Rules**:
- Data must be base64 encoded
- Keys must be valid environment variable names
- Total size must be < 1MB
- Should not be committed to version control (use sealed secrets or external secret management)

**Example Data**:
```yaml
stringData:
  DATABASE_URL: "postgresql://user:pass@host:5432/db"
  GROQ_API_KEY: "gsk_xxx"
  BETTER_AUTH_SECRET: "secret_xxx"
```

---

### Kubernetes Pod

**Purpose**: Smallest deployable unit, runs one or more containers

**Attributes**:
- **name**: String - Pod name (generated by Deployment)
- **namespace**: String - Kubernetes namespace
- **status**: Object - Current pod state
  - **phase**: String - Pending, Running, Succeeded, Failed, Unknown
  - **conditions**: Array - Detailed status conditions
  - **containerStatuses**: Array - Status of each container
- **spec**: Object - Pod specification (from Deployment template)

**Relationships**:
- Created and managed by Deployment
- Receives traffic from Service
- Runs Docker containers

**Validation Rules**:
- Must have at least one container
- Container images must be pullable
- Resource requests must be satisfiable by node
- Volume mounts must reference existing volumes

**State Transitions**:
1. Pending (scheduled, pulling images)
2. Running (all containers started)
3. Succeeded (completed successfully)
4. Failed (container exited with error)
5. Unknown (communication lost with node)

---

## Deployment Workflow

```
Developer
    ↓
[1] Build Docker Images
    ↓
Docker Images (local)
    ↓
[2] Load into Minikube
    ↓
Minikube Image Cache
    ↓
[3] Create Helm Chart
    ↓
Helm Chart (templates + values)
    ↓
[4] Helm Install
    ↓
Kubernetes Resources Created:
    ├── Deployment → Pods → Containers (using Images)
    ├── Service → Routes traffic to Pods
    ├── ConfigMap → Mounted into Pods
    └── Secret → Mounted into Pods
    ↓
[5] Port-forward Service
    ↓
Application Accessible on localhost
```

## Configuration Hierarchy

```
Helm Chart values.yaml (defaults)
    ↓
Override with values-dev.yaml / values-prod.yaml
    ↓
Override with --set flags
    ↓
Rendered into Kubernetes manifests
    ↓
Applied to cluster
    ↓
ConfigMap / Secret values
    ↓
Environment variables in Pods
    ↓
Application configuration
```

## Resource Relationships

```
Helm Chart (todo-app)
├── Subchart: frontend
│   ├── Deployment (todo-frontend)
│   │   └── Pod (todo-frontend-xxx)
│   │       └── Container (nextjs)
│   │           ├── Image: todo-frontend:latest
│   │           ├── Env from: ConfigMap, Secret
│   │           └── Probes: /api/health
│   └── Service (todo-frontend)
│       └── Routes to: Pod (todo-frontend-xxx)
│
└── Subchart: backend
    ├── Deployment (todo-backend)
    │   └── Pod (todo-backend-xxx)
    │       └── Container (fastapi)
    │           ├── Image: todo-backend:latest
    │           ├── Env from: ConfigMap, Secret
    │           └── Probes: /health
    └── Service (todo-backend)
        └── Routes to: Pod (todo-backend-xxx)

Shared Resources:
├── ConfigMap (todo-config)
│   └── Used by: frontend, backend
└── Secret (todo-secrets)
    └── Used by: backend (DATABASE_URL, GROQ_API_KEY)
```

## Summary

This data model describes the deployment infrastructure artifacts rather than application business entities. The key entities are:

1. **Docker Images** - Containerized applications
2. **Helm Charts** - Deployment packages
3. **Kubernetes Resources** - Runtime infrastructure (Deployments, Services, ConfigMaps, Secrets, Pods)

All entities follow Kubernetes and Docker conventions, with proper validation, relationships, and state management.
