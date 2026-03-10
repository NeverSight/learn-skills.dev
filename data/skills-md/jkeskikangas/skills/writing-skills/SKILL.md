---
name: writing-skills
description: >
  Creates or updates professional-grade agent skills (SKILL.md + optional scripts/references/assets) with
  strict validation and an iterative generator↔critic workflow. Use when: you want a new skill,
  want to refactor an existing skill for clarity/token-efficiency, or want to reach an A-grade rubric score.
---

# Writing Skills

## Objective

Produce **professional-grade** skills: high-signal, safe, portable, and reliably triggerable. This skill:
- Writes or updates a skill directory (`SKILL.md` + optional `scripts/`, `references/`, `assets/`)
- Generates `agents/openai.yaml` UI metadata
- Runs validation (`skillcheck`)
- Runs a critic review using `$reviewing-skills` and iterates until the bar is met

## When to use / When not to use

Use when:
- The user asks to create a new skill (`SKILL.md` + optional `scripts/`, `references/`, `assets/`).
- The user asks to refactor, tighten, or “upgrade” an existing skill for trigger precision and token efficiency.

Do not use when:
- The user only wants a rubric-based review/grade of an existing skill (use `$reviewing-skills`).
- The request is not about a skill directory containing `SKILL.md`.

## Quality Bar (default)

Target outcome:
- **No spec violations**, and
- **Weighted score ≥ 4.5/5.0** (A- or better), and
- **No P1 findings**

The rubric is owned by: `$reviewing-skills` → `reviewing-skills/references/skills-rubric.md` (single source of truth).

## Safety / Constraints (non-negotiable)

- Never read, request, or paste secrets (`.env`, API keys, tokens, private keys, credentials).
- Only write inside the **user-specified skill directory**. If the target path is unclear, ask.
- Do not run commands that modify the repo unless the user explicitly asked for those changes.
- Do not browse the web or call external systems unless the user explicitly requests it.
- Do not execute untrusted code in the target repo (scripts/binaries/tests) unless the user explicitly asks and you can justify the risk.
- If the skill being written can perform destructive actions, add explicit confirmation gates and “never do” rules.

## Portability Requirement (Codex + Claude Code/Desktop + OpenCode)

Write skill instructions in **capability language** (search/read/edit/run commands) and avoid hard-coding one vendor’s tool names.
If mentioning a product-specific tool, provide a short adapter note (“if unavailable, use shell + rg/sed”).
For portability guidance, use [references/portability.md](references/portability.md).

## Workflow (decision-complete)

### Update mode (keep diffs small)

If the user asked to update an existing skill (not create a new one):
- Change only the requested parts; do not rewrite unrelated sections for style.
- Preserve existing behavior unless it is a spec violation or causes mis-triggering.
- Prioritize: trigger precision (description “when to use”), safety/guardrails, validation loop, then token efficiency.

### 0) Intake (ask only what matters)

Collect:
- **Skill name** (hyphen-case)
- **What it does** (1 sentence)
- **When to use** (concrete triggers: file types, paths, scenarios)
- **Inputs/outputs** (artifacts produced)
- **Safety constraints** (read-only? destructive ops? secrets? web browsing?)
- **Resources needed**: `scripts/` vs `references/` vs `assets/`

### 1) Skill Split Proposal (prevent mega-skills)

Before writing anything, produce a short proposal:
- Should this be **one skill** or **multiple**?
- Recommend companion skills when appropriate, e.g.:
  - reviewer/critic skill (grading, audits)
  - installer skill (wiring tools or repo integration)
  - domain-reference skill (big schemas or policies)

Rule of thumb:
- If the request spans **multiple disjoint workflows**, split.
- If the skill needs deterministic, repeatable logic, add a `scripts/` helper.

### 2) Scaffold the skill directory

