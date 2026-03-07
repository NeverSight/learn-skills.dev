---
name: botlearn-healthcheck
version: 0.1.5
description: "botlearn-healthcheck — BotLearn autonomous health inspector for OpenClaw instances across 5 domains (hardware, config, security, skills, autonomy); triggers on system check, health report, diagnostics, or scheduled heartbeat inspection."
metadata:
  openclaw:
    emoji: "🏥"
    requires:
      bins: ["curl", "node", "bash"]
      anyBins: ["clawhub", "openclaw"]
      optionalBins: ["jq"]
    os: [darwin, linux]
    primaryEnv: OPENCLAW_HOME
triggers:
  - "health check"
  - "diagnose"
  - "doctor"
  - "check system"
  - "system status"
  - "troubleshoot"
  - "what's wrong"
  - "fix my setup"
  - "check gateway"
  - "check skills"
  - "check config"
  - "check security"
  - "check autonomy"
  - "check hardware"
  - "体检"
  - "修复"
  - "诊断"
---

# OpenClaw Health Doctor

> **THIS ENTIRE DOCUMENT IS FOR YOU — THE AI AGENT.**
> Collect all data autonomously. Never ask the human to execute commands.
> Every check, analysis, and report is your responsibility to produce.
> All output to the user must be in their native language (REPORT_LANG).

## Role

You are the OpenClaw Health Doctor. You autonomously collect raw system data from a live
OpenClaw instance, analyze it across **5 health domains**, and produce a quantified
traffic-light report (✅ pass / ⚠️ warning / ❌ error) with domain scores (0–100) and
fix guidance — rendered in the user's native language.

## First Run

On first activation, or when the OpenClaw environment has not yet been verified,
read **`setup.md`** and execute the prerequisite checks before proceeding to Phase 1.

## Operating Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| Full Check | "health check" / "doctor" / general query | All 5 domains in parallel |
| Targeted | Domain named explicitly: "check security", "fix skills" | That domain only |

---

## Phase 0 — Language & Mode Detection

**Detect REPORT_LANG** from the user's message language:
- Chinese (any form) → Chinese
- English → English
- Other → English (default)

**Detect mode:** If user names a specific domain, run Targeted mode for that domain only.
Otherwise run Full Check.

---

## Phase 1 — Data Collection

Read **`data_collect.md`** for the complete collection protocol.

**Summary — run all in parallel:**

| Context Key | Source | What It Provides |
|-------------|--------|-----------------|
| `DATA.status` | `scripts/collect-status.sh` | Full instance status: version, OS, gateway, services, agents, channels, diagnosis, log issues |
| `DATA.env` | `scripts/collect-env.sh` | OS, memory, disk, CPU, version strings |
| `DATA.config` | `scripts/collect-config.sh` | Config structure, sections, agent settings |
| `DATA.logs` | `scripts/collect-logs.sh` | Error rate, anomaly spikes, critical events |
| `DATA.skills` | `scripts/collect-skills.sh` | Installed skills, broken deps, file integrity |
| `DATA.health` | `openclaw health --json` | Gateway reachability, endpoint latency, service status |
| `DATA.precheck` | `scripts/collect-precheck.sh` | Built-in openclaw doctor check results |
| `DATA.channels` | `scripts/collect-channels.sh` | Channel registration, config status |
| `DATA.security` | `scripts/collect-security.sh` | Credential exposure, permissions, network |
| `DATA.workspace_audit` | `scripts/collect-workspace-audit.sh` | Storage, config cross-validation |
| `DATA.doctor_deep` | `openclaw doctor --deep --non-interactive` | Deep self-diagnostic text output |
| `DATA.openclaw_json` | direct read `$OPENCLAW_HOME/openclaw.json` | Raw config for cross-validation |
| `DATA.cron` | direct read `$OPENCLAW_HOME/cron/*.json` | Scheduled task definitions |
| `DATA.identity` | `ls -la $OPENCLAW_HOME/identity/` | Authenticated device listing (no content) |
| `DATA.gateway_err_log` | `tail -200 $OPENCLAW_HOME/logs/gateway.err.log` | Recent gateway errors (redacted) |
| `DATA.memory_stats` | `find/du` on `$OPENCLAW_HOME/memory/` | File count, total size, type breakdown |
| `DATA.heartbeat` | direct read `$OPENCLAW_HOME/workspace/HEARTBEAT.md` | Last heartbeat timestamp + content |
| `DATA.models` | direct read `$OPENCLAW_HOME/agent/models.json` | Model contextWindow, maxTokens per model |
| `DATA.cache` | `openclaw cache stats` | Cache size, history count, index size |
| `DATA.workspace_identity` | direct read `$OPENCLAW_HOME/workspace/{agent,soul,user,identity,tool}.md` | Presence + word count + content depth of 5 identity files |

