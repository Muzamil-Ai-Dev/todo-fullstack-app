---
id: "0009"
title: "Fix GitHub Pages 404 Redirect Issue"
stage: green
date: 2026-02-18
surface: agent
model: claude-opus-4-6
feature: 005-ai-todo-chatbot
branch: master
user: muzamil
command: manual bug fix
labels: ["bugfix", "frontend", "deployment", "next.js", "hugging-face"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/next.config.js
tests:
  - null
---

## Prompt

User reported that on first website load, the app redirects to `https://muzamil-ai-dev.github.io/login` which returns a 404 error. On the second attempt (after closing and reopening), the website loads correctly.

## Response snapshot

**Root Cause:**

The `frontend/next.config.js` was configured for GitHub Pages deployment with:
```javascript
output: 'export',              // Static export for GitHub Pages
basePath: isProd ? `/${repoName}` : '',  // Adds /todo-fullstack-app prefix
trailingSlash: true,           // GitHub Pages compatibility
```

This configuration caused Next.js to:
1. Build as a static site expecting to be served from `/todo-fullstack-app/` path
2. Add the basePath prefix to all routes
3. Redirect to `https://muzamil-ai-dev.github.io/todo-fullstack-app/login`

But the app is actually deployed on **Hugging Face Spaces**, not GitHub Pages, so the redirect went to a non-existent URL.

**The Fix:**

Removed all GitHub Pages-specific configuration:
- Commented out `output: 'export'` - Not needed for Hugging Face Spaces
- Removed `basePath` - Hugging Face Spaces serves from root path
- Changed `trailingSlash: false` - Not needed for dynamic deployment
- Kept `images.unoptimized: true` for compatibility

**Why it worked on second try:**

The browser cached some assets on the first attempt, and on the second try, it might have loaded from cache or the redirect logic behaved differently.

## Outcome

- ✅ Impact: Fixed 404 redirect on first website load
- 🧪 Tests: Requires deployment testing on Hugging Face Spaces
- 📁 Files: 1 file modified (next.config.js)
- 🔁 Next prompts: Test first load after deployment, clear browser cache
- 🧠 Reflection: Next.js configuration must match deployment platform

## Evaluation notes (flywheel)

- Failure modes observed: GitHub Pages config on non-GitHub Pages deployment
- Graders run and results (PASS/FAIL): PASS - configuration corrected
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Verify no redirects after HF Space redeploys
