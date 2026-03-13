---
name: setup-smello
description: Explore a Python codebase and propose a plan to integrate Smello traffic capture (HTTP and gRPC). Use when the user wants to add Smello to their project, set up request monitoring, or capture outgoing API calls for debugging.
argument-hint: "[server_url]"
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(uv *), Bash(cat *), Bash(ls *), Bash(python *), Bash(docker *)
---

# Setup Smello

You are helping the user integrate [Smello](https://github.com/smelloscope/smello) into their Python project. Smello captures outgoing HTTP requests (via `requests` and `httpx`) and gRPC calls (via `grpc`) and displays them in a local web dashboard at http://localhost:5110. Google Cloud libraries (BigQuery, Firestore, Pub/Sub, Analytics Data API, Vertex AI, etc.) use gRPC under the hood and are captured automatically.

**Your job is to explore the codebase, then present a plan. Do NOT make any changes until the user approves.**

## Step 1: Explore the codebase

Investigate the project to understand:

1. **Package manager**: Is the project using `pip` + `requirements.txt`, `pip` + `pyproject.toml`, `uv`, `poetry`, `pipenv`, or something else?
2. **HTTP/gRPC libraries**: Does the project use `requests`, `httpx`, `grpc`, or Google Cloud client libraries? Search for `import requests`, `import httpx`, `from requests`, `from httpx`, `import grpc`, `from google.cloud`, `from google.analytics`.
3. **Application entrypoint**: Find where the app starts. Look for:
   - `if __name__ == "__main__":` blocks
   - Framework-specific entrypoints: Django (`manage.py`, `wsgi.py`, `asgi.py`), Flask (`app = Flask(...)`, `create_app()`), FastAPI (`app = FastAPI()`), etc.
   - CLI entrypoints in `pyproject.toml` (`[project.scripts]`)
4. **Docker setup**: Check for `docker-compose.yml`, `docker-compose.dev.yml`, `compose.yml`, `compose.dev.yml`, `Dockerfile`, or similar files. Identify development-specific compose files vs production ones.
5. **Environment-based config**: Check if the project uses environment variables, `.env` files, or settings modules to toggle dev-only features (this informs where to gate `smello.init()`).

## Step 2: Present the plan

After exploring, present a clear plan with these sections:

### A. Install the packages

The recommended approach is to install `smello` as a **regular (not dev) dependency**. It has zero dependencies itself, and `smello.init()` is a safe no-op when `SMELLO_URL` is not set — no patching, no threads, no side effects. This means users don't need conditional imports or `try/except ImportError` guards in production.

Based on the package manager detected:

- **pip + requirements.txt**: `pip install smello` (add `smello` to `requirements.txt`)
- **pip + pyproject.toml**: Add `smello` to `[project.dependencies]`
- **uv**: `uv add smello`
- **poetry**: `poetry add smello`
- **pipenv**: `pipenv install smello`

The server is covered separately in section D below.

### B. Add `smello.init()` to the entrypoint

Propose the exact file and location. The two lines must go **before** any HTTP library imports or usage:

```python
import smello
smello.init()
```

Common placement patterns:

- **Django**: In `manage.py` (for `runserver`) or a custom `AppConfig.ready()` method
- **Flask**: At the top of `create_app()` or the app factory
- **FastAPI**: At module level in the main app file, or in a `lifespan` handler
- **CLI / script**: Near the top of `if __name__ == "__main__":`
- **General**: Wherever the application bootstraps, before HTTP calls are made

Since Smello uses the server URL as its activation signal, the recommended pattern is to always call `smello.init()` and control activation via the `SMELLO_URL` environment variable:

```python
import smello
smello.init()  # only activates when SMELLO_URL is set
```

Then in `.env` or the shell:

```bash
SMELLO_URL=http://localhost:5110
```

This way the code has zero conditional logic — without `SMELLO_URL`, `init()` is a safe no-op (no patching, no threads, no side effects).

### C. Configure via environment variables

Smello supports full configuration via `SMELLO_*` environment variables. Suggest adding these to the project's `.env`, `.env.development`, or equivalent:

```bash
SMELLO_URL=http://localhost:5110                  # server URL (activates Smello)
# SMELLO_CAPTURE_HOSTS=api.stripe.com,api.openai.com  # only capture these hosts
# SMELLO_IGNORE_HOSTS=localhost,internal.svc      # skip these hosts
# SMELLO_REDACT_HEADERS=Authorization,X-Api-Key   # headers to redact
```

All parameters can also be passed explicitly to `smello.init()`, which takes precedence over env vars:

- If the app talks to specific APIs, suggest `SMELLO_CAPTURE_HOSTS=api.example.com` or `capture_hosts=["api.example.com"]`
- If there are internal services to skip, suggest `SMELLO_IGNORE_HOSTS=...` or `ignore_hosts=[...]`
- If a non-default server URL is needed (e.g., Docker networking), suggest `SMELLO_URL=http://smello:5110` or `server_url="http://smello:5110"`
- Always mention that `Authorization` and `X-Api-Key` headers are redacted by default

Boolean env vars accept `true`/`1`/`yes` and `false`/`0`/`no` (case-insensitive). List env vars are comma-separated.

### D. Set up the server

**Ask the user** which server setup they prefer:

1. **No server setup** — they'll install and run `smello-server` separately (skip this section)
2. **Docker Compose** — add a Smello service to their compose file
3. **Development dependency** — add `smello-server` to their project's dev dependencies

`pip install smello-server` includes the full web dashboard — Docker is not required for the UI.

#### Option: Docker Compose

If the user chooses Docker Compose, propose adding a Smello service:

```yaml
smello:
  image: ghcr.io/smelloscope/smello
  ports:
    - "5110:5110"
  volumes:
    - smello-data:/data
```

And add `smello-data` to the `volumes:` section. The app container should set `SMELLO_URL=http://smello:5110` (or pass `server_url="http://smello:5110"` to `init()`) to reach the Smello server over the Docker network.

Prefer adding this to a dev-specific compose file (`docker-compose.dev.yml`, `compose.dev.yml`, `compose.override.yml`) if one exists. If only a single compose file exists, note that the user may want to create a dev overlay.

#### Option: Development dependency

If the user chooses to add the server as a dev dependency, use the same package manager pattern from section A:

- **pip + requirements.txt**: Add `smello-server` to `requirements-dev.txt`
- **pip + pyproject.toml**: Add `smello-server` to the dev dependency group
- **uv**: `uv add --dev smello-server`
- **poetry**: `poetry add --group dev smello-server`
- **pipenv**: `pipenv install --dev smello-server`

Then run with `smello-server run`, or as a standalone tool:

```bash
# With uv
uv tool install smello-server

# With pipx
pipx install smello-server
```

## Step 3: Wait for approval

After presenting the plan, ask the user which parts they want to proceed with. Do NOT edit any files until explicitly told to do so.

## Reference

- Smello client SDK: `pip install smello` (Python >= 3.10, zero dependencies)
- Smello server: `pip install smello-server` (Python >= 3.14, includes web dashboard) or Docker `ghcr.io/smelloscope/smello`
- Dashboard: http://localhost:5110 (served by both pip install and Docker)
- Supported libraries: `requests` (patches `Session.send()`), `httpx` (patches `Client.send()` and `AsyncClient.send()`), and `grpc` (patches `insecure_channel()` and `secure_channel()`)
- Default redacted headers: `Authorization`, `X-Api-Key`
- Default server URL: `http://localhost:5110`

### Environment variables

| Variable | Type | Default |
|----------|------|---------|
| `SMELLO_URL` | string | `None` (inactive) |
| `SMELLO_CAPTURE_ALL` | bool | `true` |
| `SMELLO_CAPTURE_HOSTS` | comma-separated list | `[]` |
| `SMELLO_IGNORE_HOSTS` | comma-separated list | `[]` |
| `SMELLO_REDACT_HEADERS` | comma-separated list | `Authorization,X-Api-Key` |

Precedence: explicit `init()` parameter > env var > hardcoded default.
