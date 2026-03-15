---
name: docker-containerization
description: Docker containerization patterns for Python Flask applications with ML models, Tesseract OCR, and React frontends. Use when building, debugging, or deploying Docker containers for the Chuuk Dictionary application.
---

# Docker Containerization

## Overview

Docker containerization for the Chuuk Dictionary application including multi-stage builds, ML model packaging, OCR dependencies, and production deployment patterns.

## Docker Architecture

```text
chuuk/
├── Dockerfile               # Main application container
├── Dockerfile.ollama        # Ollama LLM container
├── ollama-entrypoint.sh     # Ollama startup script
├── docker-compose.yml       # Local development
└── .dockerignore
```

## Main Application Dockerfile

```dockerfile
# Multi-stage build for Chuuk Dictionary
# Stage 1: Build React frontend
FROM node:22-slim AS frontend-build

WORKDIR /app/frontend

# Install dependencies first (better caching)
COPY frontend/package*.json ./
RUN npm ci --no-audit

# Build frontend
COPY frontend/ ./
RUN npm run build

# Stage 2: Python application
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Tesseract OCR for image processing
    tesseract-ocr \
    tesseract-ocr-eng \
    # PDF processing
    poppler-utils \
    # Image libraries
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    # Build tools for some Python packages
    gcc \
    g++ \
    # Clean up
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY src/ ./src/
COPY config/ ./config/
COPY data/ ./data/
COPY scripts/ ./scripts/

# Copy ML models (large files)
COPY models/ ./models/

# Copy built frontend from Stage 1
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# Create necessary directories
RUN mkdir -p uploads logs output

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "300", "app:app"]
```

## Docker Ignore File

```dockerignore
# .dockerignore
# Git
.git
.gitignore
.github

# Python
__pycache__
*.py[cod]
*$py.class
.Python
*.so
.pytest_cache
.mypy_cache
*.egg-info
dist/
build/
eggs/
.eggs/

# Virtual environments
venv/
.venv/
ENV/

# Node
frontend/node_modules/
frontend/.vite/
frontend/dist/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Local development
.env
.env.local
*.log
logs/

# Test files
tests/
test_results/
htmlcov/
.coverage

# Documentation
docs/
*.md
!README.md

# Temporary files
*.tmp
*.temp
uploads/*
output/*
```

## Docker Compose for Development

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=development
      - COSMOS_CONNECTION_STRING=${COSMOS_CONNECTION_STRING}
      - FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
    volumes:
      # Mount code for hot reload (dev only)
      - ./app.py:/app/app.py:ro
      - ./src:/app/src:ro
      # Persist uploads
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    depends_on:
      - ollama
    networks:
      - chuuk-network

  ollama:
    build:
      context: .
      dockerfile: Dockerfile.ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama-models:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
    networks:
      - chuuk-network
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  # Local MongoDB for development
  mongodb:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongodb-data:/data/db
    environment:
      - MONGO_INITDB_DATABASE=chuuk_dictionary
    networks:
      - chuuk-network

networks:
  chuuk-network:
    driver: bridge

volumes:
  ollama-models:
  mongodb-data:
```

## Ollama Container

### Dockerfile.ollama

```dockerfile
# Dockerfile.ollama
FROM ollama/ollama:latest

# Copy custom model configurations
COPY ollama-modelfile/ /modelfiles/
COPY ollama-entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

### ollama-entrypoint.sh

```bash
#!/bin/bash
# Start Ollama server in background
ollama serve &

# Wait for server to be ready
sleep 10

# Load custom Chuukese model if exists
if [ -f "/modelfiles/chuukese-translator.modelfile" ]; then
    echo "Loading Chuukese translator model..."
    ollama create chuukese-translator -f /modelfiles/chuukese-translator.modelfile
fi

# Keep container running
wait
```

## Building and Running

### Build Commands

```bash
# Build main application
docker build -t chuuk-dictionary:latest .

# Build with specific tag
docker build -t chuuk-dictionary:v1.0.0 .

# Build without cache (fresh build)
docker build --no-cache -t chuuk-dictionary:latest .

# Build for specific platform
docker build --platform linux/amd64 -t chuuk-dictionary:latest .

# Build only frontend stage
docker build --target frontend-build -t chuuk-frontend:latest .
```

### Run Commands

```bash
# Run container
docker run -d \
  --name chuuk-app \
  -p 8000:8000 \
  -e COSMOS_CONNECTION_STRING="$COSMOS_CONNECTION_STRING" \
  -e FLASK_SECRET_KEY="$FLASK_SECRET_KEY" \
  chuuk-dictionary:latest

# Run with volume mounts
docker run -d \
  --name chuuk-app \
  -p 8000:8000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/logs:/app/logs \
  chuuk-dictionary:latest

# Run interactively for debugging
docker run -it --rm \
  -p 8000:8000 \
  chuuk-dictionary:latest /bin/bash

# Run with GPU support
docker run -d \
  --gpus all \
  --name chuuk-app \
  -p 8000:8000 \
  chuuk-dictionary:latest
```

