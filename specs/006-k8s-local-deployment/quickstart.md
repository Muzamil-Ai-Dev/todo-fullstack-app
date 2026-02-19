# Quickstart: Local Kubernetes Deployment

**Feature**: 006-k8s-local-deployment
**Date**: 2026-02-18
**Purpose**: Step-by-step guide to deploy the Todo application to Minikube

## Prerequisites

Before starting, ensure you have the following installed:

- **Docker Desktop** or **Docker Engine** (version 20.10+)
- **Minikube** (version 1.30+)
- **kubectl** (version 1.27+)
- **Helm** (version 3.12+)
- **Git** (for cloning the repository)

### Verify Installations

```bash
# Check Docker
docker --version
# Expected: Docker version 20.10.x or higher

# Check Minikube
minikube version
# Expected: minikube version: v1.30.x or higher

# Check kubectl
kubectl version --client
# Expected: Client Version: v1.27.x or higher

# Check Helm
helm version
# Expected: version.BuildInfo{Version:"v3.12.x" or higher}
```

---

## Step 1: Start Minikube

Start a local Kubernetes cluster with appropriate resources:

```bash
# Start Minikube with 4GB RAM and 2 CPUs
minikube start --cpus=2 --memory=4096 --driver=docker

# Verify cluster is running
minikube status
# Expected output:
# minikube
# type: Control Plane
# host: Running
# kubelet: Running
# apiserver: Running
# kubeconfig: Configured
```

**Troubleshooting**:
- If Minikube fails to start, try: `minikube delete && minikube start --cpus=2 --memory=4096 --driver=docker`
- On Windows, ensure Docker Desktop is running
- On Linux, ensure your user is in the docker group: `sudo usermod -aG docker $USER`

---

## Step 2: Build Docker Images

Navigate to the project root and build images for frontend and backend:

```bash
# Navigate to project root
cd /path/to/Todo_Application_P002

# Build frontend image
docker build -t todo-frontend:latest -f frontend/Dockerfile ./frontend

# Build backend image
docker build -t todo-backend:latest -f backend/Dockerfile ./backend

# Verify images were built
docker images | grep todo
# Expected output:
# todo-frontend    latest    <image-id>    <time>    <size>
# todo-backend     latest    <image-id>    <time>    <size>
```

**Expected Build Times**:
- Frontend: 3-5 minutes
- Backend: 2-4 minutes

**Troubleshooting**:
- If build fails, check Dockerfile syntax and ensure all source files exist
- Clear Docker cache if needed: `docker builder prune`

---

## Step 3: Load Images into Minikube

Transfer the built images to Minikube's Docker daemon:

```bash
# Load frontend image
minikube image load todo-frontend:latest

# Load backend image
minikube image load todo-backend:latest

# Verify images are loaded
minikube image ls | grep todo
# Expected output:
# docker.io/library/todo-frontend:latest
# docker.io/library/todo-backend:latest
```

**Note**: This step is crucial - Kubernetes will fail to pull images if they're not loaded into Minikube.

---

## Step 4: Create Kubernetes Secrets

Create a secret with your database credentials and API keys:

```bash
# Create secrets (replace with your actual values)
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="postgresql://user:password@ep-xxx.neon.tech:5432/todo_db?sslmode=require" \
  --from-literal=GROQ_API_KEY="gsk_your_groq_api_key" \
  --from-literal=BETTER_AUTH_SECRET="your_better_auth_secret"

# Verify secret was created
kubectl get secrets
# Expected output:
# NAME           TYPE     DATA   AGE
# todo-secrets   Opaque   3      <time>
```

**Security Note**: Never commit secrets to version control. Use environment variables or a secrets management tool.

**Get Your Credentials**:
- **DATABASE_URL**: From your Neon PostgreSQL dashboard
- **GROQ_API_KEY**: From https://console.groq.com/keys
- **BETTER_AUTH_SECRET**: Generate with `openssl rand -base64 32`

---

## Step 5: Deploy with Helm

Install the application using Helm:

