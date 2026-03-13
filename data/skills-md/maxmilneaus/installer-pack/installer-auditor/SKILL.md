---
name: installer-auditor
version: 1.0.0
description: Validates everything built or installed. Auto-detects type, picks validation tier, self-heals when possible, escalates when not. Activate on coding agent completion, install handoff, config change, or "validate this".
---

# InstallerAuditor

Validates installs. Picks the right test tier, fixes what it can, escalates what it can't.

## Setup

Use directly by reading this skill. Optionally register as a sub-agent:
```
sessions_spawn(agentId: "installer_auditor", task: "Validate: [WHAT]. Method: [METHOD]. Expected: [DESCRIPTION].", label: "installer-auditor")
```

## Triggers
- Coding agent completes
- InstallerTester hands off (Phase 3)
- Multi-file edit or config change
- "validate this", "test this", "does this work"
- `/installer_auditor`, `/build-check`
- Before reporting "done" on non-trivial work

## Input: What, Method, Expected behaviour
## Output: `STATUS: done/retry/escalate` + tier results + checklist

---

## Tier Selection

```
CLI / simple install / config change  → Tier 1: Smoke Test
Skill / MCP server / cron / feature   → Tier 2: Functional
Refactor / system integration          → Tier 3: Integration
```
Default to Tier 2 if unclear.

---

## Tier 1: Smoke Test
1. Exists? (on PATH, at expected location, registered)
2. Runs without errors? (`--help`, `--version`)
3. One real command produces expected output?

Self-heal: one attempt. Obvious fix → re-test. Not obvious → escalate.

## Tier 2: Functional
1. Run Tier 1.
2. List every capability. Test each with real input.
3. Test edge cases: bad input, missing data, empty states.
4. Test the actual use case, not just "does API respond."
5. For workflow skills: simulate primary use case end-to-end, execute each step.

Self-heal: two attempts. Same error twice → escalate.

## Tier 3: Integration
1. Run Tier 1 + 2.
2. Test connections to dependent tools/skills/configs.
3. Regression check: everything working before still works.
4. If replaced something: confirm clean handoff.

Regressions → immediate escalate, no self-heal.

---

## Self-Heal Rules

**Do:** reinstall cleanly, fix config value, fix path/permission, re-register.
**Never:** delete existing tools, modify system files, create workarounds, retry same fix twice, make architectural decisions.

---

## Escalation

**What broke:** one sentence. **What you tried:** what happened.
**Options:** 1. [option] — [why] | 2. [option] — [trade-off] | 3. [option]
**My pick:** [number] — [why]

Immediate escalate (no self-heal): regressions, security concerns, data risk, scope creep.

---

## Structure & Wiring Check

### Location
**OpenClaw-standard:**

| Artifact | Location |
|----------|----------|
| Skills | `~/.openclaw/skills/<name>/SKILL.md` |
| Config | `~/.openclaw/openclaw.json` |
| Knowledge | `~/.openclaw/workspace/` |
| Memory | `~/.openclaw/workspace/memory/YYYY-MM-DD.md` |

**Workspace paths** *(customise for your setup):* docs, scripts, plans.

### Wiring
- MCP server → registered? Shows in `mcporter list`?
- Skill → folder matches `name:` in front matter?
- CLI → in TOOLS.md?
- API keys → stored securely? Wired in config?
- Cron → correct target, model, channel?
- Cross-references → Skill A calls Skill B, path works?

### Completeness
Multi-step workflow skill without a completion checklist → flag and add one.

### Discoverability
Reachable from TOOLS.md, AGENTS.md, skills list, or workspace links. Orphan → add reference.

---

## Slash Command
If channel supports slash commands, suggest one.

---

## Show It Working
Open the thing and do a real test run — not just "is it there."
- Skill → open + trigger with real prompt
- CLI → demo command with real output
- MCP → call with actual data
- Config → show status, confirm behaviour changed
- Cron → show in list, trigger test run

Run it automatically. Not done until there's a live result.

---

## Auto-Log
Write to `~/.openclaw/workspace/memory/YYYY-MM-DD.md`: what, tier, result, self-heal actions.

## Learn From Fixes
Log to `~/.openclaw/workspace/.learnings/SOLUTIONS.md`: what broke, what fixed it, install type.

---

## Completion Checklist

- [ ] Tier tests executed
- [ ] Structure check — location, wiring, discoverability
- [ ] Show it working — live test result
- [ ] Slash command — suggested or skipped
- [ ] Auto-log — written

Unchecked = not done.

## Constraints
- Never report done without checklist complete
- Max 2 fix attempts without checking in
- Never modify system files without permission
- Regressions = immediate escalate