### Docker Compose Commands

```bash
# Start all services
docker-compose up -d

# Start with build
docker-compose up -d --build

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild specific service
docker-compose build app
docker-compose up -d app
```

## Multi-Platform Builds

### Build for Azure Container Apps (AMD64)

```bash
# Enable buildx for multi-platform
docker buildx create --name chuuk-builder --use

# Build and push for AMD64
docker buildx build \
  --platform linux/amd64 \
  --push \
  -t myregistry.azurecr.io/chuuk-dictionary:latest \
  .
```

### Build for Multiple Architectures

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t myregistry.azurecr.io/chuuk-dictionary:latest \
  .
```

## Optimization Strategies

### Layer Caching

```dockerfile
# BAD: Invalidates cache on any code change
COPY . .
RUN pip install -r requirements.txt

# GOOD: Dependencies cached unless requirements change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

### Reduce Image Size

```dockerfile
# Use slim base images
FROM python:3.11-slim

# Install and clean in single RUN
RUN apt-get update && apt-get install -y --no-install-recommends \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*

# Use --no-cache-dir for pip
RUN pip install --no-cache-dir -r requirements.txt

# Remove build dependencies after use
RUN apt-get purge -y gcc g++ && apt-get autoremove -y
```

### Multi-Stage for ML Models

```dockerfile
# Stage 1: Download/prepare models
FROM python:3.11-slim AS model-prep

RUN pip install huggingface_hub
RUN python -c "from huggingface_hub import snapshot_download; \
    snapshot_download('Helsinki-NLP/opus-mt-mul-en', cache_dir='/models')"

# Stage 2: Final image
FROM python:3.11-slim

COPY --from=model-prep /models /app/models
```

## Debugging Containers

### Inspect Running Container

```bash
# View container logs
docker logs chuuk-app
docker logs -f chuuk-app  # Follow logs

# Execute command in running container
docker exec -it chuuk-app /bin/bash

# Check container stats
docker stats chuuk-app

# Inspect container configuration
docker inspect chuuk-app
```

### Debug Build Issues

```bash
# Build with verbose output
docker build --progress=plain -t chuuk-dictionary:latest .

# Build up to specific stage
docker build --target frontend-build -t debug:latest .

# Check image layers
docker history chuuk-dictionary:latest

# Analyze image size
docker images chuuk-dictionary:latest
```

### Health Checks

```bash
# Check container health status
docker inspect --format='{{.State.Health.Status}}' chuuk-app

# View health check logs
docker inspect --format='{{json .State.Health}}' chuuk-app | jq
```

## Security Best Practices

### Non-Root User

```dockerfile
# Create user before copying files
RUN useradd -m -u 1000 appuser

# Change ownership
COPY --chown=appuser:appuser . /app

# Switch to non-root user
USER appuser
```

### Secrets Management

```dockerfile
# NEVER put secrets in Dockerfile
# BAD
ENV API_KEY=my-secret-key

# GOOD: Use environment variables at runtime
docker run -e API_KEY="$API_KEY" myimage

# BETTER: Use Docker secrets or Azure Key Vault
```

### Scan for Vulnerabilities

```bash
# Scan image for vulnerabilities
docker scout cves chuuk-dictionary:latest

# Use trivy for scanning
trivy image chuuk-dictionary:latest
```

## Production Considerations

### Resource Limits

```yaml
# docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

### Logging Configuration

```dockerfile
# Configure logging driver
# In docker-compose.yml or docker run
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### Graceful Shutdown

```python
# In app.py
import signal
import sys

def signal_handler(sig, frame):
    print('Shutting down gracefully...')
    # Cleanup code here
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
```

## Common Issues and Solutions

### Issue: Large Image Size

```bash
# Check what's taking space
docker history --no-trunc chuuk-dictionary:latest

# Solutions:
# 1. Use multi-stage builds
# 2. Use slim base images
# 3. Clean up in same RUN layer
# 4. Use .dockerignore
```

### Issue: Slow Builds

```bash
# Solutions:
# 1. Order Dockerfile by change frequency
# 2. Use BuildKit for parallel builds
DOCKER_BUILDKIT=1 docker build .

# 3. Use --cache-from for CI/CD
docker build --cache-from=myregistry/app:latest .
```

### Issue: Container Won't Start

```bash
# Check logs
docker logs chuuk-app

# Run interactively
docker run -it chuuk-dictionary:latest /bin/bash

# Check if port is in use
lsof -i :8000
```

## Dependencies

Container includes:

- Python 3.11
- Node.js 22 (build stage)
- Tesseract OCR with English language pack
- Poppler PDF utilities
- OpenCV dependencies
- Gunicorn WSGI server
