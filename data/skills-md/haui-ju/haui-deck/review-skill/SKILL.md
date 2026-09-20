---
name: review-skill
description: >-
  Hostile audit of haui-deck Agent Skills against Agent Skills spec, Anthropic
  authoring practices, Cursor slash conventions, and repo AGENTS.md. Scores
  structure, triggering, progressive disclosure, token waste, responsibility
  splits, install footprint, and suit patterns. Use when the user runs
  /review-skill, asks to review/audit/lint a skill, or before merging skill PRs.
disable-model-invocation: true
---

# Review skill

Hostile reviewer. Prefer FAIL over soft PASS. Do not praise. Do not edit unless asked.

## Load order (token discipline)

1. Read repo [`AGENTS.md`](../../../AGENTS.md).
2. Inventory target skill dir (files only; do not dump unrelated suits).
3. Read target `SKILL.md` fully.
4. Read [references/checklist.md](references/checklist.md) and apply every row.
5. Open other refs **only if needed**:
   - [references/standards.md](references/standards.md) — external standards summary
   - [references/anti-patterns.md](references/anti-patterns.md) — failure modes
   - [references/haui-deck.md](references/haui-deck.md) — this repo’s layout rules
6. Read `scripts/`, `references/`, `assets/` in the target only when checklist items require them.

Do not load this skill’s entire `references/` tree up front.

## Targets

- User-named skill path, or
- All skills under `suit/**/SKILL.md` (including `suit/meta/`), excluding `.agents/` installs.

## Stance

- Question existence: would a strict one-job policy still keep this skill?
- Question every SKILL.md line: paid on every invocation — is it worth it?
- Question install footprint: would `npx skills add` ship tests or maintainer junk?
- Question init vs action: bootstrap belongs in init skills, not make-* skills.
- Prefer scripts for fragile FS/config; prefer short prose for decisions.

## Report format (required)

```markdown
## Verdict
PASS | FAIL

## Scorecard
| Area | Result | Notes |
|------|--------|-------|
| Spec / frontmatter | PASS/FAIL | |
| Triggering / description | PASS/FAIL | |
| Progressive disclosure | PASS/FAIL | |
| Token economy | PASS/FAIL | |
| Responsibility split | PASS/FAIL | |
| Install footprint | PASS/FAIL | |
| Repo / suit layout | PASS/FAIL | |
| Docs sync | PASS/FAIL | |

## Findings
### Critical
- path: issue — fix

### Warning
- …

### Nit
- …

## Challenge questions
- …
```

**FAIL** if any Critical finding exists or any Scorecard area is FAIL.
Report only; do not modify files unless the user explicitly requests fixes.
