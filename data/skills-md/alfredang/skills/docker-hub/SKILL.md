---
name: Docker Hub
description: Build and push Docker images to Docker Hub (tertiaryinfotech). Auto-generates Dockerfile if missing by detecting project type. Use when pushing Docker images, running "push to docker hub", "docker push", or any Docker Hub deployment task.
---

# Docker Hub

Build and push Docker images to `tertiaryinfotech` on Docker Hub. Auto-generates a Dockerfile if one doesn't exist by detecting the project type.

## Command
`/docker-hub` or `docker-hub`

## Navigate
Docker & Deployment

## Keywords
docker hub, docker push, docker build, docker image, dockerfile, container, containerize, push image, docker deploy, docker hub push, tertiaryinfotech, build image, docker registry

## Description
Build and push Docker images to Docker Hub under the `tertiaryinfotech` organization. Automatically detects the project type, generates a Dockerfile if missing, builds the image, and pushes it to https://hub.docker.com/repositories/tertiaryinfotech.

## Execution
This skill runs using **Claude Code with subscription plan**. Do NOT use pay-as-you-go API keys. All AI operations should be executed through the Claude Code CLI environment with an active subscription.

## Response
I'll help you build and push your Docker image to Docker Hub!

The workflow includes:

| Step | Description |
|------|-------------|
| **Pre-flight** | Verify Docker CLI, daemon, and Docker Hub authentication |
| **Dockerfile** | Detect project type and generate Dockerfile if missing |
| **Build** | Build image tagged as `tertiaryinfotech/<project>:latest` |
| **Push** | Push image to Docker Hub |
| **Verify** | Confirm push and print Docker Hub URL |

## Instructions

When executing `/docker-hub`, follow this workflow:

### Phase 1: Pre-flight Checks

#### 1.1 Verify Docker CLI
```bash
docker --version
```
If Docker is not installed, inform the user and stop. Provide installation link: https://docs.docker.com/get-docker/

#### 1.2 Verify Docker Daemon
```bash
docker info > /dev/null 2>&1
```
If the daemon is not running, inform the user:
```
Docker daemon is not running. Please start Docker Desktop or the Docker service.
```

#### 1.3 Verify Docker Hub Authentication
```bash
docker login --username tertiaryinfotech
```
If not logged in, prompt the user to authenticate. The push target is always the `tertiaryinfotech` account.

#### 1.4 Determine Image Name
```bash
PROJECT_NAME=$(basename "$(pwd)")
IMAGE_NAME="tertiaryinfotech/$PROJECT_NAME"
echo "Image will be pushed as: $IMAGE_NAME:latest"
```

The image name is always `tertiaryinfotech/<folder-name>`. The tag defaults to `latest` unless the user specifies otherwise.

### Phase 2: Dockerfile Detection & Generation

#### 2.1 Check for Existing Dockerfile
```bash
ls Dockerfile 2>/dev/null
```

**If Dockerfile exists:** Skip to Phase 3.

**If Dockerfile does NOT exist:** Detect the project type and generate an appropriate Dockerfile.

#### 2.2 Detect Project Type

Check for these files in order to determine the project type:

| File | Project Type |
|------|-------------|
| `package.json` | Node.js (check for Next.js, Vite, Express, etc.) |
| `requirements.txt` | Python (pip) |
| `pyproject.toml` | Python (uv/poetry) |
| `Pipfile` | Python (pipenv) |
| `go.mod` | Go |
| `pom.xml` | Java (Maven) |
| `build.gradle` | Java (Gradle) |
| `Cargo.toml` | Rust |
| `Gemfile` | Ruby |
| `index.html` (no framework files) | Static site |

#### 2.3 Generate Dockerfile

Based on the detected project type, generate a production-ready Dockerfile following these best practices:
- Use official base images with specific version tags (not `latest`)
- Multi-stage builds where applicable to minimize image size
- Non-root user for security
- Copy dependency files first, install, then copy source (layer caching)
- Use `.dockerignore` to exclude unnecessary files

**Node.js Example (Express/generic):**
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

FROM node:20-alpine
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=builder /app .
USER appuser
EXPOSE 3000
CMD ["node", "index.js"]
```

**Node.js Example (Next.js):**
```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
USER appuser
EXPOSE 3000
CMD ["npm", "start"]
```

**Python Example (pip):**
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
RUN useradd -r -s /bin/false appuser
COPY --from=builder /install /usr/local
COPY . .
USER appuser
EXPOSE 8000
CMD ["python", "main.py"]
```

