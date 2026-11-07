---
name: skill-security-review
description: Assess ANY agent skill (Claude Code / Cursor / Copilot / plugin skill, marketplace or bespoke, local or cloned) as a senior security and AI architect and produce a standardized, risk-rated assessment. Covers BOTH execution surfaces - the agent-execution surface (SKILL.md instructions and the scripts the agent invokes - prompt injection, tool poisoning, memory-file poisoning) AND the developer-execution surface (bundled test files, git hooks, and npm/pip lifecycle scripts that auto-run on npm test / git commit / npm install, outside the agent, with the developer's own permissions - a surface skill scanners now mostly cover, except a write to persistent agent memory). Use when someone asks to review, assess, vet, audit, or risk-rate an agent skill, asks is it safe to install skill X, mentions a malicious skill, a test-file or git-hook payload, memory poisoning, or a rug pull in a skill, or wants a skill risk report; covers first-time and re-assessments. Do NOT use to build or modify skills.
---

# Skill Security Review

Assess any agent skill the way a senior security and AI architect would, and deliver a compact, standardized
report a decision-maker can act on — a marketplace skill, a cloned repo, or one authored last sprint. The report
format is fixed, so assessments stay comparable across skills and capturable into a register later.

Core stance: **an agent skill is code with TWO execution surfaces, and most reviewers only look at one.**

- The **agent-execution surface** — `SKILL.md` and the scripts the agent invokes — runs inside the model's
  context (prompt injection, tool poisoning, memory-file poisoning) and under the agent's tools.
- The **developer-execution surface** — bundled test files, git hooks, and `npm`/`pip` lifecycle scripts — is
  auto-run by the *developer's toolchain* on `npm test` / `git commit` / `npm install`, **outside the agent, with
  the developer's own permissions.** A skill can ship a clean `SKILL.md` and a bundled payload that scanners flag
  only *advisorily* (they report it but exit 0, never failing the build) and still steal SSH keys the moment
  someone runs the project's tests (the "Gecko" vector). **Assess both surfaces, or you have assessed nothing.**

This skill is the assessor-side methodology; the [`skill-auditor`](https://github.com/garymike/security-agents)
Tier-2 agent wires the tools that execute it, and the Tier-1 `skill-testfile-gate`
([security-workflows](https://github.com/garymike/security-workflows)) is the static pre-filter it escalates from.

## Workflow

### 1. Identify and gather

Establish exactly what is being assessed. Collect (search the web, marketplaces, and repos as needed; ask the
requester only for what you cannot find):

- Name, author/publisher, source links (GitHub / marketplace / plugin), exact version or commit.
- Release and maintenance signals: last update, cadence, maintainer count, stars-vs-age, issue responsiveness.
- **The full bundled surface — not just `SKILL.md`.** Enumerate everything the folder ships, because install copies
  the *whole directory*: `SKILL.md`, `references/`, `scripts/`, **`*.test.*` / `*.spec.*` / `conftest.py` /
  `__tests__/`**, **`.husky/` and `.git/hooks/`**, **`package.json` lifecycle scripts** (`preinstall`,
  `postinstall`, `prepare`), `.claude/commands/`, and any symlinks. `references/inspection-checklist.md` has the
  authoritative location list (personal, project, plugin, nested `**/.claude/skills/`, `--add-dir`).
- Install/trigger reality: user-invoked vs model-invoked, how it is installed (`npx skills add`, marketplace,
  manual clone), and what auto-runs on install or on the developer's next `npm test` / `git commit`.

**Choose your review mode(s) from `references/review-methods.md` by the access you have:** a repo/marketplace link
(source review), an installed copy (local review), or a running detonation (sandbox review). The modes are
complementary — each is blind to what the others catch — so reconcile them, and a repo-vs-published divergence is
itself a finding. Given a link, clone at a pinned commit (record the SHA — the point-in-time anchor). Record which
modes and scanners you actually ran; coverage bounds what your findings can claim, and any gap is a stated
limitation, not a silent skip.

Assign assessment depth from `references/risk-tiering.md`: a docs-only, no-script skill gets a fast pass; anything
that ships scripts, tests, hooks, lifecycle scripts, or writes agent memory gets the full inspection.

### 2. Inspect

Work `references/inspection-checklist.md` at the assigned depth, across **both surfaces**:

- **Part A — Provenance & integrity.** Author↔repo↔published match, marketplace typosquats, dependency scan of any
  bundled `package.json`/`requirements.txt`, incident history. Hash the skill definition set
  (`scripts/hash_skill_definitions.py`) — the anchor for rug-pull re-review.
- **Part B — Agent-execution surface.** `SKILL.md` and agent-invoked scripts as an injection surface: prompt
  injection and tool poisoning in the instructions, **invisible-Unicode / bidi hidden instructions**, and
  **memory-file poisoning** (`MEMORY.md` / `SOUL.md` / `CLAUDE.md` writes that persist across sessions). Run
  SkillSpector (or equivalent) plus a human read of the whole `SKILL.md`.
- **Part C — Developer-execution surface (the surface others miss).** The auto-executed files: test files, git
  hooks, and lifecycle scripts. Run the `skill-testfile-gate` (presence inventory + Semgrep malice pack). **On this
  surface, credential-file access (`~/.ssh`, `.aws/credentials`, `.env`), outbound exfil, `curl|bash` /
  decode-and-exec, reverse shells, or a package runner (`npx`/`uvx`) fetching remote code are automatic Critical
  findings** — they run with the developer's permissions, outside every agent guardrail.
- **Part D — Dynamic confirmation.** Static rules are evadable (SkillCloak-style packing bypasses >90% of
  scanners), so **detonate the flagged files** in an egress-gated, credential-free sandbox and observe: filesystem
  writes, outbound network *attempts* (blocked = the signal), subprocesses, dynamic-code use. This is the
  static→dynamic escalation the `skill-auditor` agent runs; opaque/packed artifacts get detonated even with a clean
  static pass.

### 3. Assess composition (when install context is known)

If the skill will join a real setup, run the skill-level composition risks: **memory poisoning that steers *other*
skills**, command/skill shadowing (a skill overriding a trusted `.claude/commands/` name), and the lethal trifecta
across the installed skill set (private-data access + untrusted content + exfil). Assessing in the abstract, state
the preconditions instead ("completes the trifecta for any workspace that also holds cloud credentials").

### 4. Compute risk and produce the report

Score per `references/risk-scoring.md` (factor-based; any developer-execution-surface Critical overrides to a
blocking verdict), then produce the report **data-first**: author a schema-valid `assessment.json`
(`schema/assessment.schema.json`) and render it per `references/report-template.md`.

- **Author the data, not prose.** The `assessment.json` IS the machine-readable record a register captures — it
  holds the risk state and the point-in-time definition hash. Hand-formatting a report is a regression.
- **Findings lead.** Verdict-first summary (overall rating, severity counts, top findings), recommendations next,
  detail below. Any developer-execution Critical (credential access, exfil, reverse shell, obfuscated payload)
  surfaces in that summary — that is the whole point of this skill.
- **Every field gets a value or an explicit "unknown, because …";** security-relevant unknowns raise the score,
  never lower it. Which surfaces you actually inspected is recorded — an un-run gate is a stated limitation.

### 5. Optional: decision and lifecycle layer

If this supports an install decision (approved by someone other than the requester), record the pinned commit and
the definition hash, then set monitoring: **definition-hash rug-pull detection** (a skill that mutates its scripts
or hooks after approval re-triggers review), re-review on any bundled-file change, and offboarding. Always record
the hash — it anchors every re-assessment.

## Reference files

| File | Read when |
|---|---|
| `references/review-methods.md` | Step 1, how to ingest a skill (repo, marketplace, local copy) + the manual fallback for each missing scanner |
| `references/risk-tiering.md` | Step 1, sets depth; contains automatic disqualifiers |
| `references/inspection-checklist.md` | Step 2, the two-surface checklist + the authoritative skill-location list |
| `references/risk-scoring.md` | Step 4, the computed-risk model (developer-execution criticals override) |
| `references/report-template.md` | Step 4, the report pipeline and authoring rules |
| `schema/assessment.schema.json` | Step 4, the field-by-field contract for `assessment.json` |

## Scripts

- `scripts/hash_skill_definitions.py` — deterministic SHA-256 over a skill's bundled surface (`SKILL.md` + scripts
  + tests + hooks + lifecycle scripts). Use it in Part A and in monitoring so the recorded hash is reproducible on
  re-review and a post-approval mutation (rug pull) is detectable. Stdlib-only; the canonicalization is pinned in
  the script.

## Standards alignment and sources

The checklist and scoring cover both surfaces against the field's evidence base:

- **Agent-execution surface:** *Agent Skills in the Wild* (arXiv 2601.10338 — 26.1% of skills vulnerable, and
  bundled-script skills 2.12× more likely), *Cloak and Detonate* (arXiv 2607.02357 — static scanners are evadable,
  dynamic detonation is load-bearing), Snyk *ToxicSkills* (memory-file poisoning, curl|bash, base64-eval), NVIDIA
  **SkillSpector**.
- **Developer-execution surface:** the **Gecko / VentureBeat** test-file vector (`npx skills add` copies the whole
  directory; test runners + hooks auto-run). **What to expect a scanner to have caught here, re-measured on
  SkillSpector v2.13.0:** it blocks the test-file carrier (64/100), the git-hook carrier (76/100) and auto-run
  agent config (100/100 for `.claude/`, 51/100 for `.cursor/` + `.vscode/`). So a clean SkillSpector run on those
  carriers is real evidence, not a non-answer. The exception is a **write to persistent agent memory**
  (`MEMORY.md`, `CLAUDE.md`, `AGENTS.md`): that scores **0/100 `SAFE`, "no security issues detected"** at
  `Coverage 100.0%`. Only the written bytes are matched against injection patterns, so an inert or
  runtime-assembled payload scores 0 and a literal injection string reaches just 35/100 — neither blocks. Read
  memory writes yourself; do not infer anything from a clean scan there. Also unmatched: `.vscode/tasks.json`
  with `runOn: folderOpen` + `reveal: silent` yields zero findings. Live numbers:
  [`gate-proof.sh`](https://github.com/garymike/security-workflows/blob/main/tests/gate-proof.sh).
  Also: Datadog Security Labs (a cloned repo introduces skills without explicit install → re-review on pull),
  Koi Security **ClawHavoc** (341 malicious skills → SSH/keychain/crypto exfil).

Canonical citations live in
[security-workflows `docs/references.md`](https://github.com/garymike/security-workflows/blob/main/docs/references.md).
When any source adds an attack class, fold it into the checklist as a concrete item and re-validate this mapping.

## Relationship to the platform

- **`skill-testfile-gate`** (Tier-1, security-workflows) is the static pre-filter — presence inventory + Semgrep
  malice pack over the developer-execution surface. This skill *interprets and escalates* its findings.
- **`skill-auditor`** (Tier-2, security-agents) is the agent that *runs* this methodology: static triage on both
  surfaces, then sandbox detonation of the flagged files. This skill is its brains.
- **`mcp-security-review`** is the sibling for MCP servers; keep the shared discipline (data-first report,
  definition-hash monitoring, factor-based scoring, `hash_*` script canonicalization) in sync across both.

## Maintaining this skill

- **After any revision:** re-run the `evals/evals.json` prompts and grade against their assertions before
  redistributing.
- **Quarterly:** re-check the sources above; fold new attack classes into the checklist as concrete items, not
  prose, and re-validate the standards mapping.
- **Keep in sync with `mcp-security-review`:** the report/data-first discipline, the risk-scoring shape, and the
  `hash_*` canonicalization approach are shared; a change to the shared discipline is a paired change.
