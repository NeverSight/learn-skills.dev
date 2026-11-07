---
name: agentbox
description: Run web-scraping subagents inside isolated Docker sandboxes, one box per subagent. Each box has a terminal (curl, python), a persistent headless Chromium, passive request listeners that log every HTTP call, and an optional proxy with a hard budget and known cost per request. Use when a task fans out to several subagents that must browse or scrape websites, find hidden API endpoints behind pages, validate data sources or build crawlers, and you need every request and every agent step logged and auditable.
---

# agentbox

You are the **orchestrator**. For every subagent you spawn, you start one box (a Docker container) and hand its name to that subagent. The subagent keeps running on the host with its normal tools, but every web action goes through `agentbox exec <box> -- <command>`. Each box logs every request, every command and the agent's own journal, so you can check every claim a subagent makes before you report it.

```
orchestrator (you)
 ├─ subagent A ──docker exec──▶ box A: terminal · Chromium · listeners · proxy tunnel ──▶ proxy ──▶ website
 ├─ subagent B ──docker exec──▶ box B: …
 └─ subagent C ──docker exec──▶ box C: …
                                  └─ /work  ==  $AGENTBOX_HOME/runs/<box>/ on the host (logs, results)
```

## When the skill is activated, do this in order

1. **Docker**: read `docker/01-preflight.md` and run its checks. Stop and tell the user if Docker is missing or not running. Never install Docker yourself.
2. **Workspace and image**: read `docker/02-workspace.md`. If the workspace is not installed (or its version is older than this skill's), materialize every file listed there from the folders below, then build the image (`docker/03-image.md`). The host CLI is in `docker/04-cli.md`.
3. **Proxy**: read `proxy/01-config.md`. Make sure `$AGENTBOX_HOME/config/proxy.json` exists with the user's proxy services, the budget per box and the cost of each service. If it does not exist, ask the user for it (never invent credentials or prices). Boxes also work without a proxy, in direct mode only.
4. **Understand the moving parts** before briefing anyone (read once per session, skim later):
   - `proxy/02-routing.md`: how traffic leaves the box, `proxy on|off`, budget enforcement.
   - `listener/README.md`: how requests are observed without touching them.
   - `browser/browser.md`: the persistent browser and its CLI.
   - `logs/logs.md`: what is logged, the agent journal, the timeline and the audit.
5. **Orchestrate**: follow `subagents/orchestrator.md`. Brief each subagent with `subagents/subagent-prompt.md`, filled in, including the proxy cost table. The ladder subagents must follow is in `subagents/escalation.md`.
6. **Audit and report**: when a subagent finishes, collect its transcript, build the timeline and check every claim against the request log (`logs/logs.md`, "Audit"). Only then report.
7. **Tear down**: `agentbox down <box>` or `agentbox down --all`. Runs are kept on disk.

## Folder map

| Folder | What it holds |
|---|---|
| `docker/` | preflight checks, workspace layout, Dockerfile and image build, host CLI |
| `proxy/` | provider-agnostic proxy config (credentials, budget, cost per service), the browser tunnel, `proxy` command, budget accounting |
| `listener/` | shared logging library, browser listener (CDP), curl wrapper, python hook, `reqlog` |
| `browser/` | Chromium boot flags and the `browser` command |
| `logs/` | log files, agent journal, transcript import, timeline, claim audit |
| `subagents/` | orchestrator procedure, subagent prompt template, escalation ladder |

## Rules that always apply

- One box per subagent. Never share a box between subagents.
- Listeners only observe. Nothing sits in the traffic path or decrypts TLS for logging.
- The proxy is opt-in per box (`proxy on`) and capped by its budget. When the budget is spent, requests fail with HTTP 402. Costs are estimates from the configured prices; the provider's dashboard is the source of truth.
- Never try to get past a login, a paywall or a CAPTCHA. Report what is blocked and what sits behind it.
- Respect each site's terms and rate limits. Only scrape what the user is allowed to collect.
- A subagent's "blocked" or "not available" claim counts only if the log shows the failure at every rung of the escalation ladder.
