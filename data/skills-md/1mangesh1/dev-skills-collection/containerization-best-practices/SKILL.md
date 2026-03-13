---
name: containerization-best-practices
description: Container and Docker best practices. Use when user asks to "optimize Docker", "Docker best practices", "container security", "image optimization", "layer caching", "multi-stage builds", "container networking", "volume management", "Docker performance", or mentions containerization strategies and Docker optimization.
---

# Containerization & Docker Best Practices

Advanced Docker and containerization strategies for building efficient, secure, and maintainable containers.

## Dockerfile Best Practices

### Multi-Stage Build
```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM node:18-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

### Layer Caching Optimization
```dockerfile
# Bad - rebuilds on every code change
FROM node:18
COPY . .
RUN npm install

# Good - leverages layer caching
FROM node:18
COPY package*.json ./
RUN npm install
COPY . .
```

### Minimal Base Images
```dockerfile
# Large ~330MB
FROM ubuntu:22.04

# Better ~100MB
FROM node:18

# Best ~50MB (Alpine)
FROM node:18-alpine
```

## Image Size Optimization

- Use alpine variants (-alpine, -slim)
- Multi-stage builds to exclude build dependencies
- .dockerignore file to exclude files
- Remove package manager caches
- Use specific versions (not latest)

### Example .dockerignore
```
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.DS_Store
coverage
tests
```

## Security Best Practices

### Run as Non-Root
```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

### No Secrets in Images
```dockerfile
# Bad - secrets in image
RUN npm install --password=$DB_PASSWORD

# Good - use build args or env at runtime
ARG NPM_TOKEN
RUN npm install --no-optional
```

### Scan Images
```bash
docker scan myapp:latest
trivy image myapp:latest
```

### Network Security
- Use specific base images (not ubuntu)
- Keep images updated
- Remove unnecessary tools
- Use read-only filesystems where possible

## Container Networking

### Bridge Networks
```bash
docker network create myapp-net
docker run --network myapp-net myapp
```

### Environment Variables
```dockerfile
ENV NODE_ENV=production
ENV LOG_LEVEL=info
```

## Volume Management

### Named Volumes
```bash
docker volume create appdata
docker run -v appdata:/data myapp
```

### Bind Mounts
```bash
docker run -v /host/path:/container/path myapp
```

## Performance Optimization

1. **Base Image**: Use minimal base images
2. **Layer Caching**: Order commands by change frequency
3. **Compression**: Use BuildKit for better caching
4. **Concurrent Builds**: Parallel layer building

### Enable BuildKit
```bash
export DOCKER_BUILDKIT=1
docker build -t myapp .
```

## Docker Compose Best Practices

```yaml
version: '3.8'
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - NODE_ENV=production
    volumes:
      - appdata:/data
    networks:
      - appnet
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 30s
      timeout: 10s

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  appdata:
  pgdata:

networks:
  appnet:
```

## Image Registry Best Practices

- Tag images semantically (version, git-sha, latest)
- Use private registries for proprietary code
- Regular cleanup of old images
- Implement image signing and verification

### Semantic Tagging
```bash
docker tag myapp:latest myapp:1.0.0
docker tag myapp:latest myapp:2024-02-07
docker tag myapp:latest myapp:${GIT_SHA}
```

## Debugging Containers

```bash
# Execute command in running container
docker exec -it container-id bash

# View logs
docker logs container-id
docker logs -f container-id

# Inspect resource usage
docker stats

# Debug image layers
docker history myapp:latest
```

## References

- Docker Documentation
- Google Container Best Practices
- Kubernetes Documentation
- 12-Factor App Methodology
- Container Image Spec (OCI)
