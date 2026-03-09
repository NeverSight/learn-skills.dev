---
name: audit-openclaw-security
description: Audit and harden OpenClaw (Gateway + agents) security. Use when the user asks to audit/secure/harden OpenClaw; when troubleshooting risky exposure (especially the Gateway web UI/control plane on port 18789); when reviewing DM/group access control (pairing/allowlists/mention-gating); tool permissions (exec/fs/browser/nodes/gateway/cron); plugins/skills supply-chain risk; secrets/transcripts/log retention; or when deploying OpenClaw on a Mac mini, personal laptop, Docker host, or cloud VM (AWS EC2/VPS).
license: MIT
compatibility: Works best in Claude Code (local shell access). In Claude.ai, instruct the user to run the included scripts/commands locally and share redacted outputs (prefer `openclaw status --all` and `openclaw security audit --json`).
metadata:
  author: "community"
  version: "2.0.0"
  upstream: "OpenClaw docs + security guidance (updated Feb 2026)"
---

# audit-openclaw-security

Teach the agent to perform a **defensive, permissioned** security audit of an OpenClaw deployment and produce an actionable report + remediation plan.

OpenClaw is a local-first personal AI assistant with a Gateway control plane, multi-channel inbox, tools (browser/fs/exec/nodes), and optional remote access patterns. The goal of this skill is to **reduce attack surface** (network + identity), **minimise agent permissions**, and **protect secrets/transcripts**.

## Scope and safety rules (non-negotiable)

1. **Only audit systems you own or have explicit permission to test.**
2. **Do not request or handle raw secrets.** Never ask for:
   - gateway tokens/passwords
   - model API keys / OAuth tokens
   - WhatsApp creds, Slack tokens, Discord tokens, etc.
3. Prefer outputs that are designed to be shareable/redacted:
   - `openclaw status --all`
   - `openclaw security audit --json` (and `--deep --json`)
4. Treat **any remote browser control / node pairing** as *admin-equivalent access* and audit accordingly.
5. Default to **audit-only**. If the user wants remediation, propose changes and get explicit approval before running any:
   - `openclaw security audit --fix`
   - config edits (`openclaw config set`, Control UI Config, `config.apply` / `config.patch`)
   - firewall edits
   - restarts

## What “good” looks like (target posture)

- Gateway binds to loopback unless there is a strong reason otherwise.
- Strong Gateway auth (token/password, rotated) is enabled.
- No public internet exposure (no open security group / port-forward / Tailscale Funnel / accidental reverse proxy bypass).
- DMs require pairing or strict allowlists; group chats require mention-gating.
- Tooling is least-privilege (deny/ask for exec; workspace-only FS; deny control-plane tools on untrusted surfaces).
- Secrets are stored with tight filesystem permissions; logs/transcripts have a retention plan.
- Plugins/skills are explicitly trusted, minimal, and protected from unauthorised modification.

## Workflow

### Step 0 — Establish context (fast)

Collect just enough context to pick the right audit path:

- Where is OpenClaw running?
  - **Mac mini** (always-on home host)
  - **Personal laptop** (macOS/Windows/Linux)
  - **Docker** (local or on a VM)
  - **Cloud host** (AWS EC2 / VPS)
- Install type?
  - native install vs Docker Compose vs source checkout
- Do we have **local shell access**?
  - **Claude Code**: can run commands directly
  - **Claude.ai**: user must run commands and paste outputs

Then pick one of these modes:

- **Mode A: Assisted self-audit (Claude.ai)** — user runs commands/scripts, shares redacted output.
- **Mode B: Automated local audit (Claude Code)** — run scripts directly and generate a report.

---

## Mode A — Assisted self-audit (no local shell access)

Ask the user to run the following on the OpenClaw host and paste results.

> If they are worried about sharing output, reassure them that `openclaw status --all` and `openclaw security audit --json` are intended to be shareable. If they still refuse, provide high-level hardening guidance without requesting outputs.

### 1) Collect OpenClaw posture (recommended minimum)

```bash
openclaw --version
openclaw status --all
openclaw doctor
openclaw security audit --json
openclaw security audit --deep --json
```

Helpful extras (for supply-chain + snapshot context):

```bash
openclaw health --json
openclaw skills list --eligible --json
openclaw plugins list --json
```

If the user is comfortable sharing a config for review, prefer **targeted** reads over full-file sharing:

```bash
openclaw config get gateway.bind
openclaw config get gateway.auth.mode
openclaw config get discovery.mdns.mode
openclaw config get session.dmScope
```

If they *must* share the full config, remind them OpenClaw config is **JSON5** (`~/.openclaw/openclaw.json`), not strict JSON, and have them use the redaction script:

```bash
python3 scripts/redact_openclaw_config.py ~/.openclaw/openclaw.json > openclaw.json5.redacted
```

### 2) Collect host/network posture (pick the right block)

**macOS (Mac mini / Mac laptop):**
```bash
whoami
sw_vers
uname -a
lsof -nP -iTCP -sTCP:LISTEN
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode
fdesetup status || true
```

