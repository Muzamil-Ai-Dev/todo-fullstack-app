# Hugging Face Spaces Setup Guide

## Required Environment Variables

The backend requires the following environment variables to be configured in your HF Space settings:

### 1. Database Configuration
```
DATABASE_URL=postgresql://neondb_owner:npg_RgGc9Y7ulmKk@ep-bitter-sea-aibscj36-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### 2. JWT Configuration
```
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Better Auth Configuration
```
BETTER_AUTH_SECRET=your-better-auth-secret-here
BETTER_AUTH_TRUST_HOST=true
```

### 4. Groq API Configuration
```
GROQ_API_KEY=your-groq-api-key-here
```

### 5. CORS Configuration
```
BACKEND_CORS_ORIGINS=["https://muzamil-ai-dev.github.io","http://localhost:3000"]
```

### 6. Application Configuration
```
ENVIRONMENT=production
DEBUG=false
SERVER_NAME=muzamil-ai-dev-todo-backend.hf.space
SERVER_HOST=https://muzamil-ai-dev-todo-backend.hf.space
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

## How to Configure HF Space

1. Go to your HF Space: https://huggingface.co/spaces/muzamil-ai-dev/todo-backend
2. Click on "Settings" tab
3. Scroll down to "Repository secrets"
4. Add each environment variable as a secret:
   - Click "New secret"
   - Enter the variable name (e.g., `DATABASE_URL`)
   - Enter the variable value
   - Click "Add secret"
5. Repeat for all required variables
6. After adding all secrets, the Space will automatically rebuild

## Troubleshooting

### Space Stuck in "Starting" State

If your Space is stuck showing "starting" for more than 2 minutes:

1. **Check Build Logs**: Click on "Logs" tab to see build output
2. **Verify All Secrets**: Ensure all required environment variables are set
3. **Check for Errors**: Look for validation errors in logs (e.g., "Field required")
4. **Restart Space**: Click "Factory reboot" in Settings to force restart

### Common Errors

**Error: "Field required" for JWT_SECRET_KEY**
- Solution: Add `JWT_SECRET_KEY` to HF Space secrets

**Error: "Field required" for DATABASE_URL**
- Solution: Add `DATABASE_URL` to HF Space secrets with full Neon connection string

**Error: Exit code 137 (OOM)**
- Solution: Already fixed in Dockerfile with `--workers 1 --limit-concurrency 10`
- If still occurring, consider upgrading to a paid HF Space tier with more memory

**Error: Connection timeout**
- Solution: Frontend timeout increased to 60s to handle cold starts
- First request after cold start may take 30-60 seconds

### Cold Start Behavior

HF Spaces free tier has cold start delays:
- **First request**: 30-60 seconds (container startup)
- **Subsequent requests**: <1 second (while container is warm)
- **Idle timeout**: ~15 minutes (then container sleeps)

The frontend is configured with a 60-second timeout to accommodate this.

## Verification Steps

After configuring all secrets:

1. Wait for Space to rebuild (check Logs tab)
2. Once running, test the health endpoint:
   ```bash
   curl https://muzamil-ai-dev-todo-backend.hf.space/health
   ```
3. Expected response:
   ```json
   {
     "status": "healthy",
     "timestamp": "2026-02-19T11:36:00.000Z"
   }
   ```
4. Test login from frontend at https://muzamil-ai-dev.github.io/todo-fullstack-app/

## Security Notes

- Never commit secrets to the repository
- Use HF Space secrets for all sensitive values
- Rotate secrets periodically
- Use strong, randomly generated values for JWT_SECRET_KEY and BETTER_AUTH_SECRET

## Generate Secrets

To generate secure random secrets:

```bash
# JWT Secret Key (32 bytes)
openssl rand -hex 32

# Better Auth Secret (32 bytes)
openssl rand -hex 32
```

## Current Configuration Status

Based on the deployment:
- ✅ Dockerfile optimized for HF Spaces (single worker, concurrency limits)
- ✅ Frontend timeout increased to 60s
- ✅ CORS configured for GitHub Pages
- ⚠️ **ACTION REQUIRED**: Set all environment variables in HF Space secrets
