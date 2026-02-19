# Helm Chart Contract

**Feature**: 006-k8s-local-deployment
**Date**: 2026-02-18
**Purpose**: Define the interface contract for Helm charts

## Chart Structure Contract

### Parent Chart: todo-app

**Chart.yaml**:
```yaml
apiVersion: v2
name: todo-app
description: A Helm chart for Todo Application with AI Chatbot
type: application
version: 1.0.0
appVersion: "1.0.0"
dependencies:
  - name: frontend
    version: 1.0.0
    repository: "file://./charts/frontend"
  - name: backend
    version: 1.0.0
    repository: "file://./charts/backend"
```

**Directory Structure**:
```
helm/todo-app/
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
    │       └── _helpers.tpl
    └── backend/
        ├── Chart.yaml
        ├── values.yaml
        └── templates/
            ├── deployment.yaml
            ├── service.yaml
            └── _helpers.tpl
```

---

## Values Contract

### Parent Chart Values (values.yaml)

```yaml
# Global configuration shared across all subcharts
global:
  environment: development
  imagePullPolicy: IfNotPresent

# Database configuration
database:
  host: "ep-xxx.neon.tech"
  port: 5432
  name: "todo_db"
  sslmode: "require"

# Secrets (override via --set or separate values file)
secrets:
  databaseUrl: ""  # postgresql://user:pass@host:5432/db?sslmode=require
  groqApiKey: ""   # gsk_xxx
  betterAuthSecret: ""  # secret_xxx

# Frontend subchart configuration
frontend:
  enabled: true
  replicaCount: 1
  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 3000
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 250m
      memory: 256Mi
  env:
    nodeEnv: production
    apiUrl: "http://todo-backend:8000"

# Backend subchart configuration
backend:
  enabled: true
  replicaCount: 1
  image:
    repository: todo-backend
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 8000
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 250m
      memory: 256Mi
  env:
    logLevel: info
    corsOrigins: "http://localhost:3000,http://todo-frontend:3000"
```

### Values Override Contract

**Development** (values-dev.yaml):
```yaml
global:
  environment: development

frontend:
  replicaCount: 1
  resources:
    limits:
      cpu: 500m
      memory: 512Mi

backend:
  replicaCount: 1
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
```

**Production** (values-prod.yaml - for Phase V):
```yaml
global:
  environment: production
  imagePullPolicy: Always

frontend:
  replicaCount: 3
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
    requests:
      cpu: 500m
      memory: 512Mi

backend:
  replicaCount: 3
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
    requests:
      cpu: 500m
      memory: 512Mi
```

---

## Template Contract

### Shared ConfigMap Template

**templates/configmap.yaml**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "todo-app.fullname" . }}-config
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
data:
  ENVIRONMENT: {{ .Values.global.environment | quote }}
  DATABASE_HOST: {{ .Values.database.host | quote }}
  DATABASE_PORT: {{ .Values.database.port | quote }}
  DATABASE_NAME: {{ .Values.database.name | quote }}
  DATABASE_SSLMODE: {{ .Values.database.sslmode | quote }}
```

### Shared Secret Template

**templates/secret.yaml**:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "todo-app.fullname" . }}-secrets
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
type: Opaque
stringData:
  DATABASE_URL: {{ .Values.secrets.databaseUrl | quote }}
  GROQ_API_KEY: {{ .Values.secrets.groqApiKey | quote }}
  BETTER_AUTH_SECRET: {{ .Values.secrets.betterAuthSecret | quote }}
```

### Frontend Deployment Template