```bash
# Navigate to Helm chart directory
cd helm/todo-app

# Install the chart
helm install todo-app . \
  --set secrets.databaseUrl="postgresql://user:password@ep-xxx.neon.tech:5432/todo_db?sslmode=require" \
  --set secrets.groqApiKey="gsk_your_groq_api_key" \
  --set secrets.betterAuthSecret="your_better_auth_secret"

# Verify deployment
helm list
# Expected output:
# NAME      NAMESPACE  REVISION  UPDATED                   STATUS    CHART           APP VERSION
# todo-app  default    1         2026-02-18 18:00:00 UTC   deployed  todo-app-1.0.0  1.0.0
```

**Alternative**: Use a values file for cleaner command:

```bash
# Create values-local.yaml with your secrets
cat > values-local.yaml <<EOF
secrets:
  databaseUrl: "postgresql://user:password@ep-xxx.neon.tech:5432/todo_db?sslmode=require"
  groqApiKey: "gsk_your_groq_api_key"
  betterAuthSecret: "your_better_auth_secret"
EOF

# Install with values file
helm install todo-app . -f values-local.yaml
```

---

## Step 6: Verify Deployment

Check that all pods are running:

```bash
# Check pod status
kubectl get pods
# Expected output:
# NAME                            READY   STATUS    RESTARTS   AGE
# todo-frontend-xxxxxxxxxx-xxxxx  1/1     Running   0          30s
# todo-backend-xxxxxxxxxx-xxxxx   1/1     Running   0          30s

# Check services
kubectl get services
# Expected output:
# NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
# todo-frontend   ClusterIP   10.96.xxx.xxx   <none>        3000/TCP   30s
# todo-backend    ClusterIP   10.96.xxx.xxx   <none>        8000/TCP   30s

# Check deployment status
kubectl get deployments
# Expected output:
# NAME            READY   UP-TO-DATE   AVAILABLE   AGE
# todo-frontend   1/1     1            1           30s
# todo-backend    1/1     1            1           30s
```

**Troubleshooting**:
- If pods are in `ImagePullBackOff`: Images not loaded into Minikube (repeat Step 3)
- If pods are in `CrashLoopBackOff`: Check logs with `kubectl logs <pod-name>`
- If pods are `Pending`: Check resource availability with `kubectl describe pod <pod-name>`

---

## Step 7: Access the Application

Use port-forwarding to access the application locally:

```bash
# Port-forward frontend (in one terminal)
kubectl port-forward svc/todo-frontend 3000:3000

# Port-forward backend (in another terminal)
kubectl port-forward svc/todo-backend 8000:8000
```

**Access the Application**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend Health: http://localhost:8000/health
- API Docs: http://localhost:8000/docs

**Expected Behavior**:
- Frontend loads successfully
- You can log in and see the todo list
- AI chatbot is accessible and functional
- All Phase III features work correctly

---

## Step 8: View Logs

Monitor application logs:

```bash
# View frontend logs
kubectl logs -f deployment/todo-frontend

# View backend logs
kubectl logs -f deployment/todo-backend

# View logs from specific pod
kubectl logs -f <pod-name>

# View logs from all pods with label
kubectl logs -l app.kubernetes.io/name=frontend --tail=50
```

---

## Common Operations

### Scale Deployments

```bash
# Scale frontend to 2 replicas
kubectl scale deployment todo-frontend --replicas=2

# Scale backend to 2 replicas
kubectl scale deployment todo-backend --replicas=2

# Verify scaling
kubectl get pods
```

### Update Application

```bash
# Rebuild images (after code changes)
docker build -t todo-frontend:latest -f frontend/Dockerfile ./frontend
docker build -t todo-backend:latest -f backend/Dockerfile ./backend

# Reload images into Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest

# Restart deployments to use new images
kubectl rollout restart deployment/todo-frontend
kubectl rollout restart deployment/todo-backend

# Watch rollout status
kubectl rollout status deployment/todo-frontend
kubectl rollout status deployment/todo-backend
```

### Upgrade with Helm

```bash
# Update Helm chart or values
helm upgrade todo-app . -f values-local.yaml

# Check upgrade status
helm list
helm history todo-app
```

### Rollback Deployment

```bash
# Rollback to previous version
helm rollback todo-app

# Rollback to specific revision
helm rollback todo-app 2
```

### Delete Deployment

```bash
# Uninstall Helm release
helm uninstall todo-app

# Verify resources are deleted
kubectl get all
```

---

## Using AIOps Tools (Optional)

