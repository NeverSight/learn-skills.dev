---
name: test-in-docker
description: Use Docker to execute and test shell commands, scripts, code, builds, installations, CLI tools, and other operations instead of running them directly on the host machine. If Docker is unavailable, skip testing entirely. Never fall back to host execution.
---

# Test in Docker

## Purpose

Use Docker as a temporary testing environment instead of executing test commands directly on the user's computer.

## Rules

1. Before testing, check whether Docker is installed and running.
2. If Docker is unavailable, skip testing. Never execute the test command on the host.
3. Choose an appropriate Docker image based on the command and required runtime.
4. Prefer disposable containers using `docker run --rm`.
5. Execute the requested command inside the container.
6. Mount project files only when necessary.
7. Use read-only mounts whenever possible.
8. If tests need to modify project files, use a temporary copy instead of modifying the original project.
9. Enable network access only when required.
10. Never expose sensitive host files, credentials, or the Docker socket.
11. Check the actual exit code and output.
12. Clean up temporary resources created during testing.
13. Report whether the test passed, failed, or was skipped.

## Examples

### 1. Test a shell command

```bash
docker run --rm alpine:latest sh -c 'echo "Hello from Docker"'
```

### 2. Test Node.js

```bash
docker run --rm node:24-alpine node --version
```

### 3. Test Python

```bash
docker run --rm python:3-alpine python --version
```

### 4. Test PHP

```bash
docker run --rm php:8.3-cli-alpine php --version
```

### 5. Test a project

Mount the project read-only:

```bash
docker run --rm \
  -v "$PWD:/workspace:ro" \
  -w /workspace \
  node:24-alpine \
  npm run lint
```

If the test needs to modify files, copy the project into a disposable container workspace and run the test there.

### 6. Test a shell script

```bash
docker run --rm \
  -v "$PWD:/workspace:ro" \
  -w /workspace \
  alpine:latest \
  sh ./test.sh
```

Use an image containing Bash if the script requires Bash.

### 7. Test with additional dependencies

```bash
docker run --rm node:24-alpine sh -c '
  apk add --no-cache curl bash
  node --version
  curl --version
  bash --version
'
```

## Docker availability

Check:

```bash
docker --version
docker info
```

Both must succeed before testing.

If Docker is unavailable:

- Skip testing.
- Do not install Docker automatically.
- Do not execute commands on the host.
- Continue other work that does not require command execution.
- Inform the user that testing was skipped.

## Final principle

**Test inside Docker. Never test directly on the host.**

Docker unavailable = Skip testing.