**charts/frontend/templates/deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "frontend.fullname" . }}
  labels:
    {{- include "frontend.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "frontend.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "frontend.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: frontend
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: 3000
          protocol: TCP
        env:
        - name: NODE_ENV
          value: {{ .Values.env.nodeEnv | quote }}
        - name: NEXT_PUBLIC_API_URL
          value: {{ .Values.env.apiUrl | quote }}
        livenessProbe:
          httpGet:
            path: /api/health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /api/health
            port: http
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
```

### Backend Deployment Template

**charts/backend/templates/deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "backend.fullname" . }}
  labels:
    {{- include "backend.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "backend.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "backend.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: backend
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: 8000
          protocol: TCP
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: DATABASE_URL
        - name: GROQ_API_KEY
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: GROQ_API_KEY
        - name: BETTER_AUTH_SECRET
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: BETTER_AUTH_SECRET
        - name: LOG_LEVEL
          value: {{ .Values.env.logLevel | quote }}
        - name: CORS_ORIGINS
          value: {{ .Values.env.corsOrigins | quote }}
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 20
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
```

### Service Templates

**charts/frontend/templates/service.yaml**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "frontend.fullname" . }}
  labels:
    {{- include "frontend.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
  - port: {{ .Values.service.port }}
    targetPort: http
    protocol: TCP
    name: http
  selector:
    {{- include "frontend.selectorLabels" . | nindent 4 }}
```

**charts/backend/templates/service.yaml**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "backend.fullname" . }}
  labels:
    {{- include "backend.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
  - port: {{ .Values.service.port }}
    targetPort: http
    protocol: TCP
    name: http
  selector:
    {{- include "backend.selectorLabels" . | nindent 4 }}
```

---

## Helm Commands Contract

### Installation

**Install with default values**:
```bash
helm install todo-app ./helm/todo-app
```

**Install with custom values**:
```bash
helm install todo-app ./helm/todo-app \
  --values ./helm/todo-app/values-dev.yaml \
  --set secrets.databaseUrl="postgresql://..." \
  --set secrets.groqApiKey="gsk_..." \
  --set secrets.betterAuthSecret="secret_..."
```

**Expected Behavior**:
- Chart validates successfully
- All resources created in Kubernetes
- Pods start and reach Running state
- Services expose pods correctly

### Upgrade

**Upgrade deployment**:
```bash
helm upgrade todo-app ./helm/todo-app \
  --values ./helm/todo-app/values-dev.yaml
```

**Expected Behavior**:
- Rolling update of deployments
- Zero downtime (if replicas > 1)
- Old pods terminated after new pods ready

### Rollback

**Rollback to previous version**:
```bash
helm rollback todo-app
```

**Rollback to specific revision**:
```bash
helm rollback todo-app 2
```

**Expected Behavior**:
- Deployment reverted to previous state
- Pods recreated with old configuration

### Uninstall

**Remove deployment**:
```bash
helm uninstall todo-app
```

**Expected Behavior**:
- All resources deleted
- Pods terminated gracefully
- Services removed

### Validation

**Template rendering**:
```bash
helm template todo-app ./helm/todo-app
```

**Expected Output**:
- Valid Kubernetes YAML manifests
- No template errors
- All values interpolated correctly

**Dry-run installation**:
```bash
helm install todo-app ./helm/todo-app --dry-run --debug
```

**Expected Output**:
- Simulated installation
- Rendered manifests displayed
- No actual resources created

**Lint chart**:
```bash
helm lint ./helm/todo-app
```

**Expected Output**:
- No errors or warnings
- Chart follows best practices

---

## Helper Templates Contract

### _helpers.tpl (Parent Chart)

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "todo-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "todo-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-app.labels" -}}
helm.sh/chart: {{ include "todo-app.chart" . }}
{{ include "todo-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "todo-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

### _helpers.tpl (Subcharts)

Similar helper templates for frontend and backend subcharts with appropriate naming.

---

## Validation Contract

### Chart Validation

**Success Criteria**:
- `helm lint` passes with no errors
- `helm template` renders valid YAML
- All required values have defaults or are documented
- Templates follow Kubernetes API conventions

### Deployment Validation

**Success Criteria**:
- `helm install` succeeds
- All pods reach Running state within 2 minutes
- Services route traffic correctly
- ConfigMaps and Secrets mounted properly
- Health checks pass

### Upgrade Validation

**Success Criteria**:
- `helm upgrade` completes successfully
- Rolling update proceeds without errors
- No downtime for services with replicas > 1
- Old pods terminated cleanly

---

## Summary

This contract defines the structure, values, templates, and commands for Helm charts. Key aspects:

1. **Chart Structure**: Parent chart with frontend/backend subcharts
2. **Values Contract**: Default values, overrides, and environment-specific configurations
3. **Template Contract**: Kubernetes resource definitions with proper templating
4. **Commands Contract**: Installation, upgrade, rollback, and validation commands
5. **Helper Templates**: Reusable template functions for naming and labels
6. **Validation Contract**: Success criteria for chart operations

All contracts ensure consistent, maintainable, and production-ready Helm deployments.
