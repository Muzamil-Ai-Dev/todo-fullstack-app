# Environment Variables for Kubernetes Deployment

**Feature**: 006-k8s-local-deployment
**Purpose**: Document all environment variables required for deploying the Todo application to Kubernetes

## Required Environment Variables

### Database Configuration

**DATABASE_URL** (Required)
- **Description**: PostgreSQL connection string for Neon database
- **Format**: `postgresql://user:password@host:port/database?sslmode=require`
- **Example**: `postgresql://user:pass@ep-xxx.neon.tech:5432/todo_db?sslmode=require`
- **Used by**: Backend service
- **Kubernetes Secret**: `todo-secrets` key `DATABASE_URL`

### API Keys

**GROQ_API_KEY** (Required)
- **Description**: API key for Groq AI service (chatbot functionality)
- **Format**: String starting with `gsk_`
- **Example**: `gsk_xxxxxxxxxxxxxxxxxxxxx`
- **Used by**: Backend service (AI chatbot)
- **Kubernetes Secret**: `todo-secrets` key `GROQ_API_KEY`
- **Obtain from**: https://console.groq.com/keys

**BETTER_AUTH_SECRET** (Required)
- **Description**: Secret key for Better Auth authentication
- **Format**: Base64 encoded string (minimum 32 characters)
- **Example**: Generate with `openssl rand -base64 32`
- **Used by**: Backend service (authentication)
- **Kubernetes Secret**: `todo-secrets` key `BETTER_AUTH_SECRET`

### Application Configuration

**NODE_ENV** (Optional)
- **Description**: Node.js environment mode
- **Default**: `production`
- **Values**: `development`, `production`, `test`
- **Used by**: Frontend service
- **Kubernetes ConfigMap**: `todo-app-config` key `NODE_ENV`

**LOG_LEVEL** (Optional)
- **Description**: Logging verbosity level
- **Default**: `info`
- **Values**: `debug`, `info`, `warn`, `error`
- **Used by**: Backend service
- **Kubernetes ConfigMap**: `todo-app-config` key `LOG_LEVEL`

**CORS_ORIGINS** (Optional)
- **Description**: Allowed CORS origins (comma-separated)
- **Default**: `http://localhost:3000,http://todo-frontend:3000`
- **Format**: Comma-separated URLs
- **Used by**: Backend service
- **Kubernetes ConfigMap**: `todo-app-config` key `CORS_ORIGINS`

### Frontend Configuration

**NEXT_PUBLIC_API_URL** (Optional)
- **Description**: Backend API URL for frontend
- **Default**: `http://todo-backend:8000` (within cluster)
- **Format**: Full URL with protocol
- **Used by**: Frontend service
- **Kubernetes ConfigMap**: Set via Helm values

**NEXT_PUBLIC_BETTER_AUTH_URL** (Optional)
- **Description**: Better Auth URL for frontend
- **Default**: `http://localhost:3000` (for local development)
- **Format**: Full URL with protocol
- **Used by**: Frontend service
- **Kubernetes ConfigMap**: Set via Helm values

## Setting Environment Variables

### Method 1: Kubernetes Secrets (Recommended for Sensitive Data)

Create secrets using kubectl:

```bash
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="postgresql://user:pass@host:5432/db?sslmode=require" \
  --from-literal=GROQ_API_KEY="gsk_xxx" \
  --from-literal=BETTER_AUTH_SECRET="your_secret_here"
```

### Method 2: Helm Values (Recommended for Deployment)

Create a `values-local.yaml` file:

```yaml
secrets:
  databaseUrl: "postgresql://user:pass@host:5432/db?sslmode=require"
  groqApiKey: "gsk_xxx"
  betterAuthSecret: "your_secret_here"

frontend:
  env:
    nodeEnv: "production"
    apiUrl: "http://todo-backend:8000"

backend:
  env:
    logLevel: "info"
    corsOrigins: "http://localhost:3000,http://todo-frontend:3000"
```

Deploy with:

```bash
helm install todo-app ./helm/todo-app -f values-local.yaml
```

### Method 3: Helm --set Flags

```bash
helm install todo-app ./helm/todo-app \
  --set secrets.databaseUrl="postgresql://..." \
  --set secrets.groqApiKey="gsk_xxx" \
  --set secrets.betterAuthSecret="secret_xxx"
```

## Environment Variable Validation

### Backend Startup Validation

The backend service validates required environment variables on startup:

- `DATABASE_URL` - Must be valid PostgreSQL connection string
- `GROQ_API_KEY` - Must start with `gsk_`
- `BETTER_AUTH_SECRET` - Must be at least 32 characters

If any required variable is missing or invalid, the service will fail to start with a clear error message.

### Frontend Build-time Variables

Frontend environment variables prefixed with `NEXT_PUBLIC_` are embedded at build time:

- `NEXT_PUBLIC_API_URL` - Backend API endpoint
- `NEXT_PUBLIC_BETTER_AUTH_URL` - Authentication endpoint

These must be set before building the Docker image or provided via Helm values.

## Security Best Practices

1. **Never commit secrets to version control**
   - Add `values-local.yaml` to `.gitignore`
   - Use `.env.example` for documentation only

2. **Use Kubernetes Secrets for sensitive data**
   - Database credentials
   - API keys
   - Authentication secrets

3. **Use ConfigMaps for non-sensitive configuration**
   - Log levels
   - CORS origins
   - Feature flags

4. **Rotate secrets regularly**
   - Update Kubernetes secrets
   - Restart deployments to pick up new values

5. **Use different secrets per environment**
   - Development secrets
   - Staging secrets
   - Production secrets

## Troubleshooting

### Pod fails to start with "missing environment variable"

**Cause**: Required environment variable not set in Kubernetes Secret or ConfigMap

**Solution**:
1. Check secret exists: `kubectl get secret todo-secrets`
2. Verify secret contents: `kubectl get secret todo-secrets -o yaml`
3. Check pod environment: `kubectl describe pod <pod-name>`
4. Recreate secret if needed

### Backend cannot connect to database

**Cause**: Invalid `DATABASE_URL` or network connectivity issue

**Solution**:
1. Verify DATABASE_URL format is correct
2. Test connectivity from pod: `kubectl exec -it <pod-name> -- curl -v telnet://host:5432`
3. Check database firewall allows Kubernetes cluster IP range
4. Verify SSL mode is set to `require` for Neon

### Frontend cannot reach backend API

**Cause**: Incorrect `NEXT_PUBLIC_API_URL` or service not accessible

**Solution**:
1. Verify backend service exists: `kubectl get svc todo-backend`
2. Check service endpoints: `kubectl get endpoints todo-backend`
3. Test backend from frontend pod: `kubectl exec -it <frontend-pod> -- curl http://todo-backend:8000/health`
4. Update NEXT_PUBLIC_API_URL if needed and rebuild image

## Reference

- **Neon PostgreSQL**: https://neon.tech/docs/connect/connect-from-any-app
- **Groq API**: https://console.groq.com/docs/quickstart
- **Better Auth**: https://www.better-auth.com/docs/installation
- **Kubernetes Secrets**: https://kubernetes.io/docs/concepts/configuration/secret/
- **Helm Values**: https://helm.sh/docs/chart_template_guide/values_files/
