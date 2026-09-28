---
name: env-check
hub_skill_version: 3
description: >-
  Detect CLOUD_AGENT vs LOCAL_WORKSPACE and apply the matching agent
  constraints. Use at session start when choosing tests, credentials, Hub
  continuity fallback, or whether local skill CLIs (e.g. graphify) exist.
  Hub MCP unavailable (not runtime alone) triggers the forge `[ADHD]` issue
  mailbox; never invent Hub or graphify state.
---

# Env check — Cloud agent vs local workspace

## When to use

Run early in a session (or when continuity / credentials / browser tests / local CLIs matter) to classify the host. Use the result as **supporting context**. The Hub continuity fallback is triggered when **ADHD Hub MCP is missing, errored, unauthorized, or otherwise unavailable** — not merely because the runtime looks like a cloud sandbox.

## Quick detect

Resolve `scripts/check_runtime.sh` relative to **this skill’s install location** (not the ADHD Hub source tree alone).

Supported layouts:

| Layout | Example command |
|--------|-----------------|
| ADHD Hub source checkout | `bash skills/env-check/scripts/check_runtime.sh` |
| Project-scoped install (`.agents/skills`) | `bash .agents/skills/env-check/scripts/check_runtime.sh` |
| Global / plugin install | From the installed `env-check` skill directory: `bash scripts/check_runtime.sh` |

```bash
# Project-scoped (common after adhd-hub sync-project / setup --project-skills):
bash .agents/skills/env-check/scripts/check_runtime.sh
```

Output lines:

- `RUNTIME_ENV: CLOUD_AGENT` or `RUNTIME_ENV: LOCAL_WORKSPACE`
- `RUNTIME_SIGNALS: …` (container / Cursor markers; informational)
- `HUB_CONTINUITY_TRIGGER: MCP unavailable …`
- `LOCAL_SKILL_CLIS: …` (CLOUD_AGENT: do not assume; LOCAL_WORKSPACE: may be available)

### Detection quality

The script **does not** treat `$USER=root` as cloud by itself (false positives on local root shells). It combines:

- Cursor Cloud markers: `CURSOR_AGENT`, `__CURSOR_SANDBOX_ENV_RESTORE`, `/tmp/cursor/cloud-agent-transcripts`, `/exec-daemon`, plus agent sockets when paired with container cues
- Container cues (`/.dockerenv`, cgroup) as **supporting** signals only — local Docker alone stays `LOCAL_WORKSPACE`

Do not invent “I'm in cloud” from a single weak hint. Prefer the script output when unsure.

## CLOUD_AGENT guidelines

When `RUNTIME_ENV: CLOUD_AGENT` (Cursor Cloud / remote sandbox):

- **Do not assume** machine-installed local skill binaries or CLIs exist (examples: `graphify`, other opt-in companions installed on a developer laptop). Cloud/remote sandboxes often cannot see those tools even when project rules mention them.
- If a required local CLI is missing: one-line notice, then continue via repo tools (Read/Grep/Glob/tests) and any **committed** artifacts such as `graphify-out/` when present. Never fabricate graphify graph output or Hub continuity/progress/thread state.
- No native browser GUI or macOS/Windows desktop binaries; prefer headless tests and CLI verification
- Prefer injected environment / OIDC / platform secrets over committing or relying on `.env.local`
- Local-only assumptions (opening `localhost` GUIs, host Docker socket from the agent VM, Tailscale to a private Hub) may fail — plan accordingly
- If Hub MCP tools are missing/errored/unauthorized: on the first substantial Hub-worthy turn, the **first line** of the reply MUST say Hub MCP is not available, plus a short fix hint (MCP URL → this Hub's `/mcp`, `ADHD_HUB_AUTH_TOKEN`, restart the agent; skip/cancel Auth if it hangs until Hub OAuth is enabled). Never invent Hub state or claim a Hub write succeeded
- Fallback still applies when Hub MCP is down: when issue-write access exists and the identity is on Hub **Inbox authors**, open/update a forge/GitHub issue titled `[ADHD] …` with Goal / Focus / Next / Resume (or Now / Done / Next / Return). Optional labels `adhd-hub`, `project:<slug>`, `source:cursor` — skip labels if the token cannot set them. Recommended: append `Made with [ADHD Progress Hub](https://github.com/uniskela/adhd-hub)` under a non-imported heading (e.g. `## Attribution`). No secrets, private Hub URLs, internal hosts/IPs, absolute local paths, or transcripts. Otherwise state that continuity persistence is unavailable and continue authorized work.

## LOCAL_WORKSPACE guidelines

When `RUNTIME_ENV: LOCAL_WORKSPACE` (including local Docker / localhost):

- Machine-installed local skill CLIs (e.g. `graphify`) **may** be available — use them when present; still do not invent output if a binary is missing
- Local Docker, localhost services, and host browsers are OK when the operator's machine provides them
- Prefer Hub MCP (`resolve_project`, `session_digest`, `upsert_progress`, …) when it is reachable
- Same no-hallucination rule if MCP is down: acknowledge + fix hint; never invent Hub state; use the forge `[ADHD]` mailbox only when write access + Inbox authors allow it

## Continuity priority

1. **MCP unavailable?** → loud first-line warning + forge `[ADHD]` fallback (if allowed) — this is the Hub continuity trigger (still true on CLOUD_AGENT)
2. **Runtime env** → choose tests, credentials, tooling constraints, and whether local skill CLIs are expected
3. Prefer Hub MCP whenever it is available, on either runtime

See also: `adhd-hub-session` (full Hub protocol), [docs/forge-issue-inbox.md](https://github.com/uniskela/adhd-hub/blob/main/docs/forge-issue-inbox.md).
