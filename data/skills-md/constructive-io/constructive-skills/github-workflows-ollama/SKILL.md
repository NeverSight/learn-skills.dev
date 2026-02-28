---
name: github-workflows-ollama
description: Configure GitHub Actions workflows for Ollama and pgvector testing. Use when asked to "set up CI for RAG", "configure Ollama in CI", "test embeddings in GitHub Actions", or when building CI/CD pipelines for AI applications with pgvector.
compatibility: GitHub Actions, Docker, PostgreSQL with pgvector, Ollama
metadata:
  author: constructive-io
  version: "1.0.0"
---

# GitHub Workflows for Ollama and pgvector

Configure GitHub Actions workflows for testing RAG pipelines, vector embeddings, and Ollama-based AI applications.

## When to Apply

Use this skill when:
- Setting up CI/CD for RAG applications
- Testing pgvector and embedding functionality in CI
- Configuring Ollama service containers
- Running integration tests that need LLM inference
- Building pipelines for AI-powered applications

## Complete Workflow Template

```yaml
name: CI tests
on:
  pull_request:
    branches:
      - main
  push:
    branches:
      - main
  workflow_dispatch:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}-tests
  cancel-in-progress: true

env:
  PGPM_VERSION: '2.7.9'

jobs:
  test:
    runs-on: ubuntu-latest
    continue-on-error: true
    strategy:
      fail-fast: false
      matrix:
        package:
          - my-rag-package

    env:
      PGHOST: localhost
      PGPORT: 5432
      PGUSER: postgres
      PGPASSWORD: password
      OLLAMA_HOST: http://localhost:11434

    services:
      pg_db:
        image: pyramation/postgres:17
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      ollama:
        image: ollama/ollama:latest
        ports:
          - 11434:11434

    steps:
      - name: Configure Git (for tests)
        run: |
          git config --global user.name "CI Test User"
          git config --global user.email "ci@example.com"

      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 10

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install

      - name: Cache pgpm CLI
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: pgpm-${{ runner.os }}-${{ env.PGPM_VERSION }}

      - name: Install pgpm CLI globally
        run: npm install -g pgpm@${{ env.PGPM_VERSION }}

      - name: Build
        run: pnpm -r build

      - name: Seed pg and app_user
        run: |
          pgpm admin-users bootstrap --yes
          pgpm admin-users add --test --yes

      - name: Wait for Ollama and pull models
        run: |
          echo "Waiting for Ollama to be ready..."
          for i in $(seq 1 30); do
            if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
              echo "Ollama is ready!"
              break
            fi
            echo "Waiting for Ollama... ($i/30)"
            sleep 2
          done
          echo "Pulling nomic-embed-text model (for embeddings)..."
          curl -s -X POST http://localhost:11434/api/pull -d '{"name": "nomic-embed-text"}'
          echo ""
          echo "Pulling mistral model (for RAG response generation)..."
          curl -s -X POST http://localhost:11434/api/pull -d '{"name": "mistral"}'

      - name: Test ${{ matrix.package }}
        run: cd ./packages/${{ matrix.package }} && pnpm test
```

## Service Containers

### PostgreSQL with pgvector

Use the Constructive PostgreSQL image with pgvector and other extensions:

```yaml
services:
  pg_db:
    image: pyramation/postgres:17
    env:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
    ports:
      - 5432:5432
```

For projects requiring additional extensions:

```yaml
services:
  pg_db:
    image: ghcr.io/constructive-io/docker/postgres-plus:17
    env:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
    ports:
      - 5432:5432
```

Available images:
- `pyramation/postgres:17` - PostgreSQL 17 with pgvector (recommended)
- `ghcr.io/constructive-io/docker/postgres-plus:17` - PostgreSQL 17 with pgvector and additional extensions

### Ollama Service

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - 11434:11434
```

Note: Ollama doesn't have a built-in health check, so we wait for it in a step.

## Environment Variables

```yaml
env:
  # PostgreSQL connection
  PGHOST: localhost
  PGPORT: 5432
  PGUSER: postgres
  PGPASSWORD: password

  # Ollama connection
  OLLAMA_HOST: http://localhost:11434
```

## Waiting for Ollama

Ollama takes time to start. Use this pattern to wait:

```yaml
- name: Wait for Ollama and pull models
  run: |
    echo "Waiting for Ollama to be ready..."
    for i in $(seq 1 30); do
      if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "Ollama is ready!"
        break
      fi
      echo "Waiting for Ollama... ($i/30)"
      sleep 2
    done
