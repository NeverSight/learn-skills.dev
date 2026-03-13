---
name: docker-build
description: Build Docker images with proper tagging, cache busting, and build tracking. Prevents stale image issues.
disable-model-invocation: true
---

# Docker Build with Tracking

Build a Docker image with proper tagging and tracking: $ARGUMENTS

## Process
1. **Determine the image tag** - Use git SHA or timestamp, NEVER use `:latest` alone
   ```bash
   GIT_SHA=$(git rev-parse --short HEAD)
   TIMESTAMP=$(date +%Y%m%d-%H%M%S)
   TAG="${GIT_SHA}-${TIMESTAMP}"
   ```

2. **Build with cache busting when needed**
   - For production builds: `docker build --no-cache --pull -t <registry>/<image>:${TAG} .`
   - For dev builds: `docker build -t <registry>/<image>:${TAG} .`
   - Always also tag as `:<branch>-latest` for convenience

3. **Verify the build**
   ```bash
   docker images | grep <image>
   docker inspect <registry>/<image>:${TAG} | jq '.[0].Created'
   ```

4. **Push to registry**
   ```bash
   docker push <registry>/<image>:${TAG}
   docker push <registry>/<image>:<branch>-latest
   ```

5. **Verify in registry**
   ```bash
   # For ACR:
   az acr repository show-tags --name <registry> --repository <image> --orderby time_desc --top 5
   # For Docker Hub:
   docker manifest inspect <registry>/<image>:${TAG}
   ```

## Anti-Patterns (DO NOT)
- Never build with just `:latest` tag
- Never skip pushing after building
- Never deploy without verifying the image exists in the registry
- Never use `imagePullPolicy: IfNotPresent` with mutable tags
