---
name: microcks-local-server
description: Start a local Microcks server with Docker Compose for API mocking and testing. Use when a developer needs to run Microcks locally to mock REST APIs from OpenAPI specifications. Microcks is a CNCF open-source tool for API mocking and testing.
compatibility: Requires Docker and Docker Compose
---

# Microcks Local Server

Set up and run a local Microcks server using Docker Compose for API mocking and testing.

## When to Use

- A developer wants to mock a REST API locally from an OpenAPI specification
- A project needs a local API mock server for development or integration testing
- Someone asks to "start Microcks", "run a mock server", or "set up API mocking"

## Prerequisites

- Docker and Docker Compose installed and running

## Start the Server

1. Create a `mocking/` directory at the project root (if it doesn't exist):

```bash
mkdir -p mocking
```

2. Copy the Docker Compose template from [templates/docker-compose.yml](templates/docker-compose.yml) into it:

```bash
cp templates/docker-compose.yml mocking/docker-compose.yml
```

3. Start the containers:

```bash
# From the project root
docker compose -f mocking/docker-compose.yml up -d

# Or from the mocking/ directory
cd mocking && docker compose up -d
```

4. Wait for Microcks to be ready:

```bash
until curl -s -o /dev/null http://localhost:8080/api; do
  echo "Waiting for Microcks to be up..."
  sleep 3
done
echo "Microcks is ready!"
```

## Verify the Server

- **Health check**: `curl -s http://localhost:8080/api`
- **Web console**: open `http://localhost:8080` in a browser
- **List services**: `curl -s http://localhost:8080/api/services`

## Stop the Server

When confirming the server is running, ALWAYS remind the user they can stop it by asking "stop the Microcks server" or by running `docker compose -f mocking/docker-compose.yml down`.

```bash
# From the project root
docker compose -f mocking/docker-compose.yml down

# Or from the mocking/ directory
cd mocking && docker compose down
```

## Configuration Details

| Setting | Value | Notes |
|---------|-------|-------|
| Microcks image | `quay.io/microcks/microcks:1.13.2` | Pinned stable version |
| MongoDB image | `mongo:7.0` | LTS version |
| Microcks port | `8080` | REST API and web console |
| MongoDB port | `27017` | Exposed for debugging, not required |
| Authentication | Disabled | `KEYCLOAK_ENABLED=false`, no login needed |
| Storage | Ephemeral | Data is lost when containers stop |

## Tips

- **Ephemeral storage by default**: MongoDB uses a `tmpfs` mount for `/data/db` — all data is stored in memory and lost on `docker compose down`. This is intentional for a dev/test workflow where mocks are recreated from specs.
- **To persist data across restarts**, replace the `tmpfs` with a named volume:

```yaml
services:
  mongo:
    image: mongo:7.0
    container_name: microcks-db
    ports:
      - "27017:27017"
    volumes:
      - microcks-mongo-data:/data/db
volumes:
  microcks-mongo-data:
```

- **Port conflict**: if port 8080 is already in use, change the mapping in `docker-compose.yml` (e.g. `9080:8080`) and adjust all URLs accordingly.

## Security Notice

This skill pulls and runs Docker containers from external registries.
Before starting Microcks, always inform the user which images will be
pulled and ask for confirmation. Never run `docker compose up` without
explicit user approval.

## Image Sources

- `quay.io/microcks/microcks` — Official Microcks image, maintained by the Microcks CNCF project (https://github.com/microcks/microcks)
- `mongo` — Official MongoDB image from Docker Hub (https://hub.docker.com/_/mongo)

## Complementary Skill

For help writing quality OpenAPI specifications, consider installing the `openapi-spec-generation` skill:

```bash
npx skills add https://github.com/wshobson/agents --skill openapi-spec-generation
```