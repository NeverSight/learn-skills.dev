---
name: helpmetest-proxy
description: "Set up HelpMeTest proxy tunnels for local development testing. Use when user needs to test localhost, wants to substitute production URLs with local ports, or needs to route multiple services. Use when user says 'set up proxy', 'test localhost', 'tunnel to local', or before running tests against local development servers."
allowed-tools: mcp__helpmetest-*
---

# HelpMeTest Proxy Setup

Sets up proxy tunnels to test local development servers through HelpMeTest.

## Purpose

HelpMeTest tests run against URLs (http://localhost, http://my.app.com). For local development, the proxy tunnels these URLs to your local ports so tests can access your dev servers.

## When to Use

- Testing against localhost during development
- Substituting production URLs with local versions
- Routing frontend and backend on different ports
- Before writing or running any local tests

## Quick Start

**Basic setup:**
```bash
# If your app runs on port 3000
helpmetest proxy start localhost:3000
```

**Verify it works:**
```robot
# Use HelpMeTest interactive command
helpmetest_run_interactive_command({ command: "Go To  http://localhost" })
# Should load your local app
```

**Then write/run tests using:**
```robot
Go To  http://localhost
```

## Three Proxy Strategies

### Strategy 1: Single Tunnel to Frontend

**When to use:** Your dev server already proxies some routes internally (e.g., `/api` → backend port)

**Setup:**
```bash
# Frontend on port 5001, it proxies /api internally to port 3001
helpmetest proxy start localhost:5001
```

**In tests:**
```robot
Go To  http://localhost
# Both UI and /api calls work through the single tunnel
```

**Example:** Vite, webpack-dev-server with proxy configuration

---

### Strategy 2: Separate Tunnels for Frontend and Backend

**When to use:**
- Services need different hostnames (cookies, CORS)
- You want explicit separation in tests
- No internal proxy configured

**Setup:**
```bash
# Frontend on port 5001
helpmetest proxy start frontend.local:5001

# Backend on port 3001
helpmetest proxy start backend.local:3001
```

**In tests:**
```robot
Go To  http://frontend.local      # For UI
# API calls use http://backend.local/api
```

---

### Strategy 3: Substitute Production with Local

**When to use:**
- You have tests running against production URLs
- Want to test local changes without modifying test code
- Need production domain for cookies/sessions

**Setup:**
```bash
# Intercept my.awesome.app and route to local port 3000
helpmetest proxy start my.awesome.app:80:3000
```

**In tests:**
```robot
Go To  http://my.awesome.app
# Routes to localhost:3000 instead of production
```

**The port mapping format:**
- `domain` - hostname in test URLs
- `external_port` - port in test URLs (usually 80 for HTTP, 443 for HTTPS)
- `source_port` - your local development port

**Example:** Production tests use `http://my.awesome.app:80`, but you want to test local code running on port 3000

## Verification

**After starting proxy, always verify using HelpMeTest:**

The proxy only intercepts traffic within HelpMeTest's infrastructure. Use interactive commands to verify:

```robot
# For localhost
helpmetest_run_interactive_command({ command: "Go To  http://localhost" })

# For custom hostnames
helpmetest_run_interactive_command({ command: "Go To  http://frontend.local" })

# For production substitution
helpmetest_run_interactive_command({ command: "Go To  http://my.awesome.app" })
```

**Expected:** You should see your local app load successfully, not a connection error.

**If verification fails:** Don't write tests yet - fix the proxy setup first.

## Troubleshooting

### Tests can't reach the URL

**Check proxy is running:**
```bash
ps aux | grep "helpmetest proxy"
```

**Check local server is running:**
```bash
# Direct connection to your local port (bypasses proxy)
curl http://127.0.0.1:3000
```

**Check proxy output shows your tunnel:**
```
✓ Proxying localhost -> localhost:3000
# or
✓ Proxying frontend.local -> localhost:5001
```

**If tunnel missing:** Restart the proxy command

---

### Custom hostname not resolving (frontend.local, etc.)

Custom hostnames are handled by the proxy - you don't need to edit `/etc/hosts`. If verification fails:

1. Verify proxy is running
2. Check the exact hostname in proxy output
3. Ensure you're using HTTP (not HTTPS) unless you configured SSL

---

### Production substitution not working

**Check port mapping:**
```bash
# Wrong (missing source port)
helpmetest proxy start my.awesome.app:80

# Correct
helpmetest proxy start my.awesome.app:80:3000
```

**Verify substitution:**
```robot
# Use HelpMeTest to verify routing
helpmetest_run_interactive_command({ command: "Go To  http://my.awesome.app" })
# Should load from localhost:3000, not production
```

## Multiple Services Example

**Complex setup with frontend, backend, and production substitution:**

```bash
# Local frontend
helpmetest proxy start frontend.local:5001

# Local backend API
helpmetest proxy start api.local:3001

# Production service running locally
helpmetest proxy start prod.myapp.com:80:8000
```

**Tests can now use all three:**
```robot
Go To  http://frontend.local
# Make API call to http://api.local/endpoint
# Access production service at http://prod.myapp.com
```

## Best Practices

1. **Start proxy BEFORE writing tests** - Don't waste time debugging test failures caused by proxy not running

2. **Always verify with HelpMeTest** - Use `helpmetest_run_interactive_command` to confirm routing works before writing automated tests

3. **Choose simplest strategy** - If frontend already proxies backend, use Strategy 1 (single tunnel)

4. **Keep proxy running** - Start in background/separate terminal, don't restart unnecessarily

5. **Use consistent hostnames** - If you use `frontend.local` in one test, use it in all tests for that service

## Output Messages

**Success:**
```
✓ Proxying localhost -> localhost:3000
```

**Already exists (safe to ignore):**
```
[W] new proxy type error: proxy already exists
```
Means tunnel is already registered - your tests will still work.

**Version:** 0.1
