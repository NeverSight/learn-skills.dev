---
name: docker-patterns
description: Best practices for containerizing applications with Docker.
---


# Docker Patterns Skill

## Purpose
Best practices for containerizing applications with Docker.

## When to Use
- Creating new Dockerfiles
- Optimizing existing images
- Setting up local development environments
- Preparing for production deployment

## Dockerfile Patterns

### Multi-Stage Build (Recommended)
Separate build and runtime environments to minimize image size.

```dockerfile
# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Copy only runtime dependencies
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Run as non-root user
RUN useradd -m -r appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Node.js Pattern
```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY package*.json ./

USER node

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Go Pattern
```dockerfile
# Build stage
FROM golang:1.22-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/server

# Production stage - scratch for minimal size
FROM scratch

COPY --from=builder /app/server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

EXPOSE 8080
ENTRYPOINT ["/server"]
```

## Layer Optimization

### Order by Change Frequency
Put rarely-changing layers first to maximize cache hits.

```dockerfile
# Least frequently changed (maximize cache)
FROM python:3.12-slim
WORKDIR /app

# Dependencies change occasionally
COPY requirements.txt .
RUN pip install -r requirements.txt

# Application code changes frequently
COPY . .

CMD ["python", "main.py"]
```

### Combine RUN Commands
Reduce layers by combining commands.

```dockerfile
# Bad - 3 layers
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# Good - 1 layer
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
```

## Security Best Practices

### Non-Root User
```dockerfile
# Create and switch to non-root user
RUN useradd -m -r -s /bin/false appuser
USER appuser
```

### Read-Only Filesystem
```yaml
# docker-compose.yml
services:
  app:
    read_only: true
    tmpfs:
      - /tmp
```

### Pin Base Image Versions
```dockerfile
# Bad - unpredictable
FROM python:latest

# Good - reproducible
FROM python:3.12.1-slim-bookworm
```

### Scan for Vulnerabilities
```bash
# Using Docker Scout
docker scout cves myimage:latest

# Using Trivy
trivy image myimage:latest
```

## .dockerignore
Always include to avoid copying unnecessary files.

```dockerignore
# Git
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
.venv
venv

# Node
node_modules
npm-debug.log

# IDE
.vscode
.idea
*.swp

# Docker
Dockerfile*
docker-compose*
.docker

# Local config
.env
*.local

# Build artifacts
dist
build
*.egg-info

# Tests
tests
*_test.py
test_*

# Documentation
docs
*.md
!README.md
```

## Docker Compose Patterns

### Development Environment
```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      target: development
    volumes:
      - .:/app                    # Live reload
      - /app/node_modules         # Preserve node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=true
    ports:
      - "3000:3000"
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: devpass
      POSTGRES_DB: devdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Production Environment
```yaml
version: '3.8'

services:
  app:
    image: myregistry/myapp:${VERSION:-latest}
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
      restart_policy:
        condition: on-failure
        max_attempts: 3
    environment:
      - NODE_ENV=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

## Health Checks

### HTTP Health Check
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

### Custom Health Check Script
```dockerfile
COPY healthcheck.sh /usr/local/bin/
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD healthcheck.sh
```

## Environment Variables

### Build-time vs Runtime
```dockerfile
# Build-time arguments (not in final image)
ARG BUILD_VERSION=unknown

# Runtime environment variables
ENV APP_VERSION=${BUILD_VERSION}
ENV LOG_LEVEL=info
```

### Using .env Files
```yaml
# docker-compose.yml
services:
  app:
    env_file:
      - .env                    # Base config
      - .env.${ENV:-local}      # Environment-specific
```

## Networking

### Custom Networks
```yaml
services:
  frontend:
    networks:
      - frontend
      - backend

  api:
    networks:
      - backend

  db:
    networks:
      - backend

networks:
  frontend:
  backend:
    internal: true  # No external access
```

## Volume Patterns

### Named Volumes for Persistence
```yaml
volumes:
  postgres_data:
    driver: local
  redis_data:
```

### Bind Mounts for Development
```yaml
volumes:
  - ./src:/app/src:ro          # Read-only
  - ./config:/app/config       # Read-write
```

## Common Issues & Solutions

### Issue: Large Image Size
```bash
# Check what's taking space
docker history myimage:latest

# Solutions:
# - Use multi-stage builds
# - Use slim/alpine base images
# - Clean up package manager cache
# - Use .dockerignore
```

### Issue: Slow Builds
```bash
# Solutions:
# - Optimize layer ordering
# - Use BuildKit: DOCKER_BUILDKIT=1
# - Use cache mounts for package managers
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

### Issue: Container Won't Start
```bash
# Debug steps:
docker logs <container>
docker exec -it <container> /bin/sh
docker inspect <container>
```

## Checklist

Before deploying:
- [ ] Using specific base image version
- [ ] Multi-stage build implemented
- [ ] Running as non-root user
- [ ] .dockerignore configured
- [ ] Health check defined
- [ ] Resource limits set
- [ ] Secrets not in image
- [ ] Image scanned for vulnerabilities
- [ ] Logging configured
- [ ] Graceful shutdown handled
