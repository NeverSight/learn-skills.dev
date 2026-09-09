---
name: locust-best-practices
description: >
  Guides developers and testers in writing, fixing, and structuring Locust load test
  scripts in Python. Use this skill whenever the user mentions Locust, locustfile,
  HttpUser, TaskSet, load testing with Python, virtual users, spawn rate, wait_time,
  catch_response, LoadTestShape, ramp-up stages, or wants to benchmark an API or
  service using Locust — even if they do not explicitly say "Locust" or "load test".
license: MIT
compatibility: "Claude Code, Cursor, Windsurf. Requires Python 3.8+ and locust installed (pip install locust)."
model: sonnet
metadata:
  author: rcampos
  version: "1.2"
  tags: [locust, load-testing, performance, python]
---

# Locust Scenario Builder

Enforces a consistent, production-ready pattern for Locust load test scripts in
**Python**, covering HTTP/REST APIs with realistic user behavior, custom load shapes,
and proper response validation.

## Output Format

When producing or fixing a locustfile, always deliver three things:

1. **A complete, runnable locustfile** — never a partial snippet.
2. **The exact run command** with all flags needed (`--headless`, `-u`, `-r`, `-t`, `--host`).
3. **A one-line explanation** of the wait_time strategy chosen and why it fits the load goal.

---

## Step 1 — Gather Context

Ask only what is unknown:

- **Goal:** New locustfile · Fix existing locustfile · Specific API question
- **Protocol:** HTTP/REST (default) · WebSocket · gRPC
- **Workload:** Fixed concurrent users or fixed arrival rate (RPS)?
- **Auth:** None · Login on start · Token from environment variable?
- **Data:** Static · CSV file · Generated per user?

**Only load [references/SHAPES.md](references/SHAPES.md) when the user asks about custom load profiles, multi-stage ramps, spike simulation, or `LoadTestShape`.**

**Only load [references/PROTOCOLS.md](references/PROTOCOLS.md) when the user mentions WebSocket, gRPC, or testing non-HTTP protocols.** Contains custom client wrappers, `events.request.fire()` pattern, and protocol compatibility notes.

**Only load [references/DESIGN-PATTERNS.md](references/DESIGN-PATTERNS.md) when the user asks about project structure, multiple user classes, TaskSet, shared auth helpers, CSV data loading at scale, modular locustfiles, or multi-file organization.**

**Only load [references/RUNNING.md](references/RUNNING.md) when the user asks about headless mode, CI/CD integration, exit codes, SLA-based build failures, distributed testing, master/worker setup, multiple cores, logging to file, or custom log levels.**

---

## Step 2 — Apply the 4-Block Pattern

Every locustfile must follow this structure. Generate the complete skeleton first, then fill in details.

```
Block 1 → Imports + config    locust imports, constants, env vars
Block 2 → User class          HttpUser with host, wait_time, on_start, @task methods
Block 3 → Shape (optional)    LoadTestShape for custom ramp profiles
Block 4 → Run command         locust CLI with all flags as a comment at the bottom
```

---

## Step 3 — HttpUser Rules

### 3.1 Always use `catch_response=True` for validation

Never rely on HTTP status alone. Always validate the response body:

```python
# Wrong — only checks HTTP status, misses business logic errors
self.client.get("/api/users")

# Correct — validates response content
with self.client.get("/api/users", catch_response=True) as response:
    if response.status_code != 200:
        response.failure(f"Expected 200, got {response.status_code}")
    elif "users" not in response.json():
        response.failure("Missing 'users' key in response")
```

### 3.2 Group dynamic URLs with `name=`

Without grouping, each unique URL creates a separate stats entry — flooding the report:

```python
# Wrong — creates N separate stats rows
for user_id in range(100):
    self.client.get(f"/user/{user_id}")

# Correct — groups all under one stats entry
for user_id in range(100):
    self.client.get(f"/user/{user_id}", name="/user/[id]")
```

### 3.3 Use `on_start` for auth — never share tokens across users

Each virtual user must authenticate independently:

```python
# Wrong — shared token is a race condition and not realistic
shared_token = None

class MyUser(HttpUser):
    def on_start(self):
        global shared_token  # ❌ shared state across users

# Correct — each user gets its own token
class MyUser(HttpUser):
    def on_start(self):
        response = self.client.post("/auth/login", json={
            "username": os.environ["TEST_USER"],
            "password": os.environ["TEST_PASSWORD"],
        })
        self.token = response.json()["access_token"]

    @task
    def get_profile(self):
        self.client.get("/profile", headers={"Authorization": f"Bearer {self.token}"})
```

### 3.4 Choose `wait_time` based on the load goal

| Goal | wait_time | Why |
|---|---|---|
| Simulate real users with think time | `between(1, 5)` | Realistic pacing |
| Maintain fixed RPS regardless of latency | `constant_throughput(2)` | Open model — 2 tasks/sec per user |
| Reproduce exact user pacing | `constant(1)` | Fixed interval |

> **Never use `wait_time = constant(0)`** — zero think time generates 10–100× more load than real users and produces unrealistic results.

### 3.5 Use `@task` weight to reflect real traffic distribution

