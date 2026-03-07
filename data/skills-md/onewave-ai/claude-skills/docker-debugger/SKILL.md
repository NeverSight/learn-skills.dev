---
name: docker-debugger
description: Debug Docker containers, fix Dockerfile issues, optimize images, and troubleshoot docker-compose. Use when having Docker problems, container issues, or optimizing Docker builds.
---

# Docker Debugger

## Instructions

When debugging Docker issues:

1. **Identify the problem type**: Build, runtime, networking, or performance
2. **Gather information** using diagnostic commands
3. **Analyze logs and errors**
4. **Apply fixes**

## Diagnostic Commands

```bash
# Check running containers
docker ps -a

# View container logs
docker logs <container_id> --tail 100 -f

# Inspect container
docker inspect <container_id>

# Check resource usage
docker stats

# View container processes
docker top <container_id>

# Execute shell in running container
docker exec -it <container_id> /bin/sh

# Check Docker disk usage
docker system df

# View build history
docker history <image_name>
```

## Common Issues & Solutions

### 1. Container exits immediately

```bash
# Check exit code
docker inspect <container_id> --format='{{.State.ExitCode}}'

# View last logs
docker logs <container_id>
```

**Fixes**:
- Ensure CMD/ENTRYPOINT runs a foreground process
- Check for missing dependencies
- Verify environment variables

### 2. Build fails

```dockerfile
# Use multi-stage builds for smaller images
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

### 3. Networking issues

```bash
# List networks
docker network ls

# Inspect network
docker network inspect <network_name>

# Check container IP
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container>
```

### 4. Volume permission issues

```dockerfile
# Create non-root user
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# Set ownership
COPY --chown=appuser:appgroup . .

USER appuser
```

## Dockerfile Best Practices

```dockerfile
# 1. Use specific tags, not :latest
FROM node:20.10-alpine

# 2. Set working directory
WORKDIR /app

# 3. Copy dependency files first (better caching)
COPY package*.json ./
RUN npm ci --only=production

# 4. Copy source after dependencies
COPY . .

# 5. Use non-root user
USER node

# 6. Set proper labels
LABEL maintainer="you@example.com"
LABEL version="1.0"

# 7. Use HEALTHCHECK
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget -q --spider http://localhost:3000/health || exit 1

# 8. Expose ports
EXPOSE 3000

# 9. Use exec form for CMD
CMD ["node", "server.js"]
```

## docker-compose Debugging

```yaml
# docker-compose.yml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    # Add for debugging
    stdin_open: true
    tty: true
    # Override command for debugging
    command: /bin/sh
    volumes:
      - .:/app
    environment:
      - DEBUG=true
```

```bash
# Rebuild without cache
docker-compose build --no-cache

# View logs
docker-compose logs -f app

# Restart single service
docker-compose restart app
```