Enhance your Kubernetes and Docker operations with AI-powered tools. See detailed documentation in `docs/kubernetes/aiops-setup.md`.

### kubectl-ai

Install and use kubectl-ai for natural language Kubernetes operations:

```bash
# Install kubectl-ai via krew
kubectl krew install ai

# Set OpenAI API key
export OPENAI_API_KEY="your-api-key"

# Use natural language commands
kubectl ai "show me all pods"
kubectl ai "scale the frontend to 3 replicas"
kubectl ai "check why the backend pod is failing"
kubectl ai "show resource usage"
```

**Examples**: See `docs/kubernetes/kubectl-ai-examples.md` for comprehensive examples specific to this project.

### Docker AI (Gordon)

Use Docker Desktop's built-in AI assistant for Dockerfile optimization:

1. Open Docker Desktop
2. Click "Ask Gordon" (AI icon) in top-right
3. Ask questions like:
   - "Optimize my frontend/Dockerfile for production"
   - "How can I reduce my image size?"
   - "Scan my images for security vulnerabilities"

**Examples**: See `docs/kubernetes/docker-ai-examples.md` for detailed Docker AI usage examples.

### Additional Resources

- **AIOps Setup Guide**: `docs/kubernetes/aiops-setup.md`
- **kubectl-ai Examples**: `docs/kubernetes/kubectl-ai-examples.md`
- **Docker AI Examples**: `docs/kubernetes/docker-ai-examples.md`

---

## Troubleshooting Guide

### Pods Not Starting

```bash
# Check pod events
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Check resource constraints
kubectl top nodes
kubectl top pods
```

### Database Connection Issues

```bash
# Verify secret exists
kubectl get secret todo-secrets -o yaml

# Check backend logs for connection errors
kubectl logs deployment/todo-backend | grep -i database

# Test database connectivity from pod
kubectl exec -it <backend-pod-name> -- curl -v telnet://ep-xxx.neon.tech:5432
```

### Image Pull Errors

```bash
# Verify images are loaded
minikube image ls | grep todo

# Reload images if missing
minikube image load todo-frontend:latest
minikube image load todo-backend:latest

# Restart deployment
kubectl rollout restart deployment/todo-frontend
kubectl rollout restart deployment/todo-backend
```

### Port-Forward Not Working

```bash
# Check if service exists
kubectl get svc

# Check if pods are running
kubectl get pods

# Try different port
kubectl port-forward svc/todo-frontend 8080:3000
```

---

## Cleanup

When you're done testing:

```bash
# Uninstall Helm release
helm uninstall todo-app

# Delete secrets
kubectl delete secret todo-secrets

# Stop Minikube
minikube stop

# (Optional) Delete Minikube cluster
minikube delete
```

---

## Next Steps

After successfully deploying to Minikube:

1. **Phase V**: Deploy to cloud Kubernetes (GKE, AKS, or DOKS)
2. **Add Ingress**: Configure ingress controller for external access
3. **Add Monitoring**: Set up Prometheus and Grafana
4. **Add CI/CD**: Automate builds and deployments with GitHub Actions
5. **Add Dapr**: Implement event-driven architecture with Kafka

---

## Quick Reference

### Essential Commands

```bash
# Cluster
minikube start --cpus=2 --memory=4096
minikube status
minikube stop

# Images
docker build -t <name>:<tag> -f <dockerfile> <context>
minikube image load <name>:<tag>
minikube image ls

# Helm
helm install <release> <chart>
helm upgrade <release> <chart>
helm uninstall <release>
helm list

# Kubernetes
kubectl get pods
kubectl get services
kubectl get deployments
kubectl logs <pod-name>
kubectl describe pod <pod-name>
kubectl port-forward svc/<service> <local-port>:<service-port>
```

### Useful Aliases

```bash
alias k=kubectl
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kgd='kubectl get deployments'
alias kl='kubectl logs -f'
alias kpf='kubectl port-forward'
```

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review pod logs: `kubectl logs <pod-name>`
3. Check pod events: `kubectl describe pod <pod-name>`
4. Verify Minikube status: `minikube status`
5. Consult Kubernetes documentation: https://kubernetes.io/docs/

**Success Criteria**: Application is accessible at http://localhost:3000 with all Phase III features working correctly.