```python
class ShopUser(HttpUser):
    wait_time = between(1, 3)

    @task(10)   # 10× more common — most users just browse
    def browse_products(self):
        self.client.get("/products")

    @task(3)    # 3× — some users search
    def search(self):
        self.client.get("/search?q=shoes", name="/search")

    @task(1)    # 1× — few users actually purchase
    def checkout(self):
        self.client.post("/checkout", json={"cart_id": self.cart_id})
```

---

## Step 4 — Standard Locustfile Template

```python
import os
import json
from locust import HttpUser, task, between, events

# ---------------------------------------------------------------------------
# Block 1 — Config
# ---------------------------------------------------------------------------
BASE_URL = os.environ.get("TARGET_HOST", "http://localhost:8080")

# ---------------------------------------------------------------------------
# Block 2 — User class
# ---------------------------------------------------------------------------
class ApiUser(HttpUser):
    host = BASE_URL
    wait_time = between(1, 3)

    def on_start(self):
        """Runs once per virtual user before any task executes."""
        with self.client.post(
            "/auth/login",
            json={
                "username": os.environ["TEST_USER"],
                "password": os.environ["TEST_PASSWORD"],
            },
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                self.token = response.json()["access_token"]
            else:
                response.failure(f"Login failed: {response.status_code}")
                self.token = None

    def _auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def get_items(self):
        with self.client.get(
            "/api/items",
            headers=self._auth_headers(),
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"GET /api/items failed: {response.status_code}")

    @task(1)
    def create_item(self):
        with self.client.post(
            "/api/items",
            json={"name": "test-item", "value": 42},
            headers=self._auth_headers(),
            catch_response=True,
        ) as response:
            if response.status_code not in (200, 201):
                response.failure(f"POST /api/items failed: {response.status_code}")

# ---------------------------------------------------------------------------
# Block 3 — Events (optional)
# ---------------------------------------------------------------------------
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("Test started — verifying environment variables...")
    for var in ["TEST_USER", "TEST_PASSWORD"]:
        if not os.environ.get(var):
            raise ValueError(f"Missing required env var: {var}")

# ---------------------------------------------------------------------------
# Run command (headless):
# TEST_USER=alice TEST_PASSWORD=secret locust -f locustfile.py \
#   --headless -u 50 -r 5 -t 5m --host http://your-api.com \
#   --html report.html --csv results
# ---------------------------------------------------------------------------
```

---

## Step 5 — Common Mistakes

### 1. No `catch_response=True` — silent failures
Without it, a 500 response with a valid HTTP connection still counts as success in Locust's stats. Always use `catch_response=True` and call `response.failure()` explicitly.

### 2. Missing `name=` on dynamic URLs
Every unique URL path creates a new row in the stats table. Parameterized paths like `/user/123`, `/user/456` explode the report. Use `name="/user/[id]"`.

### 3. Shared mutable state between users
Locust users run in greenlets (gevent), not threads, but shared state still causes race conditions in logic. Always store per-user state (`self.token`, `self.cart_id`) as instance attributes.

When loading credentials from CSV, store **all fields** as instance attributes in `on_start` — not just one:
```python
# Wrong — only stores username, password is lost
self.username = row["username"]

# Correct — store every field the user will need
self.username = row["username"]
self.password = row["password"]
```

### 4. `wait_time = constant(0)` or no `wait_time`
Omitting think time generates unrealistic load and will saturate your test machine before the target system. Always define a meaningful `wait_time`.

### 5. Hardcoded host and credentials
Never hardcode `host`, usernames, or passwords. Always use environment variables:
```python
host = os.environ.get("TARGET_HOST", "http://localhost:8080")
```

### 6. Asserting only status code, not response body
A 200 with `{"error": "token expired"}` will pass a status-only check. Always validate the response body for business logic correctness.

### 7. Using `FastHttpUser` without understanding the tradeoff
`FastHttpUser` uses `geventhttpclient` instead of `requests`. It is faster but does **not** support all `requests` features (cookies jar, some auth helpers). Only use it when you have proven a throughput bottleneck in the test runner itself, not the target system.

---

## Step 6 — Run Commands Reference

```bash
# Basic headless run — 50 users, 5/sec ramp, 5 minutes
locust -f locustfile.py --headless -u 50 -r 5 -t 5m --host https://api.example.com

# With HTML report and CSV output
locust -f locustfile.py --headless -u 100 -r 10 -t 10m \
  --host https://api.example.com \
  --html report.html --csv results

# Run specific user class only
locust -f locustfile.py --headless -u 50 -r 5 -t 5m \
  --host https://api.example.com ApiUser

# With environment variables
TARGET_HOST=https://api.example.com \
TEST_USER=alice \
TEST_PASSWORD=secret \
locust -f locustfile.py --headless -u 50 -r 5 -t 5m

# Open web UI (no --headless) — useful for interactive exploration
locust -f locustfile.py --host https://api.example.com
```

**Flag reference:**

| Flag | Meaning |
|---|---|
| `-u` | Peak number of concurrent users |
| `-r` | Spawn rate — users added per second |
| `-t` | Total run time (e.g. `30s`, `5m`, `2h`) |
| `--headless` | No web UI — run and exit automatically |
| `--host` | Target base URL |
| `--html` | Generate HTML report at path |
| `--csv` | Generate CSV stats files at prefix |
| `--only-summary` | Suppress per-interval stats output |
