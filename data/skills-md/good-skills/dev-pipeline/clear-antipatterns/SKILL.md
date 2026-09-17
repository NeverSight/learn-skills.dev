---
name: clear-antipatterns
description: >-
  Production-grade conservative TS anti-pattern remediation.
  /clear-antipatterns [scope] [pattern]. Candidates require contextual confirmation.
disable-model-invocation: true
version: 2.2.2
---

# Clear Anti-Patterns

`/clear-antipatterns` → activate. Detection: [detection.md](detection.md) (**load at Scan**). Tokens: [../shared/token-efficiency.md](../shared/token-efficiency.md).

**Principle:** Regex/grep/awk/find/hashes are **discovery only** — they MUST NOT alone justify a code change. Optimize for **justified, minimal, behavior-preserving** improvements. Modify code only when anti-pattern is **confirmed** and remediation has clear engineering benefit.

## Args

| Form | Behavior |
|------|----------|
| `[scope] [pattern]` | Path (dir or `.ts`/`.tsx`) + optional pattern (`1`–`10`, name) |
| `[pattern]` only | Auto scope when arg is not a path |
| (none) | Auto scope; patterns **1–10 sequentially** — #2, #5 manual-only (no auto-scan) |

Pattern **8** has sub-candidates: **8a** hard-coded config, **8b** potential secret — still pattern `8` for invocation.

**Path** = `/`, `.ts`/`.tsx`, or `.` / `..`. Else → pattern.

## Resolve — scope & package boundaries

**tsconfig selection** (conservative; note ambiguity in report):

1. Scope inside a package → nearest package/project `tsconfig.json`
2. Honor `references` / project boundaries when present
3. Root `tsconfig` only when no package-specific config applies
4. Do not use `tsconfig.build.json` or tooling-only configs as source scope without evidence

**Monorepo:** identify root vs package `tsconfig`, references, workspace deps. For exports, unused code, public types, shared utils, cross-package imports — check usage **outside** current package.