**Linux (EC2/VPS):**
```bash
whoami
cat /etc/os-release
uname -a
ss -ltnp
sudo ufw status verbose || true
sudo nft list ruleset || true
sudo iptables -S || true
```

**Docker deployments (local or on a VM):**
```bash
docker ps
# confirm published listeners (should be 127.0.0.1:18789, not 0.0.0.0:18789)
docker port openclaw-gateway 18789 || true
docker compose ps || true
```

---

## Mode B — Automated local audit (Claude Code)

If shell tools are available, run:

```bash
bash scripts/collect_openclaw_audit.sh --out ./openclaw-audit
python3 scripts/render_report.py --input ./openclaw-audit --output ./openclaw-security-report.md
```

Then open `openclaw-security-report.md`, refine wording, and present the report to the user.

---

## Analysis and reporting

### Step 1 — Triage findings by severity

Use OpenClaw’s audit output as the source of truth. Prioritise in this order:

1. **Anything “open” + tools enabled** (lock down DMs/groups first; then tighten tools/sandbox)
2. **Public network exposure** (LAN bind, Tailscale Funnel, reverse proxy mistakes, missing auth)
3. **Browser control / nodes exposure** (treat like operator access)
4. **File permissions** on `~/.openclaw` (config/state/credentials)
5. **Plugins/extensions + dynamic skill loading** (supply chain)
6. **Model hygiene + prompt-injection resilience** (important, but secondary to access control)

### Step 2 — Translate findings into a clear risk narrative

For each finding, capture:

- **What was observed** (quote `checkId` + summary; do not paste secrets)
- **Why it matters**
- **Impact** (data exfiltration, account takeover, unauthorised actions, persistence)
- **Concrete remediation steps**
- **Verification** (usually rerun `openclaw security audit --deep`)

### Step 3 — Recommend a secure baseline configuration (when appropriate)

Offer the baseline in `references/openclaw-baseline-config.md` as a starting point and adapt based on needs:

- single-user vs shared inbox
- required tools
- remote access method (SSH tunnel / Tailscale Serve)

### Step 4 — Platform-specific guidance

Use the platform playbooks:

- `references/platform-mac-mini.md`
- `references/platform-personal-laptop.md`
- `references/platform-aws-ec2.md`
- `references/platform-docker.md`

---

## Deliverable

Produce a Markdown security audit report using `assets/report-template.md`:

- Executive summary (1–2 paragraphs)
- Environment overview (host type, install type, exposure)
- Findings table (Critical/High/Medium/Low)
- Remediation plan (sequenced)
- Verification steps
- Residual risk + operational practices (patching, token rotation, retention)

---

## Common remediation patterns (use with care)

### Network exposure

- Prefer Gateway bound to loopback and remote access via **SSH tunnel** or **Tailscale Serve**.
- Avoid **Tailscale Funnel** for the Gateway.
- Never expose the Gateway control UI directly to the public internet.
- If you must run a reverse proxy, configure **trusted proxies** and block direct access to the Gateway port.

### Identity & access

- Use token/password auth; rotate periodically and after any suspected leakage.
- If you need a token generated in automation: `openclaw doctor --generate-gateway-token`.
- Require DM pairing or strict allowlists.
- In groups, require mention gating; avoid always-on bots in large groups.

### Control-plane tools

- The `gateway` and `cron` tool surfaces can create persistence (config changes, scheduled jobs). Deny them on any surface that handles untrusted content.

### Least privilege tools

- Keep filesystem tools workspace-only.
- Keep exec denied or “ask always” unless the user is present and approving actions.
- Treat browser control like operator access; keep it tailnet/local only.

### Secrets, transcripts, and logs

- Tight permissions on `~/.openclaw` and `~/.openclaw/openclaw.json`.
- Treat session transcripts as sensitive (`~/.openclaw/agents/<agentId>/sessions/*.jsonl`).
- Gateway logs default under `/tmp/openclaw/openclaw-YYYY-MM-DD.log` (or `logging.file`).
- Keep redaction enabled and set a retention/pruning policy.

---

## Troubleshooting

### “openclaw: command not found”

- Confirm OpenClaw CLI is installed and on PATH.
- If using Windows, prefer WSL2.
- Re-run installation via the official method for your platform; then re-run `openclaw --version`.

### “refusing to bind ... without auth”

- Expected guardrail: non-loopback binds require auth. Do not bypass.

### Audit output is empty or inconsistent

- Ensure the Gateway is running: `openclaw gateway status`
- Re-run with `--deep` for best-effort live probing.

---

## Trigger tests (for skill author)

Should trigger:

- “Can you audit my OpenClaw setup for security?”
- “My OpenClaw gateway is on port 18789 — is that safe?”
- “I deployed OpenClaw on EC2; give me a hardening checklist.”
- “Run openclaw security audit and interpret the results.”
- “I’m running OpenClaw in Docker—how do I lock it down?”

Should NOT trigger:

- General macOS security advice unrelated to OpenClaw
- Generic AWS hardening unrelated to OpenClaw
- Unrelated software audits