**Python Example (uv/pyproject.toml):**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev
COPY . .
RUN useradd -r -s /bin/false appuser
USER appuser
EXPOSE 8000
CMD ["uv", "run", "python", "main.py"]
```

**Go Example:**
```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/main .

FROM alpine:3.19
WORKDIR /app
RUN adduser -D -s /bin/sh appuser
COPY --from=builder /app/main .
USER appuser
EXPOSE 8080
CMD ["./main"]
```

**Static Site Example (nginx):**
```dockerfile
FROM nginx:alpine
COPY . /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Rust Example:**
```dockerfile
FROM rust:1.77-slim AS builder
WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src
RUN cargo build --release

FROM debian:bookworm-slim
WORKDIR /app
RUN useradd -r -s /bin/false appuser
COPY --from=builder /app/target/release/* .
USER appuser
EXPOSE 8080
CMD ["./app"]
```

**Java (Maven) Example:**
```dockerfile
FROM maven:3.9-eclipse-temurin-21 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

FROM eclipse-temurin:21-jre
WORKDIR /app
RUN useradd -r -s /bin/false appuser
COPY --from=builder /app/target/*.jar app.jar
USER appuser
EXPOSE 8080
CMD ["java", "-jar", "app.jar"]
```

**Ruby Example:**
```dockerfile
FROM ruby:3.3-slim AS builder
WORKDIR /app
COPY Gemfile Gemfile.lock ./
RUN bundle install --without development test

FROM ruby:3.3-slim
WORKDIR /app
RUN useradd -r -s /bin/false appuser
COPY --from=builder /usr/local/bundle /usr/local/bundle
COPY . .
USER appuser
EXPOSE 3000
CMD ["ruby", "app.rb"]
```

Adapt the generated Dockerfile to match the specific project (e.g., check `package.json` for the `start` script, detect the main entry file, check for framework-specific build commands).

#### 2.4 Generate .dockerignore (if missing)

If no `.dockerignore` exists, generate one appropriate for the project type:

```
node_modules
.git
.gitignore
.env
.env.*
*.md
.DS_Store
.vscode
.idea
__pycache__
*.pyc
.pytest_cache
target
dist
build
.next
```

### Phase 3: Build Image

```bash
PROJECT_NAME=$(basename "$(pwd)")
docker build -t tertiaryinfotech/$PROJECT_NAME:latest .
```

If the build fails:
1. Read the error output carefully
2. Fix the Dockerfile if the issue is in the generated Dockerfile
3. If the issue is in the user's code, report the error and suggest fixes
4. Retry the build after fixing

### Phase 4: Push to Docker Hub

```bash
PROJECT_NAME=$(basename "$(pwd)")
docker push tertiaryinfotech/$PROJECT_NAME:latest
```

**Always push to `tertiaryinfotech`.** This is hardcoded and should never be changed.

If push fails due to authentication:
```bash
docker login --username tertiaryinfotech
```
Then retry the push.

### Phase 5: Verify

1. Confirm the push succeeded from the command output
2. Print the Docker Hub URL:
```bash
PROJECT_NAME=$(basename "$(pwd)")
echo "Image pushed successfully!"
echo "Docker Hub: https://hub.docker.com/r/tertiaryinfotech/$PROJECT_NAME"
echo "Pull command: docker pull tertiaryinfotech/$PROJECT_NAME:latest"
```

## Capabilities

- Detect project type automatically (Node.js, Python, Go, Java, Rust, Ruby, static sites)
- Generate production-ready Dockerfiles with multi-stage builds
- Generate `.dockerignore` for clean builds
- Build and tag images for `tertiaryinfotech` organization
- Push images to Docker Hub
- Support for custom tags (defaults to `latest`)
- Non-root user in generated Dockerfiles for security
- Layer caching optimization in generated Dockerfiles

## Notes

- All images are pushed to the `tertiaryinfotech` Docker Hub account
- Image name is derived from the current folder name: `tertiaryinfotech/<folder-name>`
- Default tag is `latest` — user can specify a custom tag if needed
- Docker Desktop or Docker daemon must be running before using this skill
- If `DOCKER_USERNAME` or `DOCKER_PASSWORD` environment variables are set, they can be used for non-interactive login
