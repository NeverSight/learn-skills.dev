---
name: docker-compose
description: Docker Compose management for orchestrating MCP servers and multi-container applications. Use when deploying MCP servers, managing container lifecycles, or configuring service dependencies.
---

# Docker Compose Skill

Docker Compose orchestration skill for managing multi-container applications, with specific focus on MCP server deployment.

## When to Use This Skill

- Deploying MCP servers as Docker containers
- Managing multi-container application stacks
- Orchestrating services with dependencies
- Persisting data with volumes
- Enabling container-to-container communication

## Core Commands

### Lifecycle Management

**Start all services**:
```bash
docker compose up --detach
```

**Start single service**:
```bash
docker compose up <service-name> --detach
```

**Stop all services** (without removing):
```bash
docker compose stop
```

**Stop and remove all services**:
```bash
docker compose down
```

**Restart services**:
```bash
docker compose restart
docker compose restart <service-name>  # Single service
```

### Image Management

**Pull images** (for services using `image:`):
```bash
docker compose pull
```

**Build images** (for services using `build:`):
```bash
docker compose build
docker compose build --no-cache  # Force rebuild
```

### Monitoring

**View running services**:
```bash
docker compose ps
```

**View logs**:
```bash
docker compose logs
docker compose logs <service-name>  # Single service
docker compose logs -f              # Follow logs (tail)
```

**Access container shell**:
```bash
docker compose exec --interactive --tty <service-name> sh
```

### Cleanup

**Remove stopped containers**:
```bash
docker compose rm
```

**Full cleanup** (containers, networks, volumes):
```bash
docker compose down --volumes
```

## compose.yaml Structure

### MCP Server Example

```yaml
version: '3'

services:
  playwright:
    image: mcr.microsoft.com/playwright/mcp:latest
    container_name: playwright-mcp
    stdin_open: true
    tty: true
    restart: unless-stopped
    volumes:
      - ./data:/data
    networks:
      - mcp-network
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G

networks:
  mcp-network:
    driver: bridge

volumes:
  playwright-data:
```

### Key Configuration Options

**Service Definition**:
- `image:` - Use pre-built image from registry
- `build:` - Build from Dockerfile
- `container_name:` - Custom container name
- `restart:` - Restart policy (`always`, `unless-stopped`, `on-failure`)
- `stdin_open: true` + `tty: true` - Required for MCP stdio protocol
- `ports:` - Publish ports (format: `"host:container"`)
- `environment:` - Environment variables
- `volumes:` - Mount volumes for persistence
- `networks:` - Connect to custom networks
- `depends_on:` - Service dependencies

**Health Checks**:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

**Resource Limits**:
```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 1G
    reservations:
      cpus: '0.5'
      memory: 512M
```

## MCP Server-Specific Patterns

### Stdio-Based MCP Servers

MCP servers use stdin/stdout communication:
```yaml
services:
  mcp-server:
    image: your-mcp-image:latest
    stdin_open: true  # REQUIRED for MCP
    tty: true         # REQUIRED for MCP
    # No ports needed - uses stdio
```

### Volume Persistence

```yaml
services:
  filesystem-mcp:
    image: mcp/filesystem:latest
    stdin_open: true
    tty: true
    volumes:
      - ./workspace:/workspace:ro  # Read-only access
      - mcp-data:/data             # Named volume

volumes:
  mcp-data:  # Docker manages location
```

### Service Dependencies

```yaml
services:
  app:
    image: app:latest
    depends_on:
      database:
        condition: service_healthy  # Wait for health check

  database:
    image: postgres:16
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "user"]
      interval: 2s
      timeout: 2s
      retries: 3
```

## Common Workflows

### Initial Setup

```bash
# Create compose.yaml
cd mcp-servers/
cat > compose.yaml << 'EOF'
version: '3'
services:
  my-mcp:
    image: mcp-image:latest
    stdin_open: true
    tty: true
EOF

# Pull images and start
docker compose pull
docker compose up -d
```

### Update Services

```bash
# Pull latest images
docker compose pull

# Restart with new images
docker compose up -d
```

### Debug Container Issues

```bash
# Check service status
docker compose ps

# View logs
docker compose logs playwright

# Access container shell
docker compose exec -it playwright sh

# Check resource usage
docker stats $(docker compose ps -q)
```

### Clean Shutdown

```bash
# Stop gracefully
docker compose stop

# Remove containers (keep volumes)
docker compose down

# Full cleanup including volumes
docker compose down --volumes
```

## Best Practices

1. **Always use `--detach` flag** for background processes
2. **Pin image versions** instead of `:latest` for production
3. **Use named volumes** for data persistence
4. **Set resource limits** to prevent resource exhaustion
5. **Include health checks** for services with dependencies
6. **Use restart policies** for automatic recovery
7. **Keep compose.yaml in version control**
8. **Document environment variables** and their defaults

## Troubleshooting

**Service won't start**:
```bash
docker compose logs <service-name>
docker compose ps  # Check exit codes
```

**Port conflicts**:
```bash
# Change port mapping in compose.yaml
ports:
  - "8081:8080"  # Use different host port
```

**Volume permission issues**:
```bash
# Add user mapping
user: "1000:1000"
```

**Container can't reach other services**:
```bash
# Ensure both services on same network
networks:
  - shared-network
```

## References

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Compose File Specification](https://docs.docker.com/compose/compose-file/)
- [DevOps Cycle Cheatsheet](https://devopscycle.com/blog/the-ultimate-docker-compose-cheat-sheet)