**Public/library packages:** exports are externally consumable unless repo evidence proves the API is private/internal. In-package non-reference ≠ dead code (#3 Lava Flow).

**Scope fallback:** user path → package `tsconfig` dir → `src/`/`lib/`/`app/`/`packages/*/src` → repo root. File scope = that file only.

## Inspection vs modification scope

**Inspection scope** may be broader than **modification scope**. Read wider context (e.g. cross-package usage) when needed for correctness. **Modification touch set** stays minimal — only paths required by confirmed findings.

## Finding lifecycle

```text
candidate → inspected → confirmed ──→ rejected
                          ↓
                    fixed | accepted | blocked
```

| Status | Meaning |
|--------|---------|
| `candidate` | Detection output only — **no risk classification** |
| `inspected` | Context read; decision not final |
| `confirmed` | Verified — risk assigned here |
| `rejected` | False positive or intentional |
| `fixed` | Remediated and verified |
| `accepted` | Retained — **reason required** |
| `blocked` | Cannot safely execute — **blocker required** |

**Confirmed metadata:** Pattern, File, Location, Evidence, Risk, Decision, Action, Verification.

## Evidence

Observed / Inferred / Assumption / Unknown — on conflict: repo evidence → preserve behavior → reassess.

## Secrets & redaction

Never echo/`cat`/print secrets in output, reports, remediation files, patches, or logs. Use `<REDACTED>`.

## Risk (confirmed only)

When uncertain → **choose higher**.

| Risk | Execution |
|------|-----------|
| **low** | Auto-fix when confirmed and behavior-preserving |
| **medium** | Execute only when evidence + targeted validation demonstrate behavior preservation |
| **high** | **MUST NOT execute autonomously** — document, propose fix, **stop**, wait for approval |

Low-benefit confirmed → `accepted` (duplication, clarity, correctness, maintainability, conventions, risk reduction — not agent avoidance).

## Workflow

1. **Resolve** — scope, pattern, tsconfig, package boundaries.
2. **Scan** — canonical file list from detection.md → **candidates only** (#2, #5: no auto-scan).
3. **Classify** — dedupe; assign pattern (no risk).
4. **Inspect** — confirm/reject; assign risk; judge benefit (may read beyond touch set).
5. **Plan** — minimal modification touch set; remediation file if threshold met.
6. **Protect** — **pre-execution working tree baseline** (before any edit).
7. **Execute** — per risk policy.
8. **Verify** — narrowest repo-defined validation.
9. **Re-scan** — affected pattern(s) + original modification scope first; expand only if changes affect exports, public/shared types, package boundaries, generated artifacts, or dependency relationships.
10. **Review** — scoped diff + semantic impact + untracked files vs baseline.
11. **Report** — structured format.

### Pattern-by-pattern

Sequential per pattern when all active. **#2, #5 manual-only:** no automatic candidate scan, no autonomous remediation — report only when evidence appears during contextual inspection or user explicitly requests.

### Remediation file

`>15 confirmed` OR `>10 files` → tracking when repo permits. **Metadata only** — never analyze, scan, or treat as anti-pattern target.

## Git baseline (before any edit)

**Pre-execution working tree** is the comparison baseline — not `HEAD` alone.

Record before first edit: `HEAD`, branch, `status -sb`, unstaged/staged `--stat`, scoped diff per touch path, planned touch set.

Protect staged, unstaged, pre-existing untracked. Never reset/revert/discard/overwrite user changes.

**Diff attribution:** post-change vs **pre-execution baseline** (includes user dirty state).

## Change budget

Modification touch set = minimal paths for confirmed findings. Stop if scope grows. No opportunistic refactors.

## Dependencies

Do not add, remove, upgrade, downgrade, replace, or reconfigure dependencies unless explicitly required by a confirmed finding and authorized by the task.

## Tests

Do not modify, weaken, delete, skip, or downgrade tests solely to make validation pass. Test changes allowed only when remediation intentionally changes a covered contract or a focused regression test validates the fix. Never remove an assertion to accommodate a failing implementation.

## Validation

Narrowest **existing** repo command for touch set. Only tooling **already in repository/toolchain**. Report **validation limited** when none exists.

### Validation failure

Remediation-caused → small safe repair or `blocked`. Never fix unrelated failures or overwrite user changes. Pre-existing → preserve; report.

## Behavior-sensitive & TSX

Usually medium/high. TSX: hook order, closures, state, refs, effects, context, memo, forwarded refs, lifecycle. No mechanical JSX extraction.

## Diff & semantic review (required)

```bash
git status --short
git diff --stat
git diff -- <touch-set paths>
git diff --cached -- <touch-set paths>
git ls-files --others --exclude-standard
```

Compare to **pre-execution baseline**. Review new untracked files explicitly (`git diff` omits them). Semantic review for behavior-sensitive changes: call sites, exports, public API, types, async/control-flow.

## Definition of Done

All confirmed → `fixed`/`accepted`/`blocked` with evidence; validation + re-scan done; no unrelated edits; user changes preserved; diff reviewed vs baseline.

## Report format

`## Fixed` · `## Accepted` · `## Rejected` · `## Blocked` · `## Validation` · `## Re-scan` · `## Notes / Assumptions`

## Rules

- `disable-model-invocation: true`; preserve behavior.
- **#2, #5:** manual-only (see Pattern-by-pattern).
- Scan via canonical file discovery only ([detection.md](detection.md)).

## Protected areas

`standard exclusions + observed repo-specific exclusions`. detection.md = canonical file-discovery rule; repo conventions supply additions.

## Out of Scope

Non-TS/TSX, unrelated features, new tools, ESLint config (unless asked), mechanical `any→unknown`, splitting coherent large modules by line count alone.

## Version

When `--version` or `-v` is detected as the only meaningful flag, emit the skill version (from the frontmatter) verbatim and stop. Do not inspect, reason, or generate.

