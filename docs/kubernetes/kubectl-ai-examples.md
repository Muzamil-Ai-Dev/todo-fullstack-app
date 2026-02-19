# kubectl-ai Examples for Todo Application

This document provides practical examples of using kubectl-ai with the Todo Application deployment.

## Prerequisites

- kubectl-ai installed (`kubectl krew install ai`)
- OpenAI API key configured (`export OPENAI_API_KEY="your-key"`)
- Todo Application deployed to Minikube

---

## Deployment Management

### Check Deployment Status

```bash
# Natural language query
kubectl ai "show me the status of all todo-app deployments"

# Expected output: Lists frontend and backend deployments with replica counts
```

### Scale Applications

```bash
# Scale frontend
kubectl ai "scale the todo-app-frontend deployment to 3 replicas"

# Scale backend
kubectl ai "scale the todo-app-backend deployment to 2 replicas"

# Scale both
kubectl ai "scale all todo-app deployments to 2 replicas"
```

### Update Deployments

```bash
# Update image
kubectl ai "update the todo-app-frontend deployment to use image todo-frontend:v2"

# Restart deployment
kubectl ai "restart the todo-app-backend deployment"
```

---

## Pod Management

### List and Filter Pods

```bash
# All todo-app pods
kubectl ai "show me all pods related to todo-app"

# Only running pods
kubectl ai "show me running todo-app pods"

# Pods with issues
kubectl ai "show me any todo-app pods that are not running"
```

### Pod Troubleshooting

```bash
# Check why pod is failing
kubectl ai "why is the todo-app-backend pod crashing?"

# Get pod events
kubectl ai "show me recent events for todo-app-backend pod"

# Check pod resource usage
kubectl ai "how much CPU and memory is the frontend pod using?"
```

### Pod Logs

```bash
# Get recent logs
kubectl ai "show me the last 50 lines of logs from the backend pod"

# Follow logs
kubectl ai "stream logs from the todo-app-frontend pod"

# Search logs for errors
kubectl ai "show me any error messages in the backend pod logs"
```

---

## Service and Networking

### Service Information

```bash
# List services
kubectl ai "show me all services for todo-app"

# Get service endpoints
kubectl ai "what are the endpoints for the todo-app-backend service?"

# Check service connectivity
kubectl ai "can the frontend service reach the backend service?"
```

### Port Forwarding

```bash
# Setup port forward
kubectl ai "forward port 3000 from the todo-app-frontend service"

# Multiple ports
kubectl ai "forward ports 3000 and 8000 from todo-app services"
```

---

## Resource Management

### Resource Usage

```bash
# Check resource consumption
kubectl ai "show me CPU and memory usage for all todo-app pods"

# Find resource-hungry pods
kubectl ai "which todo-app pod is using the most memory?"

# Check resource limits
kubectl ai "what are the resource limits for the backend deployment?"
```

### Resource Optimization

```bash
# Suggest optimizations
kubectl ai "suggest resource optimizations for todo-app deployments"

# Check if resources are sufficient
kubectl ai "are the todo-app pods getting enough resources?"
```

---

## Configuration and Secrets

### ConfigMaps and Secrets

```bash
# List secrets
kubectl ai "show me all secrets used by todo-app"

# Check secret values (base64 decoded)
kubectl ai "what environment variables are in the todo-app-secrets secret?"

# Verify secret is mounted
kubectl ai "is the todo-app-secrets secret mounted in the backend pod?"
```

### Environment Variables

```bash
# List env vars
kubectl ai "what environment variables are set in the backend pod?"

# Check specific variable
kubectl ai "what is the value of DATABASE_URL in the backend pod?"
```

---

## Troubleshooting Scenarios

### Scenario 1: Pod Won't Start

```bash
kubectl ai "the todo-app-backend pod won't start, what's wrong?"
kubectl ai "show me the events for the failing backend pod"
kubectl ai "check if the backend pod has image pull errors"
```

