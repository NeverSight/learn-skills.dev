---
name: installer-tester
version: 1.0.0
description: Pre-install decision gate. Activate on "install X", "add X", "set up X", "should we use X", "compare X to Y", "is X worth installing".
requires:
  - installer-auditor
  - skill-vetter
---

# InstallerTester

No tool gets installed without passing this check.

## Requirements

| Skill | Role | Required? |
|-------|------|-----------|
| `installer-auditor` | Post-install validation | Recommended |
| `skill-vetter` | Security vetting for external skills | Required if installing a skill |

## Triggers
- "install X", "add X", "set up X", "should we use X"
- GitHub/npm/brew link shared
- "is X worth installing", "compare X to Y"
- `/installer_tester`, `/software-check`

---

## Phase 0: Docs & Security

1. Run `openclaw docs "<tool-name>"` (fallback: https://docs.openclaw.ai). Informs Check 3.
2. If target is a skill → activate `skill-vetter`, get ✅ SAFE or ⚠️ CAUTION (with approval) before proceeding. Fallback: manually review SKILL.md for red flags.

---

## Phase 1: Pre-Install Check

Run in order. Stop and report if any check is a clear no.

### Check 1 — What does it do?
State what it does in one sentence. Not what the user thinks — what it *actually* does. Can't determine? Stop.

### Check 2 — What would it enhance or fix?
Search error logs, memory, session history, TOOLS.md, skills for:
- **Friction:** errors, workarounds, slow steps, token waste
- **Enhancement:** faster, cheaper, more reliable, new capability

Neither found → "Shiny toy — skip."

### Check 3 — Already covered?
Check docs results from Phase 0, then:
```bash
mcporter list                                              # optional — requires mcporter
which <toolname> 2>/dev/null || echo "not installed"
openclaw skills list 2>&1 | grep -i "<toolname>"
grep -i "<toolname>" ~/.openclaw/workspace/TOOLS.md
```

Verdict: **Not covered** → Check 4 | **Partially covered** → Check 4 | **Fully covered** → stop, report what covers it.

### Check 4 — Better than what we have?
If overlap: quantify improvement (tokens, speed, reliability, capability).

Health check: last commit, stars, issues, bus factor, dependency count, red flags (archived, abandoned, no docs).

### Decision Output
One summary line:
`Coverage: [not covered/partial/fully covered] | Quality: active/stale/dead | Verdict: Install / Skip / Flag`

Wait for approval.

---

## Phase 2: Install

Follow the tool's install instructions (Homebrew, npm, pip, `claude mcp add`).
- Dependency missing or install fails → stop, report. Don't improvise.
- API keys → platform secure credential system. Never inline.
- Record install method (needed for rollback).

---

## Phase 3: Validation

If InstallerAuditor is a registered agent:
```
sessions_spawn(agentId: "installer_auditor", task: "Validate: [WHAT]. Method: [METHOD]. Expected: [DESCRIPTION].", label: "installer-auditor")
```
Otherwise read the `installer-auditor` skill and follow its tiers directly.

Validation fails → uninstall, report.

---

## Phase 4: Document

Log in TOOLS.md: name, purpose, invocation, priority order. Check OpenClaw docs first for native coverage.

---

## Completion Checklist

- [ ] Phase 0 — docs + vetter (if skill)
- [ ] Check 1 — one-sentence description
- [ ] Check 2 — friction/enhancement or "shiny toy"
- [ ] Check 3 — coverage verdict with real checks
- [ ] Check 4 — health assessed (if not fully covered)
- [ ] Decision — verdict delivered, approval received
- [ ] Phase 2 — installed (method recorded)
- [ ] Phase 3 — validated
- [ ] Phase 4 — documented

Unchecked without a reason = not done.
