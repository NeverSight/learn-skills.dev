---
name: skill-quality-review
description: Review a SKILL.md file for adherence to Anthropic's official agent-skill best practices. Use when the user asks to "review a skill", "check skill quality", "audit skill", "validate skill quality", or before merging a PR that adds or modifies a skill in skills/. Complements the deterministic structural validator (validate_skills.py) by judging content quality — concision, description discoverability, naming, freedom calibration, progressive disclosure.
metadata:
  version: 1.0.0
  author: Leandro Gil
---

# Skill Quality Review

Use this skill to evaluate a SKILL.md file against Anthropic's [agent-skill best practices](references/anthropic-best-practices.md). This is a **content-quality** review — token efficiency, discoverability, calibration. It is NOT a structural validator (the deterministic R1–R7 checks live in `scripts/build/validate_skills.py` and run in CI).

## When to Use

- Reviewing a PR that adds or modifies a `skills/<name>/SKILL.md` file in `mulesoft/mulesoft-dx`.
- Auditing an existing skill that the user suspects is bloated, vague, or hard to trigger.
- Before publishing a new skill to the bundle.

Do NOT use this skill for:
- Pure structural checks (frontmatter present, code fences balanced) — that's `make validate-skills`.
- API-spec reviews — use `api-spec-validator`.
- Generic prose editing — this is specifically about agent-skill ergonomics.

## How to Run

1. **Load references**:
   - `references/anthropic-best-practices.md` (vendored Anthropic doc, ~1100 lines) — generic agent-skill best practices, source of truth for dimensions 1-8.
   - `docs/job-template.md` and `docs/jobs-readme.md` from the repo root — repo-specific JTBD conventions.
   - `skills/skills-metadata.yaml` — declares which skills are `jtbd` vs `prose`. Determines which extra rules apply.
