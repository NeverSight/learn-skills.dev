---
name: port-selector
description: Allocate stable free ports for local development servers, previews, test runners, browser automation, and parallel worktrees with the port-selector CLI. Use when starting or restarting any process that binds a localhost port, when a fixed port is occupied or produces EADDRINUSE/address-already-in-use errors, when several services need distinct ports, or when later commands need to rediscover the same project port.
---

# Port Selector

Use `port-selector` instead of hard-coded ports or hand-written `lsof` loops. Allocate from the same working directory in which the service runs because allocations are stable per `(directory, name)`.

## Start a local service

1. Confirm the CLI is available with `command -v port-selector`. If it is missing, install it with the repository's documented method before continuing.
2. Choose a short stable service name such as `web`, `api`, `docs`, `preview`, or `e2e`. Use different names for services that run concurrently from the same directory.
3. Allocate and start the process in one shell command. Quote the port variable.

```bash
PORT="$(port-selector --name preview)"
python3 -m http.server "$PORT"
```

Adapt how the port is passed to the program:

```bash
# Program reads PORT from the environment
PORT="$(port-selector --name web)" npm run dev

# Program accepts a port flag
PORT="$(port-selector --name web)"
npm run dev -- --port "$PORT"

# Playwright or another consumer needs a base URL
PORT="$(port-selector --name e2e)"
BASE_URL="http://127.0.0.1:$PORT" npx playwright test
```

For a later shell call, run `port-selector --name <name>` again from the same directory instead of copying a port number from prior output. It returns the stable allocation.

## Verify before using

Wait for the service to report readiness or probe its expected endpoint on the allocated port. Do not assume that process startup means the listener is ready.

```bash
PORT="$(port-selector --name preview)"
curl --fail --silent --show-error "http://127.0.0.1:$PORT/" >/dev/null
```

If the expected service is already responding, reuse it instead of starting a duplicate process. Use `port-selector --list` or `port-selector --verbose --name <name>` when allocation ownership is unclear.

## Recover from a bind conflict

Never kill or replace an unknown listener merely to claim its port.

If startup fails with `EADDRINUSE`, `Address already in use`, or an equivalent bind error:

1. Stop and reuse the existing process if it is the intended service.
2. Otherwise remove only this directory's named allocation:

```bash
port-selector --forget --name preview
```

3. Allocate again with the same name and retry startup once.
4. If the retry also fails, inspect `port-selector --list` and report the conflict rather than starting an unbounded port scan.

Do not use `--forget-all`, `--force`, or terminate another process unless the user explicitly authorizes the broader action.

## Long-running and parallel work

- Keep the allocation after stopping a normal service so the project retains a predictable port.
- Use `port-selector --lock --name <name>` only when a port must remain reserved for a long-running service; unlock it when that reservation ends.
- Use separate names for `web`, `api`, databases, documentation, and test servers in the same directory.
- Let separate worktrees allocate from their own directories; do not copy one worktree's port into another.
- Prefer `127.0.0.1` for local verification unless the service requires a different bind address.