### Scenario 2: Application Not Accessible

```bash
kubectl ai "I can't access the frontend at localhost:3000, help me debug"
kubectl ai "is the frontend service properly configured?"
kubectl ai "check if port forwarding is working for the frontend"
```

### Scenario 3: Database Connection Issues

```bash
kubectl ai "the backend can't connect to the database, what should I check?"
kubectl ai "verify the DATABASE_URL secret is correct"
kubectl ai "check if the backend pod can reach external services"
```

### Scenario 4: High Resource Usage

```bash
kubectl ai "the backend pod is using too much memory, what can I do?"
kubectl ai "show me memory usage trends for the backend pod"
kubectl ai "suggest memory limit adjustments for the backend"
```

---

## Health Checks

### Liveness and Readiness Probes

```bash
# Check probe configuration
kubectl ai "show me the health check configuration for the backend"

# Verify probes are passing
kubectl ai "are the liveness probes passing for all todo-app pods?"

# Troubleshoot failing probes
kubectl ai "why is the readiness probe failing for the backend pod?"
```

### Application Health

```bash
# Test health endpoints
kubectl ai "test the health endpoint of the backend service"

# Check overall health
kubectl ai "is the todo-app healthy and ready to serve traffic?"
```

---

## Helm Integration

### Helm Release Information

```bash
# Check Helm release
kubectl ai "show me information about the todo-app helm release"

# List Helm values
kubectl ai "what values are configured for the todo-app helm chart?"

# Check Helm revision
kubectl ai "what revision is the todo-app helm release at?"
```

---

## Advanced Queries

### Multi-Resource Queries

```bash
# Complete status
kubectl ai "give me a complete status report of the todo-app deployment"

# Resource relationships
kubectl ai "show me how the frontend and backend services are connected"

# Dependency check
kubectl ai "what resources does the backend deployment depend on?"
```

### Performance Analysis

```bash
# Response times
kubectl ai "analyze response times for the backend service"

# Request rates
kubectl ai "how many requests per second is the frontend handling?"

# Error rates
kubectl ai "what's the error rate for the backend API?"
```

### Capacity Planning

```bash
# Current capacity
kubectl ai "what's the current capacity of the todo-app deployment?"

# Scaling recommendations
kubectl ai "should I scale up the frontend based on current load?"

# Resource forecasting
kubectl ai "predict resource needs if I scale to 5 replicas"
```

---

## Best Practices

### Effective Queries

**Good:**
- "Show me pods that are not running in the default namespace"
- "What's the CPU usage of the backend deployment?"
- "Why is the frontend pod restarting?"

**Less Effective:**
- "Fix my app" (too vague)
- "Make it faster" (unclear what to optimize)
- "Deploy everything" (too broad)

### Safety Tips

1. **Review Before Executing**: Always review commands kubectl-ai suggests
2. **Start Small**: Test queries on non-critical resources first
3. **Understand Output**: Make sure you understand what kubectl-ai is showing you
4. **Verify Changes**: After kubectl-ai makes changes, verify they worked as expected

### Common Pitfalls

- Don't rely solely on AI for critical operations
- Verify resource names before deletion commands
- Check namespace context before operations
- Review suggested resource limits before applying

---

## Troubleshooting kubectl-ai

### kubectl-ai Not Working

```bash
# Check installation
kubectl plugin list | grep ai

# Verify API key
echo $OPENAI_API_KEY

# Test with simple query
kubectl ai "list all pods"
```

### Inaccurate Responses

- Be more specific in your queries
- Provide context (namespace, resource names)
- Break complex queries into smaller ones
- Verify kubectl-ai's suggestions with kubectl commands

---

## Additional Resources

- [kubectl-ai GitHub Repository](https://github.com/sozercan/kubectl-ai)
- [kubectl-ai Documentation](https://github.com/sozercan/kubectl-ai/blob/main/README.md)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
