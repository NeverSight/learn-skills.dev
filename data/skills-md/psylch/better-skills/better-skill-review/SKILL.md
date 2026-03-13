---
name: better-skill-review
description: "Review an agent skill by combining automated linting with structured semantic analysis. Runs hard-rule validation, evaluates contextual findings, then performs deep review against best practices (description quality, workflow design, runtime robustness, script conventions, UX patterns). Produces actionable improvement suggestions with before/after examples. This skill should be used when reviewing a skill, validating skill structure, improving skill quality, checking skill conventions, or when the user says 'review skill', 'validate skill', 'check skill', 'improve skill', 'iterate on skill', '走查技能', '验证技能', '检查 skill', '改进技能', '优化 skill'."
---

# Skill Review

## Language

**Match user's language**: Respond in the same language the user uses.

## Overview

Review an agent skill through three layers: automated linting (hard rules), contextual finding evaluation (agent judges with context), and structured semantic review (deep analysis against best practices). Optionally fix issues and verify fixes through independent subagent validation.

## Workflow

Progress:
- [ ] Step 1: Identify the skill
- [ ] Step 2: Review (linting + profile + findings + semantic)
- [ ] Step 3: Present findings
- [ ] Step 4: Fix gate
- [ ] Step 5: Verify & iterate

### Step 1: Identify the Skill

Accept the skill location as a directory path containing SKILL.md. Auto-detect if the current working directory contains one.

### Step 2: Review

Run both tools, then evaluate.

**2a. Automated linting:**

```bash
python3 {SKILL_DIR}/scripts/validate.py run --path <skill-path>
```

Output: `checks` (hard-rule verdicts → linter grade) + `findings` (soft detections needing judgment).

**2b. Profile extraction:**

```bash
bash {SKILL_DIR}/scripts/analyze.sh analyze <skill-path>
```

Note skill level (l0/l0plus/l1) and feature flags.

**2c. Contextual findings review:**

Judge each finding using its `context_hint`. See `references/semantic_dimensions.md` § Finding Judgment Table for decision criteria. Promote real issues to warnings; dismiss the rest with a brief note.

**2d. Semantic review:**

Read the skill's SKILL.md fully, then score each dimension (0-3). Read `references/semantic_dimensions.md` for the full checklist per dimension:

| Dimension | What it evaluates |
|-----------|------------------|
| 5.1 Description Quality | Trigger phrases, length, voice, specificity |
| 5.2 Workflow Design | Steps, decision points, SKILL.md length |
| 5.3 Runtime Robustness | Preflight, degradation, troubleshooting (L0+/L1 only) |
| 5.4 Script Quality | JSON output, error handling, exit codes (scripts only) |
| 5.5 UX Practices | Language, checklist, completion report (applicability matrix) |
| 5.6 Setup Flow Integrity | Bootstrap safety, live validation, credential security |

### Step 3: Present Findings

Format the report:

```
[Skill Review] <skill-name>

═══ Linter ═══
Grade: <letter> (<pass>/<total> passed, <warn> warnings, <fail> failures)

Failures:
  ✗ <check_id>: <message> → Fix: <fix>

Warnings:
  ⚠ <check_id>: <message>

Findings (agent-reviewed):
  ✓ <finding_id>: dismissed — <reason>
  ⚠ <finding_id>: promoted to warning — <reason>

═══ Semantic Review ═══
5.1 Description Quality:   <score>/3  <one-line assessment>
5.2 Workflow Design:        <score>/3  <one-line assessment>
5.3 Runtime Robustness:     <score>/3  <one-line assessment>
5.4 Script Quality:         <score>/3  <one-line assessment>
5.5 UX Practices:           <score>/3  <one-line assessment>
5.6 Setup Flow Integrity:   <score>/3  <one-line assessment>
                            ─────────
Semantic Score:             <total>/18

═══ Improvement Suggestions ═══
For each dimension scoring < 3, provide:
  1. What to change and why
  2. Which file to edit
  3. A concrete before/after example or specific instruction
  4. Priority: High (functionality/UX) / Medium (convention) / Low (polish)
```

If linter grade is A and semantic score ≥ 15: congratulate and suggest publishing with `better-skill-publish`.

### Step 4: Fix Gate

Ask the user:

- **Fix all** — Apply all suggested changes, then auto-verify (Step 5)
- **Pick and choose** — Select specific items, then auto-verify (Step 5)
- **None** — End here, use the report as reference

After fixing, **do NOT self-evaluate**. Proceed directly to Step 5.

### Step 5: Verify & Iterate

**CRITICAL: Verification must be independent.** The agent that fixed cannot judge its own work.

**5a. Dispatch verification subagent:**

```
Agent(subagent_type: "general-purpose", description: "Verify skill review", prompt: <template>)
```

Use the prompt template from `references/semantic_dimensions.md` § Verification Subagent Prompt Template. The verification subagent must:
1. Run `validate.py` and `analyze.sh` fresh (never trust cached results)
2. Read `references/semantic_dimensions.md` for scoring criteria
3. Score all 6 dimensions independently, citing file:line evidence
4. Return linter grade + per-dimension scores + specific FAIL items

**5b. Process verification result:**

- **All pass** → Report success, done
- **Has failures** → Fix ONLY the specific FAIL items from the verification report, then dispatch a NEW subagent to verify again
- **Max 3 rounds** — if issues persist after 3 fix-verify cycles, report remaining issues and let the user decide

**Anti-patterns (never do these):**

| Anti-pattern | Why it's wrong | Correct approach |
|---|---|---|
| Self-evaluate after fixing | Blind to own mistakes | Always dispatch subagent |
| Reuse same subagent for re-verify | Already biased by prior assessment | New subagent each round |
| Fix without running tools first | Subjective judgment misses issues | Tools produce objective data |
| Ignore verification report | Discards independent evidence | Fix only reported FAIL items |

## Linter Reference

**Grading** (hard-rule checks only):

- **A** — All pass, zero warnings
- **B** — All pass, some warnings
- **C** — 1–2 failures
- **D** — 3+ failures
- **F** — SKILL.md missing or no valid frontmatter

**Check categories:**

| Category | Checks |
|----------|--------|
| structure | SKILL.md exists, frontmatter, required fields, directory layout |
| naming | Kebab-case, length, no consecutive hyphens, matches directory |
| content | Description length, body length, heading structure |
| paths | Referenced files exist, scripts executable |
| security | No secrets, no template placeholders |

## References

- `references/semantic_dimensions.md` — Full checklist for each review dimension + finding judgment table + verification prompt template
- `references/validation_rules.md` — Rationale for each linter check
- `references/improvement_patterns.md` — Knowledge base of improvement patterns with examples
- `references/best_practices.md` — Skill design conventions and quick reference
