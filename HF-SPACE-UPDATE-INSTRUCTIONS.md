# Push Backend Changes to Hugging Face Space

The HF Space is now responding (health check passed!), but we should update it with the correct port configuration.

## Option 1: Manual Update (Recommended - 2 minutes)

1. Go to: https://huggingface.co/spaces/Muzamil-Ai-Dev/todo-backend/tree/main
2. Click on `Dockerfile`
3. Click "Edit" button
4. Change line 31 from:
   ```
   EXPOSE 8000
   ```
   to:
   ```
   EXPOSE 7860
   ```
5. Change line 34 from:
   ```
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--limit-concurrency", "10"]
   ```
   to:
   ```
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1", "--limit-concurrency", "10"]
   ```
6. Click "Commit changes to main"
7. Wait 2-3 minutes for rebuild

## Option 2: Git Push (Requires HF Token)

```bash
# Add HF Space as remote
git remote add hf-space https://huggingface.co/spaces/Muzamil-Ai-Dev/todo-backend

# Configure git to use your HF token
git config credential.helper store

# Push backend changes (will prompt for username and token)
# Username: Muzamil-Ai-Dev
# Password: <your-hf-token>
cd backend
git subtree push --prefix=backend hf-space main
```

## Current Status

✅ **HF Space is WORKING!**
- Health endpoint responding: `{"status":"healthy","service":"todo-api"}`
- URL: https://muzamil-ai-dev-todo-backend.hf.space/health
- Port: Currently running on 8000 (works but should be 7860 for HF standards)

## Test Your Application

Now that HF Space is working, test the full application:

1. **Frontend**: https://muzamil-ai-dev.github.io/todo-fullstack-app/
2. **Try to login** - should work now without timeout!
3. **Create tasks** - test full functionality

The 60-second timeout issue should be resolved now that the backend is responding.
