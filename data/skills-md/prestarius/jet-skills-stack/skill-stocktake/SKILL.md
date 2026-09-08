---
name: skill-stocktake
description: Audit a collection of Claude Code skills for overlap, stale technical references, and name/trigger/scope drift, then recommend keep / improve / update / retire / merge for each. Use whenever the user wants to review, clean up, or take stock of their skills ("audit my skills", "are these overlapping", "stocktake", "which skills are stale"), especially as the collection grows.
context: fork
---

Keep the skill collection sharp: no duplicates, no stale references, no skills that won't trigger.

Pick a mode: **Quick** (only skills changed since the last run / explicitly named) or **Full** (every
skill). For larger sets, evaluate in batches and report progress.

1. **Inventory.** Enumerate the skill files (`skills/*/SKILL.md`, and `~/.claude/skills/` if auditing
   the installed set). For each, extract `name`, `description`, full-vs-stub status, body size, and any
   referenced bundled files (`references/`, `assets/`).
2. **Evaluate each skill against a checklist:**
   - **Overlap** — does its scope substantially duplicate another skill? (Flag the pair.)
   - **Freshness** — does it cite an API, library, version, CLI flag, or price that may have drifted?
     `WebSearch` to confirm; flag anything outdated.
   - **Trigger quality** — is the `description` specific and "pushy" enough to fire, and does the
     name/trigger/scope actually match the body?
   - **Integrity** — do referenced files exist? Are stubs still stubs that should be fleshed out?
3. **Summarize.** A table: skill → verdict → one-line reason. Verdicts:
   **Keep** · **Improve** (tighten body/description) · **Update** (refresh stale facts) ·
   **Retire** (no longer useful) · **Merge into `<skill>`** (resolve an overlap).
4. **Consolidate and confirm.** For every non-Keep verdict, give the concrete justification and the
   proposed change. **Confirm with the user before editing or deleting anything** — never retire or
   merge a skill unprompted (surgical-changes guardrail). This skill runs in a forked subagent:
   report the verdicts and proposed changes back; the main session confirms and applies them.

No telemetry or usage metrics — this audits content quality and correctness, not how often a skill ran.