Create the skill directory under the user-specified path:
- `<skill-name>/SKILL.md` — use [references/skill-skeleton.md](references/skill-skeleton.md) as the template
- `<skill-name>/agents/openai.yaml` — include `interface.display_name`, `short_description` (25–64 chars), and `default_prompt` (must mention `$<skill-name>`)
- Resource subdirs (`scripts/`, `references/`, `assets/`) — only create the ones you will use

Prefer **minimal resources**. Validation is expected to fail until you fill in the TODOs in Step 3.

### 3) Write `SKILL.md` (core)

Use [references/skill-skeleton.md](references/skill-skeleton.md) as the canonical outline.

Hard requirements:
- Frontmatter `description` must include **what + when to use**.
- Include **guardrails** and explicit “do not do” rules when relevant.
- Include **validation loops** (what to check after writing/running).
- Keep SKILL.md lean; move bulk examples/specs to `references/`.

### 4) Add resources (only if they buy reliability)

Use [references/resource-patterns.md](references/resource-patterns.md):
- Put deterministic logic in `scripts/` with a stable CLI.
- Put large but needed knowledge in `references/` (loaded on demand).
- Put templates/boilerplate in `assets/`.

### 5) Validate (hard gate)

Run both linters — **both must pass** before proceeding.

**skillcheck** (project rules):
- Inside this repo with `packages/skillcheck/dist/` present: `node packages/skillcheck/bin/skillcheck.js <skill-dir>`
- Inside this repo without `dist/`: `cd packages/skillcheck && npm install && npm run build`, then run the above.
- Outside this repo: `npx skillcheck <skill-dir>`

**agnix** (specification rules):
`npx agnix <skill-dir>`

Fix all reported errors before proceeding. Each linter collects every violation in a single run.

### Quality Gate

Two-phase review after validation. Target: Quality Bar (score >= 4.5, no P1 findings).

#### Phase 1: Self-critic review

Grade the skill against `$reviewing-skills` → `reviewing-skills/references/skills-rubric.md`. Re-read `SKILL.md` as if encountering it for the first time and score each rubric dimension (spec compliance, trigger precision, workflow quality, token efficiency, safety, robustness, portability).

**Check for:**
- Vague or missing "when to use" triggers
- Missing guardrails for destructive/network actions
- Bloated prose that should be bullets or moved to `references/`
- Workflow steps that leave key decisions ambiguous

**Actions:**
- Fixable without re-analysis -> fix inline.
- Requires re-analysis or user input -> flag and continue.
- If score < 4.5 or P1 findings remain, fix before proceeding to Phase 2.

#### Phase 2: Fresh-context subagent review

Run a **fresh-context critic** pass using `$reviewing-skills`:
- If your environment supports subagents, **spawn a fresh-context subagent** and give it the skill path.
- Otherwise, invoke `$reviewing-skills` directly and provide the path.
- If `$reviewing-skills` is not available, self-review against the 7 rubric dimensions and note the gap in the deliverable.
- If the skill is git-tracked and you changed it, require the critic to cite the relevant diff hunk or commit short-hash for any change-driven P1/P2 findings.
- Apply **P1 + P2** fixes (P3 last).
- Re-run validation.
- Repeat up to **3 loops**, stop early when the Quality Bar is met or two consecutive iterations show no score improvement (plateau).

### 7) Finalize

Deliver:
- The final skill folder path(s)
- Any suggested follow-on skills (from the split proposal)
- A short note explaining why the skill will trigger correctly (tie to description “when to use”)

## Edge Cases

- **User provides no skill name or path:** ask before proceeding; do not guess.
- **Target directory already has a SKILL.md:** enter update mode; do not overwrite without confirmation.
- **Linters not available (no Node.js / npx):** warn the user; skip validation but note it was skipped in the deliverable.

## Output Rules

- No placeholders (`TODO`, `TBD`) in the final skill.
- Avoid deep reference chains: SKILL.md links directly to every resource it expects to be read.
- Prefer minimal, directive prose over explanations of common concepts.