2. **Identify the target skill(s)**: the caller will name a path (e.g. `skills/omni-gateway/install-omni-gateway/SKILL.md`) or a list of paths. If the caller asks to review every skill changed in the current branch, resolve the list with `git diff --name-only <base>... -- 'skills/**/SKILL.md'`.
3. **Determine skill type** by reading `skills-metadata.yaml` (or the parent bundle's): `jtbd` (default) or `prose` (override). The type drives which extra checks apply (see "Type-specific dimensions" below).
4. **Read the full SKILL.md** plus any referenced files (`references/`, `scripts/`) — progressive disclosure means a top-level SKILL.md is only half the picture.
5. **Evaluate against each dimension below**, in order. For each dimension, decide: PASS / WARN / FAIL, with a one-line rationale and a quote from the SKILL.md.
6. **Return the findings to the caller** in the structure shown in "Output Format" below. Do not create or write to any file unless the caller explicitly asks for it — the caller decides whether to display the report, append it to a review document, attach it to a PR comment, or use it to revise a skill in-flight.

## Review Dimensions

For each, cite the exact best-practices section and quote the offending text from SKILL.md. Do not invent rules — if a check isn't grounded in the reference doc, don't include it.

### 1. Concision (Core principles → "Concise is key")
- Is every paragraph earning its tokens? Flag prose that explains things Claude already knows (what a PDF is, what a library is, what HTTP is).
- Is SKILL.md body under ~500 lines? If over, is the overflow content split into `references/` files that load on demand?
- Are there redundant restatements of the same instruction?

### 2. Description quality (Skill structure → "Writing effective descriptions")
- **Third person** — flag any "I can…" or "You can…" or "Use this to…" framings.
- **Specific + trigger-rich** — does the description list both *what* the skill does and *when* to use it (concrete user-phrasings, file types, scenarios)?
- **Length** — under 1024 chars but specific enough that Claude can disambiguate from 100+ other skills.
- **Vague rejects** — "Helps with X", "Manages Y", "Does stuff with Z" → fail.

### 3. Naming (Skill structure → "Naming conventions")
- Lowercase + hyphens + numbers only.
- No reserved words: `anthropic`, `claude`.
- Prefer gerund form (`processing-pdfs`) or noun phrases (`pdf-processing`); flag `helper`, `utils`, `tools`.
- The `name:` field must match the directory.

### 4. Degree-of-freedom calibration (Core principles → "Set appropriate degrees of freedom")
- **Fragile / one-true-path** operations (DB migrations, build commands, exact env setup) should be **low freedom** — exact scripts, "do not modify".
- **Judgment calls** (code review, design decisions) should be **high freedom** — heuristics + criteria, not lockstep steps.
- Flag mismatches: a code-review skill with 17 rigid steps, or a `mvn deploy` skill that says "use whatever flags seem right".

### 5. Progressive disclosure (Skill structure → "Pattern 1/2/3")
- Long reference content (catalogs, error tables, schemas) belongs in `references/foo.md`, loaded on demand.
- Helper logic belongs in `scripts/`, executed not loaded.
- Flag a 1500-line SKILL.md where the bottom 1000 lines are reference material that should have been split.

### 6. Discoverability triggers (Skill structure → "Writing effective descriptions" + "How Skills work")
- Description should contain the **literal terms** a user is likely to type ("validate", "review", "deploy", "Mule", "OAS") so Claude's selector matches.
- If the skill applies to a specific tool/format/file extension, that should appear verbatim.

### 7. Cross-references (skill-bundle pattern in this repo)
- If SKILL.md references other skills by name, those skills must exist in the same bundle (or be marked "coming in vX.Y").
- URLs and file paths inside the skill must resolve.
- Trigger phrases listed in the description should be plausible — not invented.

### 8. Tone consistency (Skill structure → third person)
- Any first-person ("I'll do…") or second-person command framing aimed at the human ("you should…") within instructions block is a red flag — instructions are for Claude.

## Type-specific dimensions

This repo classifies skills as **`jtbd`** (default) or **`prose`** in `skills/skills-metadata.yaml` (or the bundle-level `<bundle>/skills-metadata.yaml`). Apply only the dimensions that match the declared type. Type↔structure coherence (does the content match the type?) is already enforced by R7 of the deterministic validator — flag here only when the AI reading detects subtler drift.

> **Scope reminder:** the deterministic validators (`validate_skills.py`, `validate_jtbd.py`) already enforce structural correctness — step numbering gaps, frontmatter parseability, kebab-case names, bundle metadata, `urn:` resolution, step dependency order, type-vs-structure coherence. **Do not re-check those.** If a finding can be expressed as a regex/AST rule, it belongs in the deterministic layer, not here. Below are only judgment calls.

### JTBD-specific (when `type: jtbd`)
- **Imperative voice in step titles** — "Search Exchange" is correct; "Searching Exchange", "How to search Exchange", "Exchange search" are not. Determinístic check can't tell a verb from a gerund — that's why this is here. Apply the same criteria as `validate-imperative-format` does for API descriptions.
- **`inputs:` / `outputs:` capture the real dependency, not just the obvious ones** — if Step 7's prose says "use the GAV from Step 4", but Step 4 declares no `outputs.gav` and Step 7 declares no `inputs.gav`, the data flow is invisible to the agent. Determinístic checks see the YAML structure but can't read the prose to detect the mismatch.
- **Step prose stays consistent with step numbering after renumbering** — when a PR renumbers steps, internal references like "as in Step 5" or "Step 8 will use this" must point to the *new* step numbers. Determinístic validators don't know what Step 5 *was about*; an LLM does.
- **Phase boundaries are real, not decorative** — if a JTBD declares a "user-approval gate" between phases, the gate must actually mean something (the next step refuses to proceed without explicit user input). Cosmetic phase headings without enforcement are a smell.

### Prose-specific (when `type: prose`)
- **The skill is genuinely prose, not a JTBD wearing a costume** — if a prose skill has 8 sequential `### Step N` headings with bash commands and explicit ordering, it should probably be `type: jtbd`. R7 only flags binary mismatches (has steps / has none); the gradual slippage requires reading.
- **Decision-routing structure exists in bundle-root prose skills** — for a multi-skill bundle (like `omni-gateway/SKILL.md`), the root should route the agent to sub-skills via a decision table or mermaid flowchart. A bundle-root prose skill that's just a paragraph of "this bundle does X, Y, Z" without routing wastes the entry point.
- **Mermaid diagrams render** — confirm fenced as ` ```mermaid ` (not in YAML frontmatter) and that node references match labels. Mermaid in frontmatter is the bug we hit on PR #129.

### Bundle-level (when reviewing a whole bundle, not a single skill)
- **The bundle's `SKILL.md` (root) actually adds value** — if it's just a list of sub-skill names, the agent could discover those from descriptions alone. The root should help disambiguate, route, or set shared context.
- **CHANGELOG entry matches the actual user-visible change** — a CHANGELOG that says "improved error handling" when the diff added a new sub-skill is misleading. R-level validators don't read the CHANGELOG semantically.

## Output Format

Return findings as a markdown block per skill reviewed, using this exact structure. The block goes in the response to the caller; do not write it to a file.

```markdown
### Quality review — `<path/to/SKILL.md>`

**Blocking findings**
- **<short title>** — Best-practice violated: *<section name>*. Quote: "<offending text>". Why it harms the agent: <1 sentence>. Suggested fix: <1 sentence>.

**Should fix**
- (same shape)

**Optional polish**
- (same shape, only if non-trivial)

**Verdict**: Approve / Approve with comments / Request changes
```

When reviewing more than one skill in the same call, emit one such block per skill, in the order they were named.

Keep findings **action-oriented**. A finding like "the prose feels long" is not actionable; "lines 40-90 explain what XML namespaces are — Claude knows. Cut to one line referencing the canonical XSD section" is actionable.

## Anti-Patterns to Avoid in the Review Itself

- **Do not invent rules** beyond `references/anthropic-best-practices.md`. If something feels wrong but doesn't violate a documented principle, don't flag it as a finding — at most note as optional polish with that caveat.
- **Do not nit-pick prose style** (Oxford commas, sentence length). Best-practices doc is about token efficiency and discoverability, not English-teacher polish.
- **Do not over-trigger**. If the SKILL.md is short and clear, just say "Approve — no findings" and move on. Padding the review with weak findings dilutes the strong ones.
- **Cite literally**. Every finding must include a real quote from the SKILL.md and a real section name from the best-practices reference.

## Reference

- [`references/anthropic-best-practices.md`](references/anthropic-best-practices.md) — vendored copy of Anthropic's [official agent-skill best-practices doc](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) (fetched 2026-06-10). Re-fetch with `defuddle parse <url> --md` if Anthropic publishes updates.
- `docs/job-template.md` — repo-canonical JTBD template; new JTBD skills should structurally match it.
- `docs/jobs-readme.md` — guide explaining the JTBD format and its triple purpose (AI skill, doc, executable spec).
- `docs/x-jobs-to-be-done-schema.md` — JTBD schema reference.
- `skills/skills-metadata.yaml` (and per-bundle `<bundle>/skills-metadata.yaml`) — declares `type: jtbd` (default) or `type: prose` per skill. Drives type-specific review dimensions.
- `scripts/build/validate_skills.py` — deterministic R1–R7 structural validator (R1: name↔dir, R2: kebab-case, R3: uniqueness, R4: required metadata, R5: cross-refs, R6: type resolvable, R7: type↔structure). This skill complements those checks; it does not duplicate them.
- `scripts/build/validate_jtbd.py` — deterministic JTBD-format validator (frontmatter, step numbering, YAML step blocks, dependencies). Run before this skill — fix structural errors first.
- `.claude/skills/validate-imperative-format/SKILL.md` — sibling skill that validates API `info.description` imperative voice. Same principle applies to JTBD step titles; reuse its criteria there.
