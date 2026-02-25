---
name: workleap-skill-optimizer
description: |
  Optimize agent skills to reduce context bloat while preserving answer coverage. Use when:
  (1) A skill's SKILL.md body exceeds ~250 lines or duplicates its references/ files
  (2) A skill's YAML description is verbose or triggers false positives from sibling skills
  (3) Planning or executing a body/reference split for a skill
  (4) Auditing skill token efficiency
disable-model-invocation: true
metadata:
  version: 1.2
---

# Skill Optimizer

Reduce skill token cost without losing coverage. Every token in SKILL.md body is paid per conversation — references/ files are loaded on-demand.

## Optimization Workflow

### Phase 1: Analyze

Measure the current skill before changing anything.

1. Count SKILL.md body lines (exclude frontmatter) and estimate tokens (~4.5 tokens/line for mixed code/prose).
2. Count description characters.
3. List every `references/` file with line counts.
4. Identify duplication: for each body section (at any heading level), check if the same concept or procedure is also covered in a reference file. Count those body lines and divide by total body lines for the overlap percentage.
5. List nouns from the description that appear verbatim in a sibling skill's description — these need domain-qualifying in Phase 2.

If the skill has no `references/` directory, optimization may require creating reference files first. See the [playbook](references/optimization-playbook.md#pre-optimization-checklist) for guidance on this edge case.

Output a table:

```
| Metric              | Current |
|---------------------|---------|
| Description chars   | ???     |
| Body lines          | ???     |
| Body tokens (est.)  | ???     |
| Duplication %       | ???     |
| Reference files     | ???     |
```

### Phase 2: Plan

Decide what stays in the body, what moves to references, and what gets compressed.

**Body retention criteria** — keep a section in the body ONLY if it meets at least one:
- Complex multi-step pattern requiring coordination across multiple sections or files
- Non-obvious logic, parameters, or decision rules that agents frequently get wrong without inline guidance
- A concept unique to this skill with no external documentation
- Primary use case the skill exists for (the thing agents reach for most often)

Everything else belongs in the appropriate `references/` file. See the [playbook decision tree](references/optimization-playbook.md#body-retention-decision-tree) for concrete examples of what typically stays vs. moves.

**Description compression rules:**
1. Lead with the package/tool name and a one-line identity
2. Replace enumerations of 4+ specific names (APIs, checks, steps) with category-based phrasing (e.g., "hooks for auth, sessions, tokens" instead of listing each hook name)
3. Qualify generic keywords with the skill's domain to reduce false positives (e.g., "MyLib integrations with Redis" not "Redis integration")
4. Merge items that share a theme into a single line (e.g., "error handling" + "retry logic" → "Error handling and retry logic in MyLib")
5. Verify every original trigger category maps 1:1 to the compressed version — no categories dropped

**Plan the Reference Guide section** — for each reference file, write a one-line description of when to read it. This section is load-bearing: it tells agents which file to consult.

**Target metrics:**
- Body: under ~250 lines
- Description: under ~700 characters
- Duplication with references: 0%

### Phase 3: Execute

Apply the plan. Work in this order:

1. **Compress the description** — rewrite the YAML `description` field. Keep all trigger categories; do not remove any "when to use" signals.
2. **Remove duplicate sections from body** — delete sections already covered in references.
3. **Add the Reference Guide section** — add explicit pointers to each reference file with descriptions. This section is the primary signal that tells both agents and future editors where detailed content lives. Each entry should clearly describe what the file covers so editors naturally add new content to the appropriate reference file rather than the body. See the [playbook](references/optimization-playbook.md#reference-guide-pattern) for the recommended format.
4. **Bump version** — increment `metadata.version` minor if the skill uses versioning.

Do NOT:
- Move "when to use" triggers from description to body (description is the only field read for triggering)
- Remove code examples from retained body sections (they are the value)
- Create new reference files just to move content — use existing files when possible
- Add content that duplicates what is already in references

### Phase 4: Validate

Use the `Task` tool to spawn a subagent (opus model) to challenge coverage. Provide it:
1. The full SKILL.md (body + frontmatter)
2. All reference files
3. A list of 15-25 validation questions. **Prompt the user** (via `AskUserQuestion`) to provide questions the skill must answer. If the user declines or has none, derive them from the description trigger categories — see the [playbook](references/optimization-playbook.md#validation-question-generation) for derivation rules.

The subagent evaluates each question:
- **From SKILL.md alone**: YES / PARTIAL / NO
- **From SKILL.md + references**: YES / PARTIAL / NO
- **Gap**: content missing from ALL files

**Pass criteria:**
- 0 regressions (nothing answerable before that isn't answerable after)
- All trigger categories in the description still present
- Body under ~250 lines

If gaps are found, determine whether they are **pre-existing** (never covered) or **regressions** (lost during optimization). Only regressions require fixes — restore or rewrite the missing content in the body or appropriate reference file, then re-evaluate only the affected questions.

**Fallback:** If subagent spawning is unavailable, self-evaluate: for each question, attempt to answer it using only the optimized files and rate confidence as HIGH / MEDIUM / LOW. Any LOW-confidence answer on a question that was previously answerable is a regression.

### Output

After validation, produce a summary table:

```
| Metric            | Before | After  | Change |
|-------------------|--------|--------|--------|
| Description chars | ???    | ???    | -??%   |
| Body lines        | ???    | ???    | -??%   |
| Body tokens (est.)| ???    | ???    | -??%   |
| Duplication %     | ???    | 0%     | -??%   |
| Regressions       | n/a    | 0      |        |
```

## Reference

For detailed checklists, before/after examples, and the full validation methodology, see [optimization-playbook.md](references/optimization-playbook.md).
