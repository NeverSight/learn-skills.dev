---
name: confluent-skill-reviewer
description: Review a Confluent agent skill in this repo against the Agent Skills spec (agentskills.io), Confluent conventions in CLAUDE.md, the PR template gates, and the evals-as-contract rule. Use this skill whenever the user asks to review, audit, validate, or lint a skill; opens or inspects a PR that adds or modifies anything under `skills/`; asks about spec conformance, lazy-loading, frontmatter shape, trigger overlap, or eval coverage; or wants a pre-merge sanity check on skill changes. Do NOT trigger for general code review of application code; security review; auditing schemas, producer/consumer configs, PII tagging, or Terraform generation for Schema Registry (handled by `kafka-schema-registry`); runtime/log analysis of skill behavior (use `tools/skill_review_dashboard.py`); or any changes that don't touch the `skills/` tree.
metadata:
  author: confluent
  version: "1.1.0"
  last_updated: "2026-07-09"
---

# confluent-skill-reviewer — audit a Confluent agent skill

Three bars every skill in this repo must clear:

1. **Agent Skills spec** — frontmatter shape, naming rules, directory layout, token budgets (https://agentskills.io/specification).
2. **Confluent conventions** — lazy-loaded references, anti-trigger clauses, mode-table branching, ≥90% evals, SME + DTX/DevRel sign-off (`CLAUDE.md`, `.github/pull_request_template.md`).
3. **Evals-as-contract** — `evals/evals.json` with specific, verifiable expectations; fixtures kept in sync.

This skill walks an agent through a structured audit and returns a single Markdown report. It is **read-only** by default — never modifies the skill under review.

## Pre-flight gates

Before producing any findings, confirm all three out loud (briefly):

1. **Scope**: which mode are you in? See [Mode Detection](#mode-detection). If unclear, ask the user once.
2. **Target paths exist**: list the `skills/<name>/` directories you will audit. Stop if none.
3. **Tool availability**: run `bash skills/confluent-skill-reviewer/scripts/run_skill_validator.sh --probe` (from the repo root) to check whether the external `skill-validator` binary is installed. If absent, note it in the report and continue with native checks — do not block.

Skipping these gates is the most common source of bad reviews. The point is to be *explicit* about scope so the user can redirect early.

## Mode detection

| User intent / signal | Mode | What to do |
|---|---|---|
| "review this PR", "audit my branch", branch has uncommitted changes under `skills/`, a PR number is named | **PR-diff** | `git diff main...HEAD -- skills/` or `gh pr diff <N>`; review only changed skills; run **all five phases**, including [Phase E](#phase-e--pr-template-gates-pr-diff-mode-only) |
| "review `skills/<name>`", a single skill path is named, or you're invoked from inside a single skill dir | **Single-skill** | Audit one skill end-to-end; run phases A–D |
| "review all skills", no scope given | **Repo-wide** | Iterate `skills/*/`, run phases A–D per skill, aggregate findings by severity |

If you cannot tell, ask the user once: *"Are you reviewing a PR diff, a single skill, or the whole repo?"* Then proceed.

## Check phases

Run phases in order. Each phase reads its reference only if a finding fires. Collect findings into one in-memory list with severity tags:

- **Blocking** — violates the spec, CLAUDE.md, or a PR-template gate. Must fix before merge.
- **Warning** — violates a convention but won't break tooling; reviewer judgment.
- **Nit** — style/clarity, no functional impact.

### Phase A — Structural & spec conformance

Run `bash skills/confluent-skill-reviewer/scripts/run_skill_validator.sh <skill-path>` (from the repo root). Three outcomes:

- Binary installed → script emits `skill-validator`'s JSON. Parse `results[].level == "error"` into **Blocking**, `"warning"` into **Warning**. Map each finding's `file` and `line` into the report.
- Binary missing → script exits 0 with an install hint on stderr. Note "skill-validator not installed, skipping spec checks" as a **Warning** in the report and do the spec checks natively (read `references/spec-conformance.md` for the rule list and walk through them).
- Binary present but the skill is multi-skill (path lacks `SKILL.md`) → script falls through to the per-skill JSON; treat each entry independently.

Then, regardless of validator state, native checks that the validator does *not* cover well in this repo:
- The skill's directory name matches the `name:` frontmatter field exactly.
- `evals/` is not flagged as orphan (this repo expects evals; pass `--allow-dirs=evals` if invoking the validator directly).

Read `references/spec-conformance.md` only when interpreting an unfamiliar finding code.

### Phase B — Confluent conventions

Inspect the SKILL.md against rules in `CLAUDE.md` § Skill anatomy and § Evals are the contract. The high-leverage checks:

1. **Lazy-loading**: does the SKILL.md inline the contents of any file under `references/`? Grep for headings that also appear in references and for long fenced code blocks that duplicate reference material. Inlined reference content is **Blocking**.
2. **Anti-trigger clause**: does the `description:` contain a `Do NOT trigger for…` clause? Absence is **Blocking** when neighbor descriptions share keywords (Phase C confirms); otherwise **Warning**.
3. **Mode-table branching**: if SKILL.md exceeds ~200 lines or covers more than one distinct workflow (e.g. build *and* debug), expect a mode-detection table near the top. Absence is **Warning**.
4. **Reference depth**: references nested more than one level below the skill root are **Blocking** (the spec restricts this).
5. **Provenance metadata**: skills authored in this repo declare `metadata.author: confluent`, `metadata.version` (semver), and `metadata.last_updated` (YYYY-MM-DD). Missing fields are a **Warning**. A `compatibility` field is expected when the skill requires specific packages, CLI tools, or environment access — absence on a skill that obviously has env requirements is a **Nit**.
6. **Platform scoping**: if the `name` contains a platform token (`confluent-cloud-*`, `confluent-platform-*`, `warpstream-*`, `apache-kafka-*`), the body must scope its instructions to that platform — **Blocking** if it generically covers all platforms. Conversely, if the `name` lacks a platform token but the body performs platform-divergent operations (Cloud API keys, WarpStream object-storage config, on-prem SASL), expect a platform-detection step *and* per-platform reference files (`references/confluent-cloud.md`, `references/warpstream.md`, etc.). Missing either is a **Warning**.
7. **Plan-before-execute**: skills that create, modify, or delete resources (Kafka topics, schemas, Flink statements, connectors, Terraform state) must include an explicit "present the plan, wait for user confirmation" step before any resource-modifying call. Absence in a CRUD-capable skill is **Blocking**.
8. **Credential handling**: skills that read credentials must not `cat`, `Read`, `head`, or `grep` a `.env` file directly — they should reference variables by name (`$BOOTSTRAP_SERVERS`) and verify presence with `test -n "$VAR"`. SKILL.md or bundled scripts that read `.env` contents are **Blocking**. A credential-consuming skill with no guardrail language at all is a **Warning**.
9. **Synthetic data only**: run `python3 skills/confluent-skill-reviewer/scripts/scan_pii.py <skill-path>` (from the repo root) to catch real customer data or secrets committed into the skill — SKILL.md, `references/`, eval prompts, on-disk fixtures, and bundled scripts must use *synthetic* data only. The script emits JSON; map each finding into the report. `severity: "blocking"` (US SSN, Luhn-valid payment card, AWS key id, private-key block) → **Blocking**; `severity: "warning"` (email on a non-example domain, phone number) → **Warning**. CI runs the same scanner over `skills/`, so a clean run here mirrors the gate.

Read `references/confluent-conventions.md` for the full rule list and PR-template gates.

### Phase C — Trigger overlap

Run `python3 skills/confluent-skill-reviewer/scripts/check_trigger_overlap.py <root>` (from the repo root). The script accepts either a repo root (it scans `<root>/skills/*/SKILL.md`) or a "skills root" directory (scans `<root>/*/SKILL.md`) — use the latter for `evals/mock-skills/` runs. It parses each SKILL.md frontmatter, tokenises the `description:` field (filtering stopwords and domain-broad terms like `confluent`, `kafka`, `schema`, `producer`, `consumer`, `topic`, `stream`), and reports keyword collisions. For each collision:

- ≥3 overlapping non-broad keywords (e.g. "topology", "rebalancing", "windowing") with no mutual anti-triggers naming each other → **Blocking**.
- 2 overlapping non-broad keywords without mutual anti-triggers → **Warning**.
- Single non-broad keyword overlap → **Nit**.
- Overlap entirely on filtered domain-broad terms → script silently passes (these are coincidence, not collisions).

Read `references/trigger-overlap.md` only when proposing the wording of an anti-trigger fix — it has worked examples drawn from this repo's existing skills.

### Phase D — Evals contract

Run `python3 skills/confluent-skill-reviewer/scripts/check_eval_schema.py <skill-path>/evals/evals.json` (from the repo root). The script validates:

- Top-level `skill_name` (string) and `evals` (array) keys present.
- Each eval has `id`, `prompt`, `expected_output`, `files`, and its checks under the `assertions` key. The repo standardized on one shape: **`assertions` holding a list of strings**. Two deviations are now **Blocking** — the legacy `expectations` key (must be renamed to `assertions`) and object-form entries `[{id, type, description, …}]` (must be flattened to strings).
- `prompt` is realistic user phrasing, not abstract (heuristic: ≥40 chars, not just "Build me an X"). Short prompts are a **Warning**.
- `assertions[]` are specific (heuristic: contain a verb, a noun, and at least one concrete identifier — file path, class name, config key, or "NOT" clause). Vague assertions are a **Warning**; cite `CLAUDE.md` § Evals are the contract: "expectations encode hard-won correctness — treat them as regression tests, not aspirations".

Cross-check fixture sync: each entry in `files: [...]` is either an on-disk path (relative to the skill root — must resolve when the skill has an `evals/mock-repos/` or `evals/mock-skills/` directory; missing fixtures are **Blocking**) or an inline fixture object `{path, content}` that carries the file body in the eval itself (not resolved on disk).

Read `references/evals-contract.md` for the JSON schema, both expectation shapes, and worked examples of weak vs strong expectations.

### Phase E — PR template gates (PR-diff mode only)

Skip in single-skill and repo-wide modes.

Read `.github/pull_request_template.md` once for the live checklist. For the current PR, verify each item:

| PR-template gate | How to check |
|---|---|
| Docs updated to reflect new skill | `git diff main...HEAD -- README.md docs/`; flag **Blocking** if a skill was added but README's skill table was not touched |
| Evals pass at 90%+ threshold | Look for eval-run output in CI logs or PR comments; if absent, request the author paste the score — **Blocking** until confirmed |
| SME reviewer identified | `gh pr view --json reviewRequests,assignees` — at least one SME on the relevant domain (Kafka Streams, Schema Registry, etc.); **Blocking** if missing for a *new* skill |
| DTX/DevRel reviewer assigned | Same call — at least one reviewer from `@confluentinc/dtx` or `@confluentinc/developer-advocates`; **Blocking** if missing |

Read `references/confluent-conventions.md` § PR template if the gate wording in the live template has drifted.

## Report format

Emit one Markdown report. Group findings by severity, not by phase — reviewers scan top-down:

```markdown
# Skill review: <skill name or PR title>

**Mode:** PR-diff | Single-skill | Repo-wide
**Validator:** installed (v1.5.6) | not installed (spec checks done natively)
**Scope:** <list of skills audited>

## Blocking (N)

- `skills/<name>/SKILL.md:14` — Inlined contents of `references/build-templates.md` into the SKILL.md body. CLAUDE.md § Skill anatomy (lazy-load references bullet) requires lazy-loaded references. Move the content back and route to it from a decision point.
- `skills/<name>/evals/evals.json:42` — Eval id 3 references `evals/mock-repos/missing/` which does not exist on disk. Add the fixture or update the path.

## PR-template checklist (PR-diff mode only)

- [x] Docs updated
- [ ] Evals at 90%+ — author has not pasted score
- [x] SME reviewer assigned (@alice)
- [ ] DTX/DevRel reviewer — none assigned

## Summary

Recommend: **request changes** | **approve with nits** | **approve**.
```

If there are zero Blocking and zero Warning findings, the recommendation is **approve**. One or more Blocking → **request changes**.

## What this skill does NOT do

- Does not edit the skill under review. Findings only.
- Does not run the skill's own evals (the harness lives in `~/.claude/skills/skill-creator/`; the agent should invoke it separately if they want a 90% score).
- Does not analyze runtime/log behavior — that's `tools/skill_review_dashboard.py`.
- Does not review files outside `skills/` (the build system, `Makefile`, `service.yml`, and `.claude-plugin/` are out of scope; flag those for a human reviewer if changed).
