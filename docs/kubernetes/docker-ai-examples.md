# Docker AI (Gordon) Examples for Todo Application

This document provides practical examples of using Docker AI (Gordon) with the Todo Application.

## Prerequisites

- Docker Desktop 4.26.0 or later
- Docker Desktop Pro, Team, or Business subscription
- Todo Application Dockerfiles created

---

## Accessing Docker AI

1. Open Docker Desktop
2. Click the "Ask Gordon" button (AI icon) in the top-right corner
3. Type your question in natural language

---

## Dockerfile Optimization

### Frontend Dockerfile Analysis

**Query:**
```
"Analyze my frontend/Dockerfile and suggest optimizations for size and build time"
```

**Expected Suggestions:**
- Use specific Node.js version tags instead of `latest`
- Optimize layer caching by copying package files first
- Use `.dockerignore` to exclude unnecessary files
- Consider using `npm ci` instead of `npm install`
- Multi-stage builds to reduce final image size

### Backend Dockerfile Analysis

**Query:**
```
"Review my backend/Dockerfile and suggest security improvements"
```

**Expected Suggestions:**
- Run as non-root user (already implemented)
- Use specific Python version tags
- Scan for vulnerabilities with `docker scout`
- Minimize installed packages
- Use official base images

---

## Image Size Optimization

### Reduce Frontend Image Size

**Query:**
```
"My frontend Docker image is 293MB. How can I make it smaller?"
```

**Expected Suggestions:**
- Use alpine-based images
- Remove development dependencies in production stage
- Use `npm prune --production`
- Optimize Next.js build output
- Remove unnecessary files from final image

### Reduce Backend Image Size

**Query:**
```
"How can I reduce my Python FastAPI Docker image from 387MB?"
```

**Expected Suggestions:**
- Use `python:3.13-slim` or `python:3.13-alpine`
- Use multi-stage builds
- Remove pip cache with `--no-cache-dir`
- Only install production dependencies
- Use `.dockerignore` effectively

---

## Build Performance

### Speed Up Frontend Build

**Query:**
```
"My frontend Docker build takes too long. How can I speed it up?"
```

**Expected Suggestions:**
- Optimize layer caching order
- Use BuildKit for parallel builds
- Cache npm dependencies separately
- Use `COPY package*.json` before `COPY . .`
- Consider using build cache mounts

### Speed Up Backend Build

**Query:**
```
"How can I make my Python Docker build faster?"
```

**Expected Suggestions:**
- Use pip cache mounts
- Install dependencies in separate layer
- Use `--mount=type=cache` for pip cache
- Pre-build wheels for dependencies
- Use multi-stage builds efficiently

---

## Troubleshooting Build Issues

### Frontend Build Failures

**Query:**
```
"My Next.js Docker build fails with 'Type error' during build. What's wrong?"
```

**Expected Analysis:**
- Check TypeScript configuration
- Verify all type definitions are installed
- Review build logs for specific errors
- Ensure all dependencies are in package.json
- Check for missing environment variables

### Backend Build Failures

**Query:**
```
"Docker build fails with 'requirements.txt not found'. How do I fix this?"
```

**Expected Analysis:**
- Verify file path in COPY command
- Check build context
- Ensure requirements.txt exists
- Review .dockerignore for exclusions
- Check WORKDIR settings

---

## Security Best Practices

### Security Scan

**Query:**
```
"Scan my todo-frontend:latest image for security vulnerabilities"
```

**Expected Actions:**
- Run Docker Scout scan
- Identify CVEs in base image
- Suggest base image updates
- Recommend package updates
- Provide remediation steps

### Secrets Management

**Query:**
```
"How should I handle API keys and secrets in my Docker containers?"
```

**Expected Guidance:**
- Never hardcode secrets in Dockerfile
- Use environment variables
- Use Docker secrets in Swarm
- Use Kubernetes secrets
- Consider external secret managers

---

## Health Checks

### Add Health Checks

**Query:**
```
"How do I add health checks to my frontend Dockerfile?"
```

