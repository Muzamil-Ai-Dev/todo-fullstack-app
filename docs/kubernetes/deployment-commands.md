# Kubernetes Deployment Commands

This document provides the commands used to deploy the Todo Application to Minikube.

## Prerequisites

- Docker Desktop installed and running
- Minikube installed
- kubectl installed
- Helm installed
- Docker images built (todo-frontend:latest, todo-backend:latest)

## Deployment Steps

### 1. Start Minikube

```bash
minikube start --cpus=2 --memory=3500 --driver=docker
```

Verify Minikube is running:
```bash
minikube status
```

### 2. Load Docker Images into Minikube

```bash
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

Verify images are loaded:
```bash
minikube image ls | grep todo
```

### 3. Deploy with Helm

Install the application:
```bash
helm install todo-app ./helm/todo-app --values ./helm/todo-app/values-dev.yaml
```

Upgrade an existing deployment:
```bash
helm upgrade todo-app ./helm/todo-app --values ./helm/todo-app/values-dev.yaml
```

### 4. Verify Deployment

Check pods are running:
```bash
kubectl get pods
```

Check services:
```bash
kubectl get services
```

Check deployments:
```bash
kubectl get deployments
```

### 5. Access the Application

Port forward frontend:
```bash
kubectl port-forward service/todo-app-frontend 3000:3000
```

Port forward backend (in a separate terminal):
```bash
kubectl port-forward service/todo-app-backend 8000:8000
```

### 6. Test Health Endpoints

Frontend health check:
```bash
curl http://localhost:3000/api/health
```

Backend health check:
```bash
curl http://localhost:8000/health
```

### 7. View Logs

Frontend logs:
```bash
kubectl logs -l app.kubernetes.io/name=frontend
```

Backend logs:
```bash
kubectl logs -l app.kubernetes.io/name=backend
```

Follow logs in real-time:
```bash
kubectl logs -f <pod-name>
```

## Troubleshooting

### Pod Not Starting

Check pod status:
```bash
kubectl get pods
```

Describe pod for events:
```bash
kubectl describe pod <pod-name>
```

Check logs:
```bash
kubectl logs <pod-name>
```

### Secret Issues

View secret:
```bash
kubectl get secret todo-app-secrets -o yaml
```

Delete and recreate (Helm will recreate):
```bash
kubectl delete secret todo-app-secrets
helm upgrade todo-app ./helm/todo-app --values ./helm/todo-app/values-dev.yaml
```

### Image Pull Issues

Verify images in Minikube:
```bash
minikube image ls | grep todo
```

Reload images if needed:
```bash
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

## Cleanup

Uninstall Helm release:
```bash
helm uninstall todo-app
```

Stop Minikube:
```bash
minikube stop
```

Delete Minikube cluster:
```bash
minikube delete
```

## Useful Commands

Watch pods in real-time:
```bash
kubectl get pods -w
```

Get all resources:
```bash
kubectl get all
```

Describe deployment:
```bash
kubectl describe deployment todo-app-frontend
kubectl describe deployment todo-app-backend
```

Execute command in pod:
```bash
kubectl exec -it <pod-name> -- /bin/sh
```

View Helm release:
```bash
helm list
helm status todo-app
```

View rendered templates:
```bash
helm template todo-app ./helm/todo-app --values ./helm/todo-app/values-dev.yaml
```