```

## Pulling Models

Models must be pulled before tests run:

```yaml
- name: Pull embedding model
  run: |
    curl -s -X POST http://localhost:11434/api/pull \
      -d '{"name": "nomic-embed-text"}'

- name: Pull generation model
  run: |
    curl -s -X POST http://localhost:11434/api/pull \
      -d '{"name": "mistral"}'
```

### Model Pull Times

| Model | Size | Approximate Pull Time |
|-------|------|----------------------|
| `nomic-embed-text` | ~275MB | 30-60s |
| `mistral` | ~4GB | 2-5 min |
| `llama2` | ~4GB | 2-5 min |
| `all-minilm` | ~45MB | 10-20s |

Consider using smaller models in CI for faster runs.

## Test Timeout Configuration

LLM operations can be slow. Configure Jest timeout:

```typescript
// In test file
jest.setTimeout(300000); // 5 minutes

// Or in jest.config.js
module.exports = {
  testTimeout: 300000,
};
```

## Caching Strategies

### Cache pnpm dependencies

```yaml
- name: Setup pnpm
  uses: pnpm/action-setup@v2
  with:
    version: 10

- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'pnpm'
```

### Cache pgpm CLI

```yaml
env:
  PGPM_VERSION: '2.7.9'

steps:
  - name: Cache pgpm CLI
    uses: actions/cache@v4
    with:
      path: ~/.npm
      key: pgpm-${{ runner.os }}-${{ env.PGPM_VERSION }}

  - name: Install pgpm CLI globally
    run: npm install -g pgpm@${{ env.PGPM_VERSION }}
```

## Matrix Testing

Test multiple packages in parallel:

```yaml
strategy:
  fail-fast: false
  matrix:
    package:
      - packages/embeddings
      - packages/rag-service
      - packages/vector-search

steps:
  - name: Test ${{ matrix.package }}
    run: cd ./${{ matrix.package }} && pnpm test
```

## Minimal Workflow (Embeddings Only)

For projects that only need embeddings (no LLM generation):

```yaml
name: Embedding Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    env:
      PGHOST: localhost
      PGPORT: 5432
      PGUSER: postgres
      PGPASSWORD: password
      OLLAMA_HOST: http://localhost:11434

    services:
      postgres:
        image: pyramation/postgres:17
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Ollama
        run: curl -fsSL https://ollama.com/install.sh | sh

      - name: Start Ollama and pull model
        run: |
          ollama serve &
          sleep 5
          ollama pull nomic-embed-text

      - name: Install dependencies
        run: npm install

      - name: Run tests
        run: npm test
```

## Debugging Failed Tests

### View Ollama logs

```yaml
- name: Debug Ollama
  if: failure()
  run: |
    echo "Checking Ollama status..."
    curl -s http://localhost:11434/api/tags || echo "Ollama not responding"
```

### Check PostgreSQL

```yaml
- name: Debug PostgreSQL
  if: failure()
  run: |
    psql -h localhost -U postgres -c "SELECT version();"
    psql -h localhost -U postgres -c "SELECT * FROM pg_extension WHERE extname = 'vector';"
```

## Best Practices

1. **Use `fail-fast: false`** - Let all tests complete even if some fail
2. **Set generous timeouts** - LLM operations are slow
3. **Pull models early** - Do it before running tests
4. **Use smaller models in CI** - `all-minilm` instead of `nomic-embed-text` for speed
5. **Cache dependencies** - pnpm and pgpm caching speeds up runs
6. **Health checks** - Always use health checks for PostgreSQL
7. **Wait for Ollama** - It doesn't have built-in health checks

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Ollama not responding | Increase wait time, check service logs |
| Model pull timeout | Use smaller model or increase timeout |
| pgvector not found | Ensure using pgvector-enabled image |
| Tests timeout | Increase Jest timeout, use streaming |
| Out of memory | Use smaller models or reduce parallelism |

## References

- Related skill: `github-workflows-pgpm` for general PGPM CI/CD
- Related skill: `pgpm-testing` for database testing
- Related skill: `rag-pipeline` for RAG implementation
- Related skill: `ollama-integration` for Ollama client
- [Ollama Docker documentation](https://ollama.com/blog/ollama-is-now-available-as-an-official-docker-image)
