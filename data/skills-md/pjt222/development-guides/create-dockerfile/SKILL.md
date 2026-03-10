---
name: create-dockerfile
description: >
  Create general-purpose Dockerfiles for Node.js, Python, Go, Rust, and Java
  projects. Covers base image selection, dependency installation, user
  permissions, COPY patterns, ENTRYPOINT vs CMD, and .dockerignore. Use when
  containerizing an application for the first time, creating a consistent
  build/runtime environment, preparing an app for cloud deployment or Docker
  Compose, or when no existing Dockerfile is present in the project.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: containerization
  complexity: basic
  language: Docker
  tags: docker, dockerfile, node, python, go, rust, java, container
---

# Create Dockerfile

Write a production-ready Dockerfile for general-purpose application projects.

## When to Use

- Containerizing a Node.js, Python, Go, Rust, or Java application
- Creating a consistent build/runtime environment
- Preparing an application for cloud deployment or Docker Compose
- No existing Dockerfile in the project

## Inputs

- **Required**: Project language and entry point (e.g., `npm start`, `python app.py`)
- **Required**: Dependency manifest (package.json, requirements.txt, go.mod, Cargo.toml, pom.xml)
- **Optional**: Target environment (development or production)
- **Optional**: Exposed ports

## Procedure

### Step 1: Choose Base Image

| Language | Dev Image | Prod Image | Size |
|----------|-----------|------------|------|
| Node.js | `node:22-bookworm` | `node:22-bookworm-slim` | ~200MB |
| Python | `python:3.12-bookworm` | `python:3.12-slim-bookworm` | ~150MB |
| Go | `golang:1.23-bookworm` | `gcr.io/distroless/static` | ~2MB |
| Rust | `rust:1.82-bookworm` | `debian:bookworm-slim` | ~80MB |
| Java | `eclipse-temurin:21-jdk` | `eclipse-temurin:21-jre` | ~200MB |

**Expected:** Select the slim/distroless variant for production images.

### Step 2: Write Dockerfile (by language)

#### Node.js

```dockerfile
FROM node:22-bookworm-slim

RUN groupadd -r appuser && useradd -r -g appuser -m appuser

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --omit=dev

COPY . .

USER appuser
EXPOSE 3000
CMD ["node", "src/index.js"]
```

#### Python

```dockerfile
FROM python:3.12-slim-bookworm

RUN groupadd -r appuser && useradd -r -g appuser -m appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER appuser
EXPOSE 8000
CMD ["python", "app.py"]
```

#### Go

```dockerfile
FROM golang:1.23-bookworm AS builder

WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app/server ./cmd/server

FROM gcr.io/distroless/static
COPY --from=builder /app/server /server
EXPOSE 8080
ENTRYPOINT ["/server"]
```

#### Rust

```dockerfile
FROM rust:1.82-bookworm AS builder

WORKDIR /src
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs && cargo build --release && rm -rf src

COPY . .
RUN touch src/main.rs && cargo build --release

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src/target/release/myapp /usr/local/bin/myapp
EXPOSE 8080
ENTRYPOINT ["myapp"]
```

#### Java (Maven)

```dockerfile
FROM eclipse-temurin:21-jdk AS builder

WORKDIR /src
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src ./src
RUN mvn package -DskipTests

FROM eclipse-temurin:21-jre
COPY --from=builder /src/target/*.jar /app/app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

**Expected:** `docker build -t myapp .` completes without errors.

**On failure:** Check base image availability and dependency installation commands.

### Step 3: ENTRYPOINT vs CMD

| Directive | Purpose | Override |
|-----------|---------|----------|
| `ENTRYPOINT` | Fixed executable | Override with `--entrypoint` |
| `CMD` | Default arguments | Override with trailing args |
| Both | `ENTRYPOINT` + default args via `CMD` | Args override CMD only |

Use `ENTRYPOINT` for compiled binaries with a single purpose. Use `CMD` for interpreted languages where you might want `docker run myapp bash`.

### Step 4: Create .dockerignore

```
.git
.gitignore
node_modules
__pycache__
*.pyc
target/
.env
.env.*
*.md
!README.md
.vscode
.idea
Dockerfile
docker-compose*.yml
```

**Expected:** Build context excludes development artifacts.

### Step 5: Add Non-Root User

Always run as non-root in production:

```dockerfile
RUN groupadd -r appuser && useradd -r -g appuser -m appuser
USER appuser
```

For distroless images, use the built-in nonroot user:

```dockerfile
FROM gcr.io/distroless/static:nonroot
USER nonroot
```

### Step 6: Build and Verify

```bash
docker build -t myapp:latest .
docker run --rm myapp:latest
docker image inspect myapp:latest --format '{{.Size}}'
```

**Expected:** Container starts, responds on the expected port, runs as non-root.

**On failure:** Check logs with `docker logs`. Verify WORKDIR, COPY paths, and exposed ports.

## Validation

- [ ] `docker build` completes without errors
- [ ] Container starts and application responds
- [ ] `.dockerignore` excludes unnecessary files
- [ ] Application runs as non-root user
- [ ] Dependencies are copied before source code (cache efficiency)
- [ ] No secrets or `.env` files baked into the image

## Common Pitfalls

- **COPY before dependency install**: Invalidates the dependency cache on every code change. Always copy the manifest file first.
- **Running as root**: Default Docker user is root. Always add a non-root user for production.
- **Missing .dockerignore**: Sending `node_modules` or `.git` into the build context wastes time and disk.
- **Using `latest` tag for base images**: Pin to specific versions (e.g., `node:22.11.0`) for reproducibility.
- **Forgetting `--no-cache-dir`**: Python `pip` caches packages by default, bloating the image.
- **ADD vs COPY**: Use `COPY` unless you need URL download or tar extraction (`ADD` auto-extracts).

## Related Skills

- `create-r-dockerfile` - R-specific Dockerfile using rocker images
- `create-multistage-dockerfile` - multi-stage patterns for minimal production images
- `optimize-docker-build-cache` - advanced caching strategies
- `setup-compose-stack` - orchestrate the containerized app with other services
