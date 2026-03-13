---
name: docker-deployment
description: Production-ready Docker configurations, multi-stage builds, and deployment best practices
---

# Docker Deployment Skill

Provides production-ready Docker configurations, multi-stage builds, and deployment best practices.

## Purpose

This skill provides:
- Optimized Dockerfile patterns for different tech stacks
- Multi-stage build strategies
- Docker Compose configurations
- Container security best practices
- Docker registry integration
- Health checks and monitoring

## When to Use

- "Create a Dockerfile for Node.js app"
- "Optimize Docker image size"
- "Set up Docker Compose for microservices"
- "Implement Docker health checks"
- "Deploy with Docker Swarm/Kubernetes"

## Node.js Dockerfile (Multi-Stage Build)

```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (including dev dependencies for build)
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Prune dev dependencies
RUN npm prune --production

# Production stage
FROM node:20-alpine AS production

# Add non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# Copy built artifacts and production dependencies
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/package*.json ./

# Use non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Start application
CMD ["node", "dist/index.js"]
```

## Next.js Dockerfile

```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000
ENV PORT 3000

CMD ["node", "server.js"]
```

## Python FastAPI Dockerfile

```dockerfile
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Add local bin to PATH
ENV PATH=/root/.local/bin:$PATH

# Create non-root user
RUN useradd -m -u 1001 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Docker Compose - Full Stack Application

```yaml
version: '3.9'

services:
  # Frontend (Next.js)
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://api:4000
    depends_on:
      api:
        condition: service_healthy
    networks:
      - app-network
    restart: unless-stopped

  # Backend API (Node.js)
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    ports:
      - "4000:4000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/myapp
      - REDIS_URL=redis://redis:6379
      - NODE_ENV=production
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:4000/health')"]
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 30s
    networks:
      - app-network
    restart: unless-stopped
    volumes:
      - ./api/uploads:/app/uploads

  # PostgreSQL Database
  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=myapp
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - app-network
    restart: unless-stopped

  # Redis Cache
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - app-network
    restart: unless-stopped

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
      - api
    networks:
      - app-network
    restart: unless-stopped

networks:
  app-network:
    driver: bridge

volumes:
  postgres-data:
  redis-data:
```

## Docker Security Best Practices

### Minimal Base Image

```dockerfile
# Use distroless for minimal attack surface
FROM gcr.io/distroless/nodejs20-debian12

WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules

CMD ["dist/index.js"]
```

### Multi-Layer Security

```dockerfile
FROM node:20-alpine

# Security: Run as non-root
RUN addgroup -g 1001 app && \
    adduser -D -u 1001 -G app app

WORKDIR /app

# Security: Use specific versions
COPY package*.json ./
RUN npm ci --only=production && \
    npm cache clean --force

# Security: Set file permissions
COPY --chown=app:app . .

# Security: Drop capabilities
USER app

# Security: Read-only filesystem
# (mount volumes for writable areas)
VOLUME ["/app/data"]

EXPOSE 3000

CMD ["node", "index.js"]
```

### .dockerignore

```
# Dependencies
node_modules
npm-debug.log

# Testing
coverage
.jest
*.test.js

# Environment
.env
.env.local
.env.*.local

# Git
.git
.gitignore

# CI/CD
.github
.gitlab-ci.yml

# Documentation
README.md
docs/

# Build artifacts
dist
build
*.log

# IDE
.vscode
.idea
*.swp
```

## Docker Registry & CI/CD

### GitHub Container Registry

```yaml
# .github/workflows/docker-publish.yml
name: Docker Build & Push

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Health Checks

### Node.js Health Endpoint

```typescript
// health.ts
export function setupHealthCheck(app: Express) {
  app.get('/health', async (req, res) => {
    const checks = {
      uptime: process.uptime(),
      timestamp: Date.now(),
      database: await checkDatabase(),
      redis: await checkRedis(),
      memory: process.memoryUsage(),
    }

    const isHealthy = checks.database && checks.redis

    res.status(isHealthy ? 200 : 503).json(checks)
  })
}

async function checkDatabase(): Promise<boolean> {
  try {
    await db.raw('SELECT 1')
    return true
  } catch {
    return false
  }
}

async function checkRedis(): Promise<boolean> {
  try {
    await redis.ping()
    return true
  } catch {
    return false
  }
}
```

## Monitoring & Logging

### Docker Compose with Logging

```yaml
services:
  app:
    image: myapp:latest
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    labels:
      - "prometheus.scrape=true"
      - "prometheus.port=9090"
```

### Prometheus Metrics Endpoint

```typescript
// metrics.ts
import promClient from 'prom-client'

const register = new promClient.Registry()

promClient.collectDefaultMetrics({ register })

const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_ms',
  help: 'Duration of HTTP requests in ms',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [10, 50, 100, 500, 1000, 5000],
})

register.registerMetric(httpRequestDuration)

export function setupMetrics(app: Express) {
  app.get('/metrics', async (req, res) => {
    res.set('Content-Type', register.contentType)
    res.end(await register.metrics())
  })
}
```

## Best Practices Checklist

- ✅ Use multi-stage builds to minimize image size
- ✅ Run containers as non-root user
- ✅ Use specific base image versions (not `latest`)
- ✅ Implement health checks
- ✅ Set resource limits (CPU/memory)
- ✅ Use `.dockerignore` to exclude unnecessary files
- ✅ Scan images for vulnerabilities (Snyk, Trivy)
- ✅ Use secrets management (not env vars for sensitive data)
- ✅ Implement proper logging
- ✅ Add monitoring and metrics

## Integration with Agents

Works best with:
- **devops-automation** agent - Generates Docker configs
- **security-auditor** agent - Scans for container vulnerabilities
- **performance-optimizer** agent - Optimizes image size and startup time

## Tools & Resources

- **Docker**: Official container platform
- **Docker Compose**: Multi-container orchestration
- **Trivy**: Vulnerability scanner
- **Dive**: Image layer analyzer
- **Hadolint**: Dockerfile linter

## References

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Node.js Docker Guide](https://nodejs.org/en/docs/guides/nodejs-docker-webapp/)
- [Docker Security](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
