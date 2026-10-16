---
name: global-guardrails
description: |
  Design and enforce AI agent guardrails end-to-end: behavioral boundaries
  (content / action / tone / scope / confidence), catastrophic shell command
  denylist across Cursor/Claude/Codex/OpenCode/Pi/Hermes/Droid/Devin,
  Claude Code git PreToolUse hooks, permission allowlists, secret/PII
  protection, prompt-injection & topic filters, sandbox/network isolation,
  agent PR review gates, audit trailers, and team policy.

  Trigger when adding or tuning blocked commands; wiring a new agent or
  machine; installing git push/reset guards; designing product guardrails;
  adding content moderation / PII redaction / injection detection; onboarding
  agents to a team; sandboxing agent runs; requiring human review for
  AI-generated PRs; or when the user says guardrail, command guard,
  PreToolUse, safety filter, agent policy, or deny-dangerous.

  Keywords: guardrails, PreToolUse, beforeShellExecution, denylist,
  dangerous-patterns, git hooks, CLAUDE.md, secrets, PII, prompt injection,
  sandbox, CODEOWNERS, agent-policy, AI-Generated-By, hard block, soft warn
version: 2.0.0
license: Apache-2.0
metadata:
  author: famosapp
  stack: posix-ere-hooks, claude-code, cursor, codex, optional-presidio
  related_skills: git-full, git-worktrees, team-orch, review-security
  primary_output: wired-guard | guardrail-spec | policy-yaml | review-disposition
  sources_synthesized: global-agent-guardrails, git-guardrails-claude-code, guardrail-design, guardrails-safety-filter-builder, ai-coding-agent-guardrails
---

# Global Guardrails

Seatbelts for AI coding agents — **behavioral design + mechanical enforcement**.
Not a sandbox against a determined malicious agent (obfuscation can bypass
regex). Non-negotiables override convenience.

**Announce when activating:** "Using the global-guardrails skill."

## When to load which reference

| Need | Read |
|------|------|
| Hard bans / gates | [non-negotiable.md](references/non-negotiable.md) |
| Product guardrail design (types, UX, severity) | [design.md](references/design.md) |
| Types / layouts / severity tiers | [types-and-layouts.md](references/types-and-layouts.md) |
| Cross-agent catastrophic command denylist | [command-guard.md](references/command-guard.md) |
| Claude Code git PreToolUse install | [git-hooks.md](references/git-hooks.md) |
| CLAUDE.md / allowlists / path ACLs | [permissions.md](references/permissions.md) |
| Secrets, git-secrets, output scanners | [secrets.md](references/secrets.md) |
| PII / injection / topic / output filters | [content-filters.md](references/content-filters.md) |
| Docker / seccomp / network isolation | [sandbox.md](references/sandbox.md) |
| Agent PR CI, branch protection, CODEOWNERS | [review-gates.md](references/review-gates.md) |
| Audit trailers & JSONL logging | [audit.md](references/audit.md) |
| Team agent-policy.yaml | [team-policy.md](references/team-policy.md) |
| Pitfalls | [gotchas.md](references/gotchas.md) |
| DO / DON'T | [do-dont.md](references/do-dont.md) |
| Recipes | [examples.md](references/examples.md) |
| Review checklist | [review-checklist.md](references/review-checklist.md) |

Bundled hooks (canonical — wire agents here, do not copy).
`$SKILLS_ROOT` = absolute path to the skills repo root (contains `global-guardrails/`).

```text
$SKILLS_ROOT/global-guardrails/hooks/deny-dangerous.sh
$SKILLS_ROOT/global-guardrails/hooks/dangerous-patterns.txt
$SKILLS_ROOT/global-guardrails/hooks/test-guard.sh
$SKILLS_ROOT/global-guardrails/scripts/block-dangerous-git.sh
```

Expand to a real absolute path in agent configs (hooks do not expand `$SKILLS_ROOT` / `~`).

---

## Core rules

1. **Design before dump** — every guardrail has what / why / UX / edges / override ([design.md](references/design.md)).
2. **Block irreversible only (command layer)** — data loss, disk wipe, force-push rewrite, repo delete, token exfil. Recoverable local ops stay allowed unless the user chooses a stricter git hook.
3. **One denylist, many adapters** — `global-guardrails/hooks/dangerous-patterns.txt` is source of truth; never fork/copy patterns per agent.
4. **Layers beat silver bullets** — input filter → policy → generate → output validate → human review.
5. **Transparent refusals** — say why; offer safe alternative when possible; escalate when needed.
6. **Secrets never in chat or commits** — scan before commit; redact PII when possible instead of hard-rejecting useful output.
7. **Human owns merge** — agent PRs need review gates; infra/auth/crypto stay human-authored by default.
8. **Test after every pattern change** — `$SKILLS_ROOT/global-guardrails/hooks/test-guard.sh` must end `failed: 0`.
9. **Fail-open vs fail-closed deliberately** — know each agent’s hook semantics (Cursor `failClosed: false`).
10. **Seatbelt ≠ sandbox** — regex hooks miss `python -c "…"`. Use sandbox/network for higher stakes.

---

## Non-negotiable

Full contract: [non-negotiable.md](references/non-negotiable.md).