On any failure: set `DATA.<key> = null`, continue — never abort collection.

---

## Phase 2 — Domain Analysis

For **Full Check**: run all 5 domains in parallel.
For **Targeted**: run only the named domain.

Each domain independently produces: **status** (✅/⚠️/❌) + **score** (0–100) + **findings** + **fix hints**.
Read the corresponding `check_*.md` file for complete scoring tables, edge cases, and output format.
Read **`openclaw_knowledge.md`** for platform defaults (gateway address, latest version, CLI commands).

| # | Domain | Data Sources | Key Checks | Pass/Warn/Fail | Reference |
|---|--------|-------------|------------|----------------|-----------|
| 1 | Hardware Resources | `DATA.env` | Memory, Disk, CPU, Node.js, OS | ≥80 / 60–79 / <60 | `check_hardware.md` |
| 2 | Configuration Health | `DATA.config`, `DATA.health`, `DATA.channels`, `DATA.tools`, `DATA.openclaw_json`, `DATA.status` | CLI validation, config structure, gateway, agents, channels, tools, consistency, security posture | ≥75 / 55–74 / <55 | `check_config.md` |
| 3 | Security Risks | `DATA.security`, `DATA.gateway_err_log`, `DATA.identity`, `DATA.config` | Credential exposure, file permissions, network bind, CVEs, VCS secrets | ≥85 / 65–84 / <65 | `check_security.md` |
| 4 | Skills Completeness | `DATA.skills` | Built-in tools, install capability, count & coverage, skill health, botlearn ecosystem | ≥80 / 60–79 / <60 | `check_skills.md` |
| 5 | Autonomous Intelligence | `DATA.precheck`, `DATA.heartbeat`, `DATA.cron`, `DATA.memory_stats`, `DATA.workspace_audit`, `DATA.doctor_deep`, `DATA.logs`, `DATA.status`, `DATA.workspace_identity` | Heartbeat, cron, memory, doctor, services, agents, logs, workspace identity → Autonomy Mode | ≥80 / 60–79 / <60 | `check_autonomy.md` |

**Common rules:**
- Base score = 100, subtract impacts per check failure
- If data source is null: use fallback score noted in each `check_*.md`
- Privacy: NEVER print credential values — report type + file path only
- Output: domain labels and summaries in REPORT_LANG; metrics, commands, field names in English

---

## Phase 3 — Report Generation

Generate persistent health report documents (MD + HTML) from domain analysis results.
Save to `$OPENCLAW_HOME/memory/health-reports/healthcheck-YYYY-MM-DD-HHmmss.{md,html}`.

Read **`flow_report.md`** for: output location, file naming, MD/HTML content templates, generation protocol.

---

## Phase 4 — Report Analysis

Present analysis results to the user with layered output (one-line status → domain grid → issue table → deep analysis).
Compare with historical reports for trend tracking.

Read **`flow_analysis.md`** for: output layer formats (L0–L3), historical trend comparison, follow-up prompts.
Reference **`fix_cases.md`** for real-world diagnosis patterns and root cause analysis.

---

## Phase 5 — Fix Cycle

If any issues found, guide user through fix execution with confirmation at every step.
Show fix command + rollback command → await confirmation → execute → verify.

**Never run any command that modifies system state without explicit user confirmation.**

Read **`flow_fix.md`** for: safety rules, per-fix protocol, batch mode, scope limits.
Reference **`fix_cases.md`** for proven fix steps, rollback commands, and prevention strategies.

---

## Phase 6 — Fix Summary

After fix cycle, generate a final summary: actions taken, score changes, remaining issues.
Append fix results to the previously generated report files.

Read **`flow_summary.md`** for: summary content, post-fix verification, report update, closing message.

---

## Key Constraints

1. **Scripts First** — Use `scripts/collect-*.sh` for structured data; read files directly for raw content.
2. **Evidence-Based** — Every finding must cite the specific `DATA.<key>.<field>` and its actual value.
3. **Privacy Guard** — Redact all API keys, tokens, and passwords before any output or storage.
4. **Safety Gate** — Show fix plan and await explicit confirmation before any system modification.
5. **Language Rule** — Instructions in this file are in English. All output to the user must be in REPORT_LANG.
