---
name: vp-long-running-processes
description: >-
  Safely reuse, start, inspect, stop, or restart persistent processes such as
  servers, watchers, browsers, and background agents, including local daemons
  exposed through stable named URLs. Boundary: not for one-shot commands that
  naturally exit.
---

# Long-Running Processes

Identify processes by command, working directory, ownership, and purpose—not by
port alone.

Before starting, look for a healthy reusable instance for the same project.
Before stopping or restarting, establish the exact process tree, dependents,
logs, and user impact, then obtain authorization unless the user already
requested that exact action.

Keep persistent commands detached from the task's blocking execution path and
record where their output can be inspected. Verify service readiness rather than
assuming a live process is healthy. Report conflicts instead of killing unknown
processes.

## Named local URLs

For a local development daemon that opens an HTTP port, consider
[Portless](https://github.com/vercel-labs/portless) when a stable named URL would
make reuse, worktree isolation, or browser access clearer. Treat Portless as an
optional routing layer, not as the process owner: retain the daemon command,
working directory, process tree, logs, and readiness evidence.

If Portless is already available, prefer its inferred project and worktree name
when that name is unambiguous. Start the application through `portless` or
`portless run`, then verify the named URL and use `portless list` or
`portless doctor` when route or proxy health is unclear. For a daemon that
Portless does not launch, use a static alias only after verifying the exact
target port and owner.

When setup is requested and Portless is absent, consult its
[installation and usage guide](https://github.com/vercel-labs/portless#readme),
inspect the project's package manager and conventions, and offer the smallest
appropriate install and command change. Obtain authorization before installing
the dependency, trusting its local CA, changing system startup, or persisting
project configuration. Do not copy Portless internals or maintain a parallel
setup guide here.

The Portless proxy can be shared by unrelated projects. Do not use
`--force`, `prune`, `clean`, `proxy stop`, or service install/uninstall as a
shortcut for route conflicts. First establish the affected routes, processes,
and user impact, then apply the normal authorization rules above.

## Related skills

- [`vp-agent-browser-session`](https://github.com/VdustR/skills/tree/main/skills/vp-agent-browser-session)
  for persistent agent-browser sessions and managed Chrome profiles.
- [`vp-tunnel`](https://github.com/VdustR/skills/tree/main/skills/vp-tunnel)
  when a remote caller or public page must reach the local daemon.
- [`vp-session-wrapup`](https://github.com/VdustR/skills/tree/main/skills/vp-session-wrapup)
  when a session ends with processes that must be stopped or reported.