| Rule | Requirement |
|------|-------------|
| Catastrophic denylist | `rm -rf /|~`, `dd`/`mkfs`, `sudo rm`, fork bomb, `curl\|sh`, `git push -f`, `gh repo delete`, token dump — blocked |
| Pattern format | POSIX ERE; `[[:space:]]` not `\s` in the shared file |
| Test gate | Pattern edits require green `…/global-guardrails/hooks/test-guard.sh` |
| Merge hooks | Never overwrite existing `hooks` JSON — merge entries |
| Absolute paths | Hook commands use skill paths under `…/global-guardrails/hooks|scripts/` (`~` expansion unreliable; no forked copies) |
| No silent secrets | Never commit/read/display `.env*`, `*.pem`, `*.key`, live tokens |
| No main force-push | Agents never `git push --force` to main/master |
| Explicit override | Soft/hard tiers documented; overrides need user/admin confirmation |
| Attribution | Agent commits prefer `AI-Generated-By` trailers when team policy says so |

---

## Gotchas

Summary — [gotchas.md](references/gotchas.md).

- Codex trust hash-pinned — edit hook *entry* → re-trust via `/hooks`.
- Cursor `failClosed: true` bricks background hosts — keep `false`.
- Hermes key is `provides_hooks`; enable plugin non-interactively.
- False positives when dangerous text appears in harmless CLI args.
- Copying hooks to `~/.agents/hooks` causes drift — always wire the skill path.
- Git-guard that blocks *all* `git push` is stricter than global denylist (force only).
- Allowlist-only shells starve useful agents — prefer denylist + path policy.
- Prompt-injection regex is incomplete — layer with policy + human review.
- Sandbox without volume mounts = agent can’t work; over-mount = secrets leak.

---

## Types (“Data Types”)

| Kind | Values |
|------|--------|
| Guardrail type | `content` · `action` · `tone` · `scope` · `confidence` |
| Severity | `hard_block` · `soft_warn` · `nudge` · `escalate` |
| Refusal style | `transparent` · `redirective` · `silent` · `escalate` |
| Layer | `input` · `policy` · `output` · `hook` · `ci` · `human` |
| Disposition | `ALLOW` · `BLOCK` · `REDACT` · `ASK` · `ESCALATE` |
| Scope | `user_global` · `project` · `org` |

Details: [types-and-layouts.md](references/types-and-layouts.md).

---

## Layouts (“Tables / Columns”)

### Guardrail specification

| Column | Content |
|--------|---------|
| Category | content / action / tone / scope / confidence |
| Rule | Specific prevented behavior |
| Rationale | Harm prevented / value protected |
| UX | What user sees (refusal / redirect / escalate) |
| Edge cases | Too strict / too loose greys |
| Override | Admin / confirm / never |

### Mode routing (short)

| Signal | Path |
|--------|------|
| Wire / tune catastrophic commands | [command-guard.md](references/command-guard.md) |
| Block git push/reset in Claude Code | [git-hooks.md](references/git-hooks.md) |
| Design product behavioral boundaries | [design.md](references/design.md) |
| PII / injection / topic filters | [content-filters.md](references/content-filters.md) |
| Team onboarding agents | [permissions.md](references/permissions.md) → [team-policy.md](references/team-policy.md) |
| Agent PR security | [review-gates.md](references/review-gates.md) |

---

## DO and DON'T

| DO | DON'T |
|----|--------|
| Spec each guardrail (what/why/UX) | Invent ad-hoc refusals with no rationale |
| Block irreversible; allow recoverable | Block `git status` / `rm node_modules` by default |
| Run tests after pattern edits | Ship untested regex |
| Merge hook configs | Clobber other hooks |
| Layer defenses + log blocks | Trust one regex for injection/PII |
| Redact PII when possible | Refuse entire answers for one email |
| Require human review on agent PRs | Auto-merge AI code to main |

Complete: [do-dont.md](references/do-dont.md).

---

## Examples

See [examples.md](references/examples.md):

1. Install global command guard on a new machine
2. Add a pattern + tests
3. Project-scoped Claude git guardrails
4. Guardrail specification table (product)
5. Safety filter pipeline sketch
6. Agent PR gate labels + CODEOWNERS

---

## Critical / Recommended / Nits

Full: [review-checklist.md](references/review-checklist.md).

### Critical
Denylist missing; untested patterns; secrets in agent output/commits; force-push main allowed; hooks overwritten; infra/auth changed by agent without human gate; Cursor failClosed true.

### Recommended
Git hook scope asked; Context Brief for product guardrails; audit trailers; dependency changes labeled; sandbox for untrusted autonomy.

### Nits
Refusal copy tone; pattern comment clarity; absolute vs relative hook path docs.

---

## Decision workflow

1. **What layer?** Design (product) vs mechanical (hook/CI) vs both.
2. **Severity?** hard_block / soft_warn / nudge / escalate.
3. **Wire** command guard and/or git hooks; merge configs.
4. **Test** `test-guard.sh` + safe E2E probe (`git push --force` in non-git dir).
5. **Permissions + secrets** for the repo; optional content filters.
6. **Review gates + policy** for team; audit if compliance cares.
7. Document overrides; stop when seatbelt matches risk — don’t over-paternalize.