**Expected Example:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1
```

### Optimize Health Checks

**Query:**
```
"My health check is causing high CPU usage. How can I optimize it?"
```

**Expected Suggestions:**
- Increase interval between checks
- Use lightweight health check endpoints
- Reduce timeout values
- Consider using TCP checks instead of HTTP
- Implement efficient health check logic

---

## Multi-Stage Build Optimization

### Frontend Multi-Stage

**Query:**
```
"Explain the multi-stage build in my frontend Dockerfile and suggest improvements"
```

**Expected Analysis:**
- Stage 1: Build stage with all dev dependencies
- Stage 2: Production stage with only runtime files
- Suggestions: Copy only necessary files, optimize layer order

### Backend Multi-Stage

**Query:**
```
"How can I improve my Python multi-stage Dockerfile?"
```

**Expected Suggestions:**
- Use builder stage for compiling dependencies
- Copy only site-packages to final stage
- Remove build tools from final image
- Use virtual environments efficiently

---

## Environment-Specific Builds

### Development vs Production

**Query:**
```
"How do I create separate Docker builds for development and production?"
```

**Expected Guidance:**
- Use build arguments (ARG)
- Create separate Dockerfiles
- Use docker-compose for dev
- Optimize production for size and security
- Use different base images

### Build Arguments

**Query:**
```
"How do I pass build-time variables to my Dockerfile?"
```

**Expected Example:**
```dockerfile
ARG NODE_ENV=production
ENV NODE_ENV=$NODE_ENV
```

---

## Networking and Connectivity

### Container Communication

**Query:**
```
"My frontend container can't reach the backend container. How do I fix this?"
```

**Expected Troubleshooting:**
- Check network configuration
- Verify service names in docker-compose
- Use container names for DNS
- Check port mappings
- Review firewall rules

### External Database Connection

**Query:**
```
"How do I connect my backend container to an external Neon database?"
```

**Expected Guidance:**
- Use environment variables for connection string
- Ensure network allows outbound connections
- Check SSL/TLS requirements
- Verify credentials
- Test connectivity from container

---

## Performance Optimization

### Runtime Performance

**Query:**
```
"My Next.js container is slow. How can I improve runtime performance?"
```

**Expected Suggestions:**
- Use standalone output mode
- Enable production optimizations
- Configure proper resource limits
- Use CDN for static assets
- Optimize Next.js configuration

### Memory Usage

**Query:**
```
"My Python container uses too much memory. How can I reduce it?"
```

**Expected Suggestions:**
- Use memory-efficient base image
- Optimize Python application code
- Set memory limits
- Use gunicorn with appropriate workers
- Profile memory usage

---

## Best Practices Queries

### General Best Practices

**Query:**
```
"What are the Docker best practices for a Next.js application?"
```

**Expected Guidance:**
- Use official Node.js images
- Multi-stage builds
- Non-root user
- Proper .dockerignore
- Health checks
- Minimal final image

### Production Readiness

**Query:**
```
"Is my Dockerfile production-ready? What should I improve?"
```

**Expected Checklist:**
- Security scan results
- Image size optimization
- Health check configuration
- Logging setup
- Resource limits
- Documentation

---

## Debugging

### Container Debugging

**Query:**
```
"My container exits immediately. How do I debug it?"
```

**Expected Steps:**
- Check container logs
- Run with interactive shell
- Verify CMD/ENTRYPOINT
- Check for missing dependencies
- Review startup scripts

### Build Debugging

**Query:**
```
"How do I debug a failing Docker build?"
```

**Expected Techniques:**
- Use `docker build --progress=plain`
- Add RUN commands to inspect state
- Build up to specific stage
- Check build context
- Review build logs carefully

---

## Integration with Kubernetes

### Kubernetes Compatibility

**Query:**
```
"How do I make my Docker images work well with Kubernetes?"
```

**Expected Guidance:**
- Use imagePullPolicy correctly
- Configure health checks
- Set resource requests/limits
- Use proper logging (stdout/stderr)
- Handle signals gracefully

---

## Additional Resources

- [Docker AI Documentation](https://docs.docker.com/desktop/use-desktop/ai-assistant/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Security](https://docs.docker.com/engine/security/)